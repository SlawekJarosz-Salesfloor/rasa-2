import json
import os
import sys
from datetime import datetime

sys.path.append('../ontology-lib')
# pyright: reportMissingImports=false
from ontology_tools import get_name_url_mapping 

NLU_MIN_ENTITIES = 10

class Rasa_Nlu():
    def __init__(self, product_dbs) -> None:
        self.product_dbs = product_dbs

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
                        print(f'[{product["name"]}] URI ' + tag['label'] + ' found in the tagging data but not the ontology.  Skipping tag.')
                        continue

                    if tag['start'] >= prev_end:
                        item_text = item_text[0:tag['start'] + extra_chars] + '[' + item_text[tag['start'] + extra_chars:tag['end'] + extra_chars] + ']{"entity": "' + f'{entity}' + '"}' + item_text[tag['end'] + extra_chars:]
                        extra_chars += len(entity)
                        entities[entity]['count'] += 1
                    else:
                        print(f'Embedded tag in {product["name"]}... skipping.')
                        continue

                    item_text = item_text.replace('-', ' ')

                    prev_end = tag['end']            
                    extra_chars += len('[]{"entity": ""}')

                if '[__' in item_text:
                    print('Malformed tagging... skipping.')
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
            
            nlu_file_out.write('    - ' + parts[-1].replace('_', ' ') + '\n')
            
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
        print('\nDatabase: ' + db_name)
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
            if self.optimized_entity_count[entity] < NLU_MIN_ENTITIES and is_entity_in_text[entity]:
                is_keep = True
                break        
        if is_keep:
            return nlu_text
        # else:
        #     print('Skipping: ' + nlu_text)
            
        return None

    def create_nlu(self):
        superset_entities     = {}
        superset_descriptions = set()
        superset_names        = set()
        
        extra_entities   = json.load(open('./prep/extra_entity.json', 'r'))
        omitted_entities = json.load(open('./prep/remove_entity.json', 'r'))
        print(f'Following entities will be omitted: {omitted_entities}')

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
                    if entity_name in omitted_entities:
                        continue
                    entities[entity_name] = {entity_name: name_url_mapping[key], 'count': 0}

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
                superset_names.add(nlu_text)
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

        nlu_file_out = open('./prep/superset_entities.yml', 'w')
        for name in superset_entities:
            nlu_file_out.write('  - ' + name + '\n')
        nlu_file_out.close()

        if os.path.isfile('./data/nlu.yml'):
            os.rename('./data/nlu.yml', './data/nlu_' + str(datetime.now()) + '.yml_BAK')

        nlu_file_out = open('./data/nlu.yml', 'w')
        nlu_file_out.write('version: "3.1"\n')
        nlu_file_out.write(f'# SUPERSET w/ top {NLU_MIN_ENTITIES} [' + ','.join(self.product_dbs.keys())[:50] + f'] @ {datetime.now()}\n\n')
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

        self.optimized_entity_count = {}
        for entity in superset_entities:
            self.optimized_entity_count[entity] = 0

        skipped_nlu_count = 0
        nlu_file_out.write('- intent: sf_apparel__title_tags\n  examples: |\n')
        for nlu_text in superset_names:
            nlu_text_out = self.is_optimize(nlu_text, superset_entities)
            if nlu_text_out == None:
                skipped_nlu_count += 1
            else:
                nlu_file_out.write('    - ' + nlu_text + '\n')

        nlu_file_out.write('\n- intent: sf_apparel__description_tags\n  examples: |\n')
        for nlu_text in superset_descriptions:
            nlu_text_out = self.is_optimize(nlu_text, superset_entities)
            if nlu_text_out == None:
                skipped_nlu_count += 1
            else:
                nlu_file_out.write('    - ' + nlu_text + '\n')
        with open('./prep/extra_sf_apparel__description_tags.yml', 'r') as extra_match_file:
            extra_match_topic = extra_match_file.read()
        nlu_file_out.write(extra_match_topic)

        with open('./prep/extra_topics.yml', 'r') as extra_topics_file:
            extra_match_topic = extra_topics_file.read()
        nlu_file_out.write('\n' + extra_match_topic)

        nlu_file_out.close()

        self.calculate_db_stats(superset_entities, 'SUPERSET NLU')
        print('Number of skipped NLU training lines = ', skipped_nlu_count)

# main driver function
if __name__ == '__main__':
    nlu = Rasa_Nlu
    nlu.create_nlu()