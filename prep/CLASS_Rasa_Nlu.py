import json
import os
import sys
from datetime import datetime

from CLASS_Product_Database import printInfo, printWarning, throwError
from CLASS_Convert_Nlu import CLASS_Convert_Nlu

sys.path.append('../ontology-lib')
# pyright: reportMissingImports=false
from ontology_tools import get_name_url_mapping 

NLU_MIN_ENTITIES = 20

class Rasa_Nlu():
    def __init__(self, product_dbs, entity_limit) -> None:
        self.product_dbs = product_dbs
        self.entity_limit = NLU_MIN_ENTITIES
        if not entity_limit == None:
            if not entity_limit == '':
                self.entity_limit = int(entity_limit)

    # Helper functions
    def get_entity_using_uri(self, uri, entities):
        for entity in entities:
            for key in entities[entity]:
                if entities[entity][key] == uri:
                    return key
        return None

    def get_tags(self, products, tagging_item, entities):
        all_tagged_descriptions = set()
        for product in products:
            tags = product['labeling']['annotations'][tagging_item]['tags']
            if len(tags) > 0:
                item_text = product['labeling']['annotations'][tagging_item]['text']
                extra_chars = 0
                prev_end  = -1
                sorted_tags = sorted(tags, key=lambda x: x['start'])

                for tag in sorted_tags:
                    # text_tagged = item_text[tag['start'] + extra_chars:tag['end'] + extra_chars]
                    # # Don't accept percentages or pure numbers
                    # if text_tagged.endswith('%'):
                    #     continue
                    # if text_tagged.isnumeric():
                    #     continue

                    try:
                        entity = self.get_entity_using_uri(tag['label'], entities)
                    except Exception as exc:
                        print(exc)
                        continue
                    if entity == None:
                        printWarning(f'[{product["name"]}] URI ' + tag['label'] + ' found in the tagging data but not the ontology.  Skipping tag.')
                        continue

                    if tag['start'] >= prev_end:
                        item_text = item_text[0:tag['start'] + extra_chars] + '[' + item_text[tag['start'] + extra_chars:tag['end'] + extra_chars] + ']{"entity": "' + f'{entity}' + '"}' + item_text[tag['end'] + extra_chars:]
                        extra_chars += len(entity)
                        entities[entity]['count'] += 1
                    else:
                        printWarning(f'Embedded tag in {product["name"]}... skipping.')
                        continue

                    item_text = item_text.replace('-', ' ')

                    prev_end = tag['end']            
                    extra_chars += len('[]{"entity": ""}')

                if '[__' in item_text:
                    printWarning('Malformed tagging... skipping.')
                    continue

                all_tagged_descriptions.add(item_text)

        return all_tagged_descriptions

    def write_entities_section(self, entities, extra_entities, nlu_file_out):
        for entity in entities:
            if entities[entity]['count'] == 0:
                continue
            nlu_file_out.write(f'- lookup: {entity}\n')
            nlu_file_out.write( '  examples: |\n')
            parts = entity.split('__')

            out_text = parts[-1].replace('_', ' ')

            nlu_file_out.write('    - ' + out_text + '\n')
            
            for extras in extra_entities:
                if extras == entity:
                    nlu_file_out.write('\n')
                    nlu_file_out.write(f'- synonym: {entity}\n')
                    nlu_file_out.write( '  examples: |\n')
                    for item in extra_entities[extras]:
                        nlu_file_out.write(f'    - {item}\n')
                    
            nlu_file_out.write('\n')

    def calculate_db_stats(self, entities, db_name):
        import tabulate
        entity_stats = []
        sorted_keys = sorted(list(entities.keys()))
        for item in sorted_keys:
            colour_start = ''
            colour_end   = ''
            if entities[item]['count'] < 2:
                colour_start = "\033[31m"
                colour_end   = "\033[0m"
            elif entities[item]['count'] < 5:
                colour_start = "\033[33m"
                colour_end   = "\033[0m"
            output_count = colour_start + str(entities[item]['count']) + colour_end
            entity_stats.append([item, output_count])
        printInfo(f'\nDatabase: {db_name}')
        print(tabulate.tabulate(entity_stats, headers=['ENTITY NAME', 'COUNT']))

    def is_optimize(self, nlu_text, superset_entities):
        is_keep = False
        is_entity_in_text = {}
        for entity in superset_entities:
            is_entity_in_text[entity] = False
            if (']{"entity": "' + entity + '"}') in nlu_text:
                is_entity_in_text[entity] = True
        for entity in is_entity_in_text:
            if is_entity_in_text[entity]:            
                self.optimized_entity_count[entity] += 1
        # print(optimized_entity_count)
        for entity in self.optimized_entity_count:
            if self.optimized_entity_count[entity] < self.entity_limit and is_entity_in_text[entity]:
                is_keep = True
                break        
        if is_keep:
            return nlu_text
        # else:
        #     print('Skipping: ' + nlu_text)
            
        return None
    
    def write_text_section(self, intent_name, superset_entities, superset_texts, nlu_file_out):
        self.optimized_entity_count = {}
        for entity in superset_entities:
            self.optimized_entity_count[entity] = 0
        skipped_nlu_count = 0
        nlu_file_out.write(f'\n- intent: {intent_name}\n  examples: |\n')
        for nlu_text in superset_texts:
            nlu_text_out = self.is_optimize(nlu_text, superset_entities)
            if nlu_text_out == None:
                skipped_nlu_count += 1
            else:
                nlu_file_out.write('    - ' + nlu_text + '\n')

        return skipped_nlu_count

    def create_nlu(self):
        superset_entities     = {}
        superset_descriptions = set()
        superset_name_texts        = set()
        
        extra_entities   = json.load(open('./prep/extra_entity.json', 'r'))
        omitted_entities = json.load(open('./prep/remove_entity.json', 'r'))
        printInfo(f'Following entities will be omitted: \n{json.dumps(omitted_entities, indent=4)}')

        for category in self.product_dbs:
            product_db = self.product_dbs[category].db_content['products']
            ontology = json.loads(self.product_dbs[category].ontology)

            # uri_prefix = '/'.join(ontology['product'][0]['label'].split('/')[0:-1])
            name_url_mapping = get_name_url_mapping(ontology, {})
            entities = {}
            for key in name_url_mapping:
                if '|' in key:
                    concept_name = key.replace(' ', '_').replace('-', '_').replace('|', '__')
                    entity_name = 'sf_apparel_' + concept_name
                    if entity_name in omitted_entities or entity_name.startswith("sf_apparel_color__"):
                        continue
                    entities[entity_name] = {entity_name: name_url_mapping[key], 'count': 0}
            entities = dict(sorted(entities.items()))

            nlu_file_out = open('./prep/backup/' + category + '_entities.yml', 'w')
            for name in entities:
                nlu_file_out.write('  - ' + name + '\n')
            nlu_file_out.close()

            nlu_file_out = open('./prep/backup/' + category + '_nlu.yml', 'w')

            nlu_file_out.write('version: "3.1"\n')
            nlu_file_out.write(f'# {category} @ {datetime.now()}\n\n')
            nlu_file_out.write('nlu:\n')

            tagged_titles = self.get_tags(product_db, 'name', entities)        
            tagged_descriptions = self.get_tags(product_db, 'description', entities)

            self.write_entities_section(entities, extra_entities, nlu_file_out)

            nlu_file_out.write('- intent: sf_apparel__title_tags\n  examples: |\n')
            for nlu_text in tagged_titles:
                superset_name_texts.add(nlu_text)
                nlu_file_out.write('    - ' + nlu_text + '\n')

            nlu_file_out.write('\n- intent: sf_apparel__description_tags\n  examples: |\n')
            for nlu_text in tagged_descriptions:
                superset_descriptions.add(nlu_text)
                nlu_file_out.write('    - ' + nlu_text + '\n')

            nlu_file_out.close()

            # update the count for all entities
            for entity in entities:
                if entity in superset_entities:
                    superset_entities[entity]['count'] += entities[entity]['count']
                    continue
                superset_entities[entity] = entities[entity]

            self.calculate_db_stats(entities, category)

        ## Create a superset NLU
        low_count_entities = []
        for entity in superset_entities:
            if superset_entities[entity]['count'] < 2:
                low_count_entities.append(entity)
        json.dump(low_count_entities, open('./prep/remove_entity_auto.json', 'w'), indent=4)

        nlu_file_out = open('./prep/superset_entities.yml', 'w')
        superset_entities = dict(sorted(superset_entities.items()))
        for name in superset_entities:
            nlu_file_out.write('  - ' + name + '\n')
        nlu_file_out.close()

        if os.path.isfile('./data/nlu.yml'):
            os.rename('./data/nlu.yml', './data/nlu_' + str(datetime.now()) + '.yml_BAK')

        nlu_file_out = open('./data/nlu.yml', 'w')
        nlu_file_out.write('version: "3.1"\n')
        nlu_file_out.write(f'# SUPERSET w/ top {self.entity_limit} [' + ','.join(self.product_dbs.keys())[:50] + f'] @ {datetime.now()}\n\n')
        nlu_file_out.write('nlu:\n')

        nlu_file_out.write('# ====================\n')
        nlu_file_out.write('# === NLU ENTITIES ===\n')
        nlu_file_out.write('# ====================\n')

        self.write_entities_section(superset_entities, extra_entities, nlu_file_out)

        with open('./prep/product_category_entity.yml', 'r') as product_category_file:
            category_entity = product_category_file.read()
        nlu_file_out.write(category_entity + '\n')

        with open('./prep/no_match_entities.yml', 'r') as extra_topics_file:
            no_match_enity = extra_topics_file.read()
        nlu_file_out.write('# ARTIFICIAL NO MATCH ENTITIES START\n' + no_match_enity)
        nlu_file_out.write('# ARTIFICIAL NO MATCH ENTITIES END\n\n\n')

        nlu_file_out.write('# ==================\n')
        nlu_file_out.write('# === NLU TOPICS ===\n')
        nlu_file_out.write('# ==================\n')

        skipped_nlu_count = self.write_text_section('sf_apparel__title_tags', superset_entities, superset_name_texts, nlu_file_out)
        skipped_nlu_count += self.write_text_section('sf_apparel__description_tags', superset_entities, superset_descriptions, nlu_file_out)

        with open('./prep/extra_sf_apparel__description_tags.yml', 'r') as extra_match_file:
            extra_match_topic = extra_match_file.read()
        nlu_file_out.write(extra_match_topic)

        with open('./prep/extra_topics.yml', 'r') as extra_topics_file:
            extra_match_topic = extra_topics_file.read()
        nlu_file_out.write('\n' + extra_match_topic)

        nlu_file_out.close()

        self.calculate_db_stats(superset_entities, 'SUPERSET NLU')
        printInfo(f'Number of skipped NLU training lines = {skipped_nlu_count}')


        ### WORK ON 2 level NLU structure ###
        # Entity limit for 2nd step NLU can be much larger
        self.entity_limit = self.entity_limit*10

        converter = CLASS_Convert_Nlu(superset_entities, superset_name_texts, superset_descriptions)
        converter.convert_entities()
        converter.convert_titles()
        converter.convert_descriptions()

        nlu_file_out = open('./prep/domain_2_levels.yml', 'w')
        nlu_file_out.write('''        
version: "3.1"

intents:
  - sf_apparel__description_tags
  - sf_apparel__NO_MATCH

entities:
''')
        converter.write_all_entities(extra_entities, nlu_file_out)
        nlu_file_out.write('''
# Manually added
  - sf_apparel_NO_MATCH__sleeves

responses:
  utter_sf_prompt_customer_service:
  - text: "How can I help you?"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
''')
        nlu_file_out.close()


        nlu_file_out = open('./data/nlu_1st_level.yml', 'w')
        nlu_file_out.write('version: "3.1"\n')
        nlu_file_out.write(f'# 1st Level NLU w/ top {self.entity_limit} [' + ','.join(self.product_dbs.keys())[:50] + f'] @ {datetime.now()}\n\n')
        nlu_file_out.write('nlu:\n')

        nlu_file_out.write('# ====================\n')
        nlu_file_out.write('# === NLU ENTITIES ===\n')
        nlu_file_out.write('# ====================\n')

        converter.write_top_level_entities_section({}, nlu_file_out)
        # skipped_nlu_count = self.write_text_section('sf_apparel__title_tags', converter.top_down_entities, converter.title_texts, nlu_file_out)
        skipped_nlu_count += self.write_text_section('sf_apparel__description_tags', converter.top_down_entities, converter.title_texts + converter.description_texts, nlu_file_out)

        nlu_file_out.write('''
\n- intent: sf_apparel__NO_MATCH
  examples: |
    - Shall we focus on a specific silhouette or detail that interests you?
    - Complete the ensemble with a pair of strappy sandals and delicate accessories to complement the cheerful and celebratory atmosphere of the wedding.
    - Enjoy your new dress at the party!
''')
        nlu_file_out.close()

        entity_groups = json.load(open('./prep/_entity_groups.json', 'r'))
        # Validate the groups in the entity file
        for group_nb in entity_groups:
            is_found = False
            for group_entity in entity_groups[group_nb]:
                for top_entity in converter.top_down_entities:
                    if group_entity == top_entity:
                        is_found = True
                        break
                if not is_found:
                    printWarning(f'Entity {group_entity} not found in the ontology.')

        for top_entity in converter.top_down_entities:
            is_found = False
            for group_nb in entity_groups:
                for group_entity in entity_groups[group_nb]:                
                    if group_entity == top_entity:
                        is_found = True
                        break
            if not is_found:
                throwError(f'Entity from the ontology {top_entity} not found in the entity groups.')                

        # Set the entity limit to be unlimited
        for group_nb in entity_groups:
            nlu_file_out = open(f'./data/nlu_2nd_level_{group_nb}.yml', 'w')
            nlu_file_out.write('version: "3.1"\n')
            nlu_file_out.write(f'# 1st Level NLU w/ top {self.entity_limit} [' + ','.join(self.product_dbs.keys())[:50] + f'] @ {datetime.now()} \n')
            nlu_file_out.write(f'# For the following attributes: {", ".join(entity_groups[group_nb])} \n\n')
            nlu_file_out.write('nlu:')

            entity_group = {}
            for entity in entity_groups[group_nb]:
                entity_group[entity] = {}
                entity_group[entity]['count'] = 1

            converter.write_entities_section(entity_group, {}, nlu_file_out)

            # converter.write_text_section('sf_apparel__title_tags', entity_group, superset_name_texts, nlu_file_out)
            converter.write_text_section('sf_apparel__description_tags', entity_group, list(superset_name_texts) + list(superset_descriptions), nlu_file_out)
            nlu_file_out.write('''
\n- intent: sf_apparel__NO_MATCH
  examples: |
    - Shall we focus on a specific silhouette or detail that interests you?
    - Complete the ensemble with a pair of strappy sandals and delicate accessories to complement the cheerful and celebratory atmosphere of the wedding.
    - Enjoy your new dress at the party!
''')
            nlu_file_out.close()

# main driver function
if __name__ == '__main__':
    nlu = Rasa_Nlu
    nlu.create_nlu()