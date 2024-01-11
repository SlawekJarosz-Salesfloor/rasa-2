import json
import subprocess

from CLASS_Product_Database import *

CLONE_CMD_TEMPLATE = 'frisson dyson clone-db --from playground --fromNamespace maestro-v2-dev --to playground --toNamespace maestro-v2-dev'

class Production_Workflow():
    def __init__(self, category) -> None:
        self.product_db = Product_Database(category)

    def TEST_FUNCTION(self):
        time_start = time.perf_counter()
        for idx in range(0, 10):
            printProgressBar(idx, 10, startTime=time_start)
            time.sleep(1)

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

    def get_baseline_stats(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        self.product_db.get_ontology()
        self.product_db.check_ontology()
        self.product_db.compare_ontology()

        # Get # of records
        self.product_db.connect_db()
        self.product_db.count_number_of_records()

    def migrate_data(self, source_db_name):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        nb_records_before = self.product_db.migrate_data(source_db_name)
        while not self.product_db.nb_records == nb_records_before:
            try:
                self.product_db.count_number_of_records()
                if self.product_db.nb_records == nb_records_before:
                    break
            except:
                pass
            printInfo(f'Waiting for all records [{nb_records_before - self.product_db.nb_records} more] to be moved over to {self.product_db.db_name}')
            time.sleep(30)

    def map_visual_tags(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        # Map ViSenze tags to Salesfloor ontology
        self.product_db.map_products_to_visenze()

    def fix_description(self):
        self.product_db.set_db_name(Production_Step.PRODUCTS)
        # Removed unwanted characters from description
        self.product_db.fix_description()

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
                time.sleep(5)
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
                        time.sleep(30)
                printInfo(f'{command[-2]} to {command[-1]} cloned successfully.')
                is_clone = False
            else:
                printWarning(f'Could not clone [{command[-2]}]. {result.stderr[7:].strip()}.')
                if '500:Internal Server Error' in result.stderr:
                    printWarning('Trying again in 30 seconds.')
                    time.sleep(30)
                else:
                    throwError(f'Failed to clone [{command[-2]}]. {result.stderr[7:].strip()}.')
        self.product_db.compare_ontology()

    def clone_products_to_llm_db(self):
        # From products db to llm db
        self.clone_helper(Production_Step.PRODUCTS, Production_Step.LLM)

    def tag_llm(self):
        # Tag db using LLM
        self.product_db.set_db_name(Production_Step.LLM)
        self.product_db.collect_existing_tags()

        tag_target = int(self.product_db.nb_records * 0.1)
        try:
            self.product_db.tag_products(tag_target)                
        except:
            throwError(f'Could not finish LLM tagging of {self.product_db.get_db_name()}')

    def clone_llm_to_fix_db(self):
        # From llm db to fix db
        self.clone_helper(Production_Step.LLM, Production_Step.FIX)    

    def fix_llm_tags(self):
        # Correct LLM tags
        self.product_db.set_db_name(Production_Step.FIX)
        self.product_db.collect_existing_tags()

        wrong_tag_mapping = json.load(open('./prep/wrong_labels.json', 'r'))
        count = 1
        while True:
            print(f'Fixing LLM tags: pass #{count}')
            count += 1
            nb_fixed_products = self.product_db.correct_tags(wrong_tag_mapping)
            if nb_fixed_products == 0 or count == 10:
                break

    def clone_fix_to_rasa_db(self):
        # From fix db to rasa db
        self.clone_helper(Production_Step.FIX, Production_Step.RASA)        

    def tag_rasa(self):
        # Tag db using Rasa
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.collect_existing_tags()

        tag_target = self.product_db.nb_records
        try:
            self.product_db.tag_products(tag_target, llm_type='Rasa')                
        except:
            throwError(f'Could not finish Rasa tagging of {self.product_db.get_db_name()}')

    def validate_clu(self):
        # Tag db using Rasa
        self.product_db.set_db_name(Production_Step.RASA)
        self.product_db.collect_existing_tags()
        self.product_db.validate_clu()

    def delete_db(self, db_type):
        self.product_db.destroy()


# main driver function
if __name__ == '__main__':
    workflow = Production_Workflow('CoatsJackets')
    workflow.prep_dbs()
