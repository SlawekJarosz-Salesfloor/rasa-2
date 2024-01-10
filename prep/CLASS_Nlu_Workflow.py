import pprint

from CLASS_Product_Database import *
from CLASS_Rasa_Nlu import *

def check_for_duplicates(representations):
    duplicates = {}
    for outer_label in representations:
        for inner_label in representations:
            if outer_label == inner_label:
                continue
            for outer_value in representations[outer_label]:
                for inner_value in representations[inner_label]:
                    if outer_value == inner_value:
                        if not outer_value in duplicates:
                            duplicates[outer_value] = []                                
                        if sorted([outer_label, inner_label]) in duplicates[outer_value]:
                            continue
                        duplicates[outer_value].append(sorted([outer_label, inner_label]))
                        print(f'Duplicate attribute value [{outer_value}]: {outer_label} and {inner_label}')

class Nlu_Workflow():
    def __init__(self, product_categories, is_use_cache = False) -> None:
        self.is_use_cache = is_use_cache
        self.product_dbs = {}
        self.product_categories = product_categories
        for category in self.product_categories:
            self.product_dbs[category] = Product_Database(category)
            self.product_dbs[category].set_db_name(Production_Step.FIX)
            self.product_dbs[category].is_use_cache = self.is_use_cache
            self.product_dbs[category].connect_db()
            self.product_dbs[category].get_ontology()
            self.product_dbs[category].count_number_of_records()

    def check_tag_quality(self):
        pp = pprint.PrettyPrinter(indent=4)
        
        entity_representations = {}
        entity_representations['TOTAL'] = {}
        for category in self.product_dbs:
            self.product_dbs[category].set_tag_usage()
            entity_representations[category] = self.product_dbs[category].representations
            pp.pprint(self.product_dbs[category].description_tag_density)
            entity_representations['TOTAL'].update(entity_representations[category])
        print('\n\n\n === FINAL REPRESENTATIONS ===')
        pp.pprint(entity_representations)

        for category in self.product_categories:
            print('\n\nEntity mapping for ' + category)
            check_for_duplicates(entity_representations[category])


    def generate_nlu(self):
        for category in self.product_categories:
            self.product_dbs[category].collect_existing_tags()
        nlu = Rasa_Nlu(self.product_dbs)
        nlu.create_nlu()


# main driver function
if __name__ == '__main__':
    product_categories = ['CoatsJackets']
    workflow = Nlu_Workflow(product_categories)
