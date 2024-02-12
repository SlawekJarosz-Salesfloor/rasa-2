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
    def __init__(self, product_categories, entity_limit=None) -> None:
        self.product_dbs = {}
        self.product_categories = product_categories
        for category in self.product_categories:
            self.product_dbs[category] = Product_Database(category)
            self.product_dbs[category].set_db_name(Production_Step.FIX)
            self.product_dbs[category].connect_db()
            self.product_dbs[category].get_ontology()
            self.product_dbs[category].count_number_of_records()
        self.entity_limit = entity_limit
        
    def check_tag_quality(self):
        pp = pprint.PrettyPrinter(indent=4)
        
        entity_representations = {}
        entity_representations['TOTAL'] = {}
        
        for category in self.product_dbs:
            self.product_dbs[category].set_tag_usage()
            entity_representations[category] = self.product_dbs[category].representations
            pp.pprint(self.product_dbs[category].description_tag_density)
            
            for attribute in self.product_dbs[category].representations:
                if attribute in entity_representations['TOTAL']:
                    entity_representations['TOTAL'][attribute].update(self.product_dbs[category].representations[attribute])
                else:
                    entity_representations['TOTAL'][attribute] = self.product_dbs[category].representations[attribute]



        print('\n\n\n === FINAL REPRESENTATIONS ===')
        pp.pprint(entity_representations)

        for category in self.product_categories:
            print('\n\nEntity mapping for ' + category)
            check_for_duplicates(entity_representations[category])


    def generate_nlu(self):
        for category in self.product_categories:
            self.product_dbs[category].collect_existing_tags()
        nlu = Rasa_Nlu(self.product_dbs, self.entity_limit)
        nlu.create_nlu()

    def search_dbs(self, search_text):
        all_products_found = []
        for category in self.product_categories:
            products_found = self.product_dbs[category].search_for_text(search_text)
            printInfo(f'Products found containing "{search_text}" in {category}:')
            for product_name in products_found:
                all_products_found.append(f'{category}: {product_name}')

        if len(all_products_found) > 100:
            subset_found = all_products_found[:99]
            subset_found.append('... more found ...')
            return subset_found
        return all_products_found
    
# main driver function
if __name__ == '__main__':
    product_categories = ['CoatsJackets']
    workflow = Nlu_Workflow(product_categories)
