import shutil
import subprocess

from CLASS_Product_Database import *

CLONE_CMD_TEMPLATE = 'frisson dyson clone-db --from playground --fromNamespace maestro-v2-dev --to playground --toNamespace maestro-v2-dev'

class Production_Workflow():
    def __init__(self, category) -> None:
        self.product_db = Product_Database(category)

    def prep_dbs(self):
        # Get ontology
        self.product_db.set_db_name(Production_Step.ONTOLOGY)
        self.product_db.get_ontology()
        self.product_db.check_ontology()
        self.product_db.set_base_ontology()

    def update_ontology(self):
        self.product_db.set_db_name(Production_Step.ONTOLOGY)
        self.product_db.update_ontology()

    def clone_ontology_to_products_db(self):
        # From products db to llm db
        self.clone_helper(Production_Step.ONTOLOGY, Production_Step.PRODUCTS)
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        # TODO: Workaround - the first time, the ontology is not copied properly (still the original ontology)
        self.delete_db()        
        self.clone_helper(Production_Step.ONTOLOGY, Production_Step.PRODUCTS)
        self.product_db.set_db_name(Production_Step.PRODUCTS)

    def get_baseline_stats(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        self.product_db.get_ontology()
        self.product_db.check_ontology()
        self.product_db.compare_ontology()

        # Get # of records
        self.product_db.connect_db()
        self.product_db.count_number_of_records()


    def wait_for_product_count(self, nb_records_before):
        while not self.product_db.nb_records == nb_records_before:
            try:
                self.product_db.count_number_of_records()
                if self.product_db.nb_records == nb_records_before:
                    break
            except:
                pass
            printInfo(f'Waiting for all records [{nb_records_before - self.product_db.nb_records} more]...')
            time.sleep(RECONNECTION_SLEEP*3)

    def migrate_data(self, source_db_name):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        nb_records_before = self.product_db.migrate_data(source_db_name)
        self.wait_for_product_count(nb_records_before)

    def map_visual_tags(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        # Map ViSenze tags to Salesfloor ontology
        nb_records_before = self.product_db.count_number_of_records()
        self.product_db.db_content = None
        self.product_db.map_to_visense()
        self.wait_for_product_count(nb_records_before)

    def fix_description(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        # Removed unwanted characters from description
        nb_records_before = self.product_db.count_number_of_records()
        self.product_db.db_content = None
        self.product_db.fix_descriptions()
        self.wait_for_product_count(nb_records_before)

    def clone_helper(self, source_step, target_step):
        # Command template
        command = ''.join(CLONE_CMD_TEMPLATE).split()
        self.product_db.set_db_name(source_step)
        if not source_step == Production_Step.ONTOLOGY: # ontology db does not have any records
            nb_records_before = self.product_db.count_number_of_records()
        command.append(self.product_db.get_db_name())
        self.product_db.set_db_name(target_step)
        command.append(self.product_db.get_db_name())
        is_clone = True
        count_clone_attempt = 0
        while is_clone:
            count_clone_attempt += 1
            result = subprocess.run(command,
                                    capture_output = True, # Python >= 3.7 only
                                    text = True # Python >= 3.7 only
                                    )
            if result.returncode == 0:
                time.sleep(RECONNECTION_SLEEP)
                if not source_step == Production_Step.ONTOLOGY:                    
                    self.product_db.nb_records = 0
                    while not self.product_db.nb_records == nb_records_before:
                        try:
                            self.product_db.count_number_of_records()
                            if self.product_db.nb_records == nb_records_before:
                                break
                        except:
                            pass
                        printInfo(f'Waiting for all records [{nb_records_before - self.product_db.nb_records} more] to be cloned to {self.product_db.db_name}')
                        time.sleep(RECONNECTION_SLEEP*3)
                printInfo(f'{command[-2]} to {command[-1]} cloned successfully.')
                is_clone = False
            else:
                printWarning(f'Could not clone [{command[-2]}]. {result.stderr[7:].strip()}.')
                if '500:Internal Server Error' in result.stderr:
                    printWarning('Trying again in 30 seconds.')
                    time.sleep(RECONNECTION_SLEEP)
                else:
                    throwError(f'Failed to clone [{command[-2]}]. {result.stderr[7:].strip()}.')
        self.product_db.compare_ontology()

    def clone_products_to_llm_db(self):
        # From products db to llm db
        self.clone_helper(Production_Step.PRODUCTS, Production_Step.LLM)

    def tag_llm(self):
        LLM_TAG_PERCENTAGE = 0.05
        # Tag db using LLM
        self.product_db.set_db_name(Production_Step.LLM)
        nb_records = self.product_db.count_number_of_records()
        self.product_db.collect_existing_tags()
        # self.wait_for_product_count(nb_records_before)

        tag_target = int(nb_records * LLM_TAG_PERCENTAGE)
        printInfo(f'Tagging {tag_target} products using an LLM.')
        try:
            self.product_db.tag_products(tag_target)                
        except:
            throwError(f'Could not finish LLM tagging of {self.product_db.get_db_name()}')
        printInfo(f'{self.product_db.nb_tagged_products} products tagged in {self.product_db.db_name}.')

    def clone_llm_to_fix_db(self):
        # From llm db to fix db
        self.product_db.set_db_name(Production_Step.LLM)
        llm_cache_file_name = self.product_db.get_cache_file_name()
        self.product_db.set_db_name(Production_Step.FIX)
        fix_cache_file_name = self.product_db.get_cache_file_name()
        if os.path.isfile(llm_cache_file_name):
            if not os.path.isfile(fix_cache_file_name):
                shutil.copyfile(llm_cache_file_name, fix_cache_file_name)

        self.clone_helper(Production_Step.LLM, Production_Step.FIX)


    def fix_tags(self, is_verbose=True):
        # Correct tags
        MAX_FIX_PASSES = 5
        nb_records_before = self.product_db.count_number_of_records()
        self.product_db.collect_existing_tags()
        self.wait_for_product_count(nb_records_before)
        self.product_db.is_verbose = is_verbose

        for idx in range(0, MAX_FIX_PASSES):
            printInfo(f'Fixing tags: pass #{idx + 1}')
            nb_fixed_products = self.product_db.correct_tags()
            if nb_fixed_products == 0:
                break

    def tag_explicit(self):
        # Add explicit tags
        self.product_db.set_db_name(Production_Step.FIX)
        self.product_db.collect_existing_tags()

        printInfo(f'Add explicit tags to {self.product_db.db_name}.')
        try:
            self.product_db.tag_products(llm_type='Explicit')                
        except:
            throwError(f'Could not finish LLM tagging of {self.product_db.get_db_name()}')

        printInfo(f'{self.product_db.nb_tagged_products} products tagged in {self.product_db.db_name}.')

    def fix_llm_tags(self):
        # Correct LLM tags
        self.product_db.set_db_name(Production_Step.FIX)
        self.fix_tags()

    def clone_fix_to_rasa_db(self):
        # From fix db to rasa db
        self.clone_helper(Production_Step.FIX, Production_Step.RASA)        

    def tag_rasa(self):
        # Tag db using Rasa
        self.product_db.set_db_name(Production_Step.RASA)
        nb_records_before = self.product_db.count_number_of_records()        
        self.product_db.collect_existing_tags()
        self.wait_for_product_count(nb_records_before)

        printInfo(f'Tagging remaining products using an Rasa.')
        tag_target = self.product_db.nb_records
        try:
            self.product_db.tag_products(tag_target, llm_type='Rasa')                
        except:
            throwError(f'Could not finish Rasa tagging of {self.product_db.get_db_name()}')

    def validate_clu(self):
        # Tag db using Rasa
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.validate_clu()

    def delete_db(self):
        self.product_db.destroy()

    def fix_uris(self):
        # Tag db using LLM
        self.product_db.set_db_name(Production_Step.LLM)
        self.product_db.count_number_of_records()
        self.product_db.collect_existing_tags()

        self.product_db.update_all_uris()           

    def approve_products(self):
        # Tag db using LLM
        self.product_db.set_db_name(Production_Step.FIX)
        self.product_db.count_number_of_records()
        self.product_db.collect_existing_tags()

        self.product_db.approve_tagged_products()

    def fix_rasa_tags(self):
        # Correct Rasa tags
        self.product_db.set_db_name(Production_Step.RASA)
        self.fix_tags(is_verbose=False)

    def check_consistency(self):
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.check_for_contradictions()
        
    def partially_approve_products(self):
        # Tag db using LLM
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.count_number_of_records()
        self.product_db.collect_existing_tags()

        self.product_db.partially_approve_tagged_products()

    def publish_products(self):
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.publish_products()

    def change_all_ontologies(self):
        self.prep_dbs()
        self.update_ontology()

        self.product_db.set_db_name(Production_Step.PRODUCTS)
        self.product_db.get_ontology()

        is_same = False
        try:
            self.product_db.compare_ontology(is_rebase=True)
            is_same = True
        except:
            # If there is a difference, that's good.
            pass

        if is_same:
            throwError(f'No difference between ontologies for {self.product_db.category} [ontology and products dbs].')

        for step in Production_Step:
            self.product_db.set_db_name(step)
            if step == Production_Step.ONTOLOGY:
                self.product_db.update_ontology(is_rebase=False)
                continue
            try:
                self.product_db.update_ontology(is_rebase=True)
            except Exception as exc:
                if not str(exc).endswith('does not exist.'):
                    throwError(str(exc))

    def upload_db(self, db_choice, file_name):
        self.product_db.set_db_name(Production_Step[db_choice])
        self.product_db.upload_whole_db(file_name)

# main driver function
if __name__ == '__main__':
    workflow = Production_Workflow('CoatsJackets')
    workflow.prep_dbs()
