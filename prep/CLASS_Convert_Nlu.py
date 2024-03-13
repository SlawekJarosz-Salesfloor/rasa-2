import os
import re

class CLASS_Convert_Nlu():

    def __init__(self, entities, titles, descriptions):
        self.entities = entities
        self.title_texts = list(titles)
        self.description_texts = list(descriptions)

    def convert_entities(self):
        self.top_down_entities = {}
        self.bottom_up_entities = {}
        for entity in self.entities:
            top_level_entity = entity.split('__')[0]
            if not top_level_entity in self.top_down_entities:
                self.top_down_entities[top_level_entity] = {}
                self.top_down_entities[top_level_entity]['count'] = 0
                self.top_down_entities[top_level_entity]['children'] = []
            self.top_down_entities[top_level_entity]['children'].append(entity)
            self.top_down_entities[top_level_entity]['count'] += self.entities[entity]['count']
            self.bottom_up_entities[entity] = top_level_entity

    def convert_titles(self):
        for idx, title_text in enumerate(self.title_texts):
            for entity in self.bottom_up_entities:
                if f'"entity": "{entity}"' in title_text:
                    self.title_texts[idx] = self.title_texts[idx].replace(f'"entity": "{entity}"', f'"entity": "{self.bottom_up_entities[entity]}"')

    def convert_descriptions(self):
        for idx, content in enumerate(self.description_texts):
            for entity in self.bottom_up_entities:
                if f'"entity": "{entity}"' in content:
                    self.description_texts[idx] = self.description_texts[idx].replace(f'"entity": "{entity}"', f'"entity": "{self.bottom_up_entities[entity]}"')

    def write_all_entities(self, extra_entities, nlu_file_out):
        for entity in self.top_down_entities:
            nlu_file_out.write(f'  - {entity}\n')
            for child_entity in self.top_down_entities[entity]['children']:
                nlu_file_out.write(f'  - {child_entity}\n')

    def write_top_level_entities_section(self, extra_entities, nlu_file_out):
        for entity in self.top_down_entities:
            if self.top_down_entities[entity]['count'] == 0:
                continue
            nlu_file_out.write(f'- lookup: {entity}\n')
            nlu_file_out.write( '  examples: |\n')
            for child_entity in self.top_down_entities[entity]['children']:
                parts = child_entity.split('__')
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

    def write_entities_section(self, entity_group, extra_entities, nlu_file_out):
        for entity in entity_group:
            for child_entity in self.bottom_up_entities:
                if child_entity.startswith(entity):
                    nlu_file_out.write(f'\n- lookup: {child_entity}\n')
                    nlu_file_out.write('  examples: |\n')
                    parts = child_entity.split('__')
                    out_text = parts[-1].replace('_', ' ')            
                    nlu_file_out.write('    - ' + out_text + '\n')
                
            for extras in extra_entities:
                if extras == child_entity:
                    nlu_file_out.write('\n')
                    nlu_file_out.write(f'- synonym: {entity}\n')
                    nlu_file_out.write( '  examples: |\n')
                    for item in extra_entities[extras]:
                        nlu_file_out.write(f'    - {item}\n')
                    
            nlu_file_out.write('\n')

    def write_text_section(self, intent_name, entities, nlu_training_texts, nlu_file_out):
        nlu_file_out.write(f'\n- intent: {intent_name}\n  examples: |\n')
        for training_text in nlu_training_texts:
            is_skip = True
            for entity_name in entities:
                if f'"entity": "{entity_name}' in training_text:
                    is_skip = False
                    matches = re.findall(r'{"entity": "([\w]*)"}', training_text)
                    for match_entity in matches:
                        if not match_entity.split('__')[0] in entities:
                            replace_matches = re.findall('\[([\w\s;\'\*&:]*)\]{"entity": "' + match_entity + '"}', training_text)
                            for replace_string in replace_matches:
                                training_text = training_text.replace('[' + replace_string + ']{"entity": "' + match_entity + '"}', replace_string)
                            # print(match_entity)
            if not is_skip:
                nlu_file_out.write('    - ' + training_text + '\n')
