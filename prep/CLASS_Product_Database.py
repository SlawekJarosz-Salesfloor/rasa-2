import couchdb
import json
import os
import re
import requests
import sys
import time
# import tqdm

from deepdiff import DeepDiff
from enum import Enum

from lib_tag_correction import *

sys.path.append('../ontology-lib')
# pyright: reportMissingImports=false
from ontology_tools import get_name_url_mapping 

LIMIT_DOCS_PER_QUERY = 50

# Red
def throwError(message):
    print(f"\033[31m[ERROR]\033[0m " + message)
    raise Exception(message)

# Yellow
def printWarning(message):
    print(f"\033[33m[WARNING]\033[0m " + message)

#Green
def printInfo(message):
    print(f"\033[32m[INFO]\033[0m " + message)

# From: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
# Print iterations progress
from datetime import timedelta
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", startTime = None, startOffset = 0):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        startTime   - Optional  : start time of the progress bar timedate ms (Str)
    """

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    # Estimate remaining time
    if not startTime == None:
        time_remaining = '?'
        # Remaining time can only be estimated after 20% of the task has been done
        if not (iteration - startOffset) == 0 and ((iteration - startOffset)/(total - startOffset)) > 0.2:
            time_remaining = timedelta(seconds=int((time.perf_counter() - startTime)*(total-iteration-startOffset)/(iteration - startOffset)))
        suffix = f'ETA: {time_remaining}'

    print(f'\r{prefix} |{bar}| {percent}% [{iteration}/{total}] {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# From https://stackoverflow.com/questions/60978672/python-string-to-camelcase
def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

# class syntax
class Production_Step(Enum):
    ONTOLOGY = 1
    PRODUCTS = 2
    LLM = 3
    FIX = 4
    RASA = 5
    FINAL = 6

# functional syntax
Production_Step = Enum('Production_Step', ['ONTOLOGY', 'PRODUCTS', 'LLM', 'FIX', 'RASA', 'FINAL'])

STEP_SUFFIX_MAPPING = {
    Production_Step.ONTOLOGY: 'ontology',
    Production_Step.PRODUCTS: 'products',
    Production_Step.LLM: 'llm',
    Production_Step.FIX: 'fix',
    Production_Step.RASA: 'rasa',
    Production_Step.FINAL: 'FINAL'
}

DB_RECONNECTION_SLEEP = 10 # in seconds

class Product_Database():
    def __init__(self, category) -> None:
        self.db_name = None
        self.category = category
        self.is_use_cache = False
        self.PRODUCTS_CACHE_FILE_NAME = f'_cache_{self.category}_products.json'
        self.tagged_products = {}
        self.couchdb_db_url = 'http://admin:admin@127.0.0.1:5984'
        self.dyson_url      = 'http://localhost:9005'

        self.nb_records = 0
        self.nb_tagged_products = 0

    def destroy(self):
        printInfo(f'Deleting {self.db_name} database.')
        try:
            response = requests.delete(f'{self.dyson_url}/productDatabases/{self.db_name}')
            if response.status_code == 200:
                printInfo(f'{self.db_name} deleted.')
            else:
                print(response)
                printWarning(f'Unable to delete {self.db_name}.')
        except Exception as exc:
            print(exc)
            throwError(f'Unable to delete {self.db_name}.')

    def connect_db(self):
        # while true ; do kubectl --context playground -n maestro-v2-dev port-forward service/couchdb 5984 ; done
        self.couch = couchdb.Server(self.couchdb_db_url)
        for idx in range(0,4):
            is_connect = False
            try:
                self.db = self.couch['product-recommendation']
                is_connect = True
                break
            except:
                printWarning(f'Cannot connect to {self.db_name}.  Retrying in 10 seconds [attempt #{idx + 1}]...')
                time.sleep(10)
        
        if not is_connect:
            throwError(f'Cannot connect to {self.db_name}')

    def set_db_name(self, step_enum):
        self.db_name = 'Saks-!CATEGORY!-!#!-!STEP_NAME!'.replace('!CATEGORY!', self.category).replace('!#!', str(step_enum.value)).replace('!STEP_NAME!', STEP_SUFFIX_MAPPING[step_enum])

    def get_db_name(self):
        return self.db_name

    def set_nb_records(self, overwrite_nb_records):
        if not overwrite_nb_records == None:
            self.nb_records = overwrite_nb_records
            printInfo(f'{self.nb_records} items in {self.db_name} [overwrite]')


    def get_db_records(self, nb_docs_skip):
        count_connect_attempt = 0
        docs = []
        while True:
            try:
                response = requests.get(f'{self.couchdb_db_url}/product-recommendation/_all_docs?limit={LIMIT_DOCS_PER_QUERY}&skip={nb_docs_skip}&include_docs=true&startkey="active-cosmetics-diagnostic/v1/{self.db_name}/0"&endkey="active-cosmetics-diagnostic/v1/{self.db_name}0"')
                if response.status_code == 200:
                    rows = json.loads(response.text)['rows']
                    for row in rows:
                        if 'doc' in row:
                            docs.append(row['doc'])
                else:
                    break
                # docs = self.db.find(self.mango_query)
                if count_connect_attempt > 0:
                    printInfo(f'Connection to {self.db_name} re-established.')
                break
            except:
                count_connect_attempt += 1
                if count_connect_attempt == 1:
                    print()                    
                printWarning(f'Disconnected from {self.db_name} during retrieval of {LIMIT_DOCS_PER_QUERY} records. Reconnecting in {DB_RECONNECTION_SLEEP} seconds [attempt #{count_connect_attempt}]...')
                time.sleep(DB_RECONNECTION_SLEEP)

        return docs
    
    def save_record(self, db_record):
        count_connect_attempt = 0
        count_reset_attempt   = 0
        while True:
            try:
                self.db[db_record['_id']] = db_record
                if count_connect_attempt > 0 or count_reset_attempt > 0:
                    printInfo(f'Connection to {self.db_name} re-established.')
                break
            except couchdb.http.ResourceConflict:
                if 'labeling' in db_record:
                    throwError(f"Could not save {db_record['labeling']['annotations']['name']['text']} into {self.db_name}.  Redo the read and try again.")
                else:
                    throwError(f"Could not save doc into {self.db_name}. Redo the read and try again.")
            except:
                count_connect_attempt += 1
                if count_connect_attempt == 1:
                    print()
                elif count_connect_attempt == 12:
                    throwError(f'Could not save doc into {self.db_name}')
                printWarning(f'Disconnected from {self.db_name} during write. Trying again in {DB_RECONNECTION_SLEEP} seconds [attempt #{count_connect_attempt}]...')
                time.sleep(DB_RECONNECTION_SLEEP)


    def count_number_of_records(self):
        response = requests.get(f'{self.couchdb_db_url}/product-recommendation/_design/dyson/_view/dbStats?reduce=true&group=true&keys=%5B%22{self.db_name}%22%5D')
        if response.status_code == 200:
            try:
                db_stats = json.loads(response.text)
                self.nb_records = db_stats['rows'][0]['value']['total']
            except:
                printWarning(f'Still updating record count for {self.db_name}.')
        else:
            throwError(f'Cannot get number of records for {self.db_name}.')

        printInfo(f'{self.nb_records} items in {self.db_name}')

        return self.nb_records

    def get_ontology(self):
        # while true ; do kubectl --context playground -n maestro-v2-dev port-forward services/dyson 9005 ; done
        response = requests.get(f'{self.dyson_url}/productDatabases/{self.db_name}/ontology')
        if response.status_code == 200:
            self.ontology = response.text
            matches = re.search(': "(.*)-1"\,', self.ontology)
            if bool(matches):
                printWarning(f"Duplicate leaf name found: {matches.group(1)}")
        else:
            throwError(f'Ontology for {self.db_name} not found.')


    def update_ontology(self):
        # updated_ontology = ''.join(self.base_ontology)
        response = requests.get(f'{self.dyson_url}/productDatabases/{self.db_name}/ontology')
        if response.status_code == 200:
            updated_ontology = response.text
            original_revison = json.loads(updated_ontology)['revision']
            uri_db_name = to_camel_case(self.db_name)
            updated_ontology, nb_changes = re.subn('http://automat.ai/\w+/', f'http://automat.ai/{uri_db_name}/', updated_ontology)
            updated_ontology, base_count = re.subn('http://automat.ai/\w+/ProductCategory', f'http://automat.ai/base/ProductCategory', updated_ontology)
            if not base_count == 1:
                throwError(f'ProductCategory URI not found in {self.db_name}.  It is mandatory.')
        else:
            throwError(f'Cannot get the ontology for {self.db_name}.')
        # {
        #     "rev": "9285436391ed9024879417622ffe5d9d48e36081",
        #     "ontologyContent":  ...,
        #     "userInfo": "Copied from blablabla",
        #     "migration": null
        # }
        bare_ontology = json.loads(updated_ontology)['ontology']
        post_json = {"rev": original_revison, "ontologyContent": bare_ontology, "userInfo": "URI Alignment", "migration": None}
        response = requests.post(f'{self.dyson_url}/productDatabases/{self.db_name}/ontology', json=post_json)
        if response.status_code == 200:
            printInfo(f'Ontology for {self.db_name} updated [{nb_changes} changes].')
        else:
            throwError(f'Cannot update the ontology for {self.db_name}.')

    def check_ontology(self):
        matches = re.findall(r'([\w/\.:]*)-1', self.ontology)
        if matches == None or len(matches) == 0:
            printInfo(f'No duplicate leaves found in {self.db_name}.')
            return
        for match in matches:
            printWarning('Found duplicate leaf - ' + match + f' in {self.db_name}')

    def set_base_ontology(self):
        self.base_ontology = self.ontology

    def compare_ontology(self, other_ontology = None):

        def simplify_uri(ontology):
            for key in ontology:
                ontology[key] = ontology[key].split('/')[-1]
            return ontology
        
        current_mapping = get_name_url_mapping(json.loads(self.ontology), {})
        current_mapping = simplify_uri(current_mapping)

        if other_ontology == None:
            other_mapping = get_name_url_mapping(json.loads(self.base_ontology), {})
            other_mapping = simplify_uri(other_mapping)
            diff = DeepDiff(current_mapping, other_mapping)
            other_db_name = 'BASE ONTOLOGY'
        else:
            other_mapping = get_name_url_mapping(json.loads(other_ontology), {})
            other_mapping = simplify_uri(other_mapping)
            diff = DeepDiff(current_mapping, other_mapping)
            other_db_name = 'specified ontology'
        
        if len(diff) == 0:
            printInfo(f'No diffrences in the ontology detected between {self.db_name} and {other_db_name}.')
        else:
            throwError(f'Ontologies do not match: ' + str(diff))

        # Make sure all URI use the ontology db 
        matches = re.findall('http://automat.ai/(\w+)/', self.ontology)
        current_db_name = self.db_name
        self.set_db_name(Production_Step.ONTOLOGY)
        uri_diff = set(matches) - set(['base', to_camel_case(self.db_name)])
        self.db_name = current_db_name
        if len(uri_diff) > 0:
            throwError(f'Unexpected URI(s) [{uri_diff}] found in {self.db_name}.')

    def migrate_data(self, source_db):
        # 1. Get source data in text -> convert to JSON
        # 2. Remove all tags and approvedVersion from source data
        # 3. Copy over the base ontology into the source data
        # 4. Upload new database to newly created products db
        response = requests.get(f'{self.dyson_url}/productDatabases/{source_db}/dump')
        if response.status_code == 200:
            time_start = time.perf_counter()
            db_content = json.loads(response.content)
            # db_content['id']   = self.db_name
            # db_content['name'] = self.db_name
            nb_original_records = len(db_content['products'])
            for product in db_content['products']:
                # printProgressBar(idx, nb_original_records, startTime=time_start)
                if not 'labeling' in product:
                    continue
                for annotation in product['labeling']['annotations']:
                    if 'tags' in product['labeling']['annotations'][annotation]:
                        product['labeling']['annotations'][annotation]['tags'] = []
                    if 'approvedVersion' in product['labeling']['annotations'][annotation]:
                        del product['labeling']['annotations'][annotation]['approvedVersion']
            db_content['ontology'] = json.loads(self.base_ontology)['ontology']
            response = requests.post(f'{self.dyson_url}/productDatabases/{self.db_name}/dump?overwrite=true', json=db_content)
            if response.status_code == 200:
                printInfo(f'{self.db_name} updated with {nb_original_records} products from {source_db}')
            else:
                printWarning(str(response.content))
                throwError(f'Could not create {self.db_name} using data from {source_db}.')
        else:
            throwError(f'Could not get data from {source_db}.')

        printInfo('Migration latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')
        return nb_original_records

    def map_products_to_visenze(self):
        local_count = 0
        time_start = time.perf_counter()
        printProgressBar(local_count, self.nb_records, startTime=time_start)
        nb_docs_skip = 0
        while True:
            docs = self.get_db_records(nb_docs_skip)
            record_count = 0
            for db_record in docs:
                if not 'labeling' in db_record:
                    continue
                mapping_labels = {}
                for tag_category in db_record['labeling']['annotations']:
                    if tag_category.startswith('vi_'):
                        mapping_labels[tag_category[3:]] = db_record['labeling']['annotations'][tag_category]['text']

                session = requests.Session()
                response = session.post('http://127.0.0.1:443/post/getAllViSenzeMapping',
                                            data={"visenze_categories": json.dumps(mapping_labels), 
                                                "ontology": self.ontology,
                                                "colour": "GREEN"})
                
                tagging_results = json.loads(response.text)
                is_update = False
                for tag_category in tagging_results:                
                    diff = DeepDiff(tagging_results[tag_category], db_record['labeling']['annotations']['vi_' + tag_category]['tags'])
                    if len(tagging_results[tag_category]) > 0 and len(diff) > 0:
                        is_update = True                
                        db_record['labeling']['annotations']['vi_' + tag_category]['tags'] += tagging_results[tag_category]
                record_count += 1
                local_count  += 1
                printProgressBar(local_count, self.nb_records, startTime=time_start)
                if is_update:
                    try:
                        self.save_record(db_record)
                    except:
                        # Reset the counter and read
                        local_count -= record_count
                        nb_docs_skip -= LIMIT_DOCS_PER_QUERY
                        break
            nb_docs_skip += LIMIT_DOCS_PER_QUERY
            if record_count == 0:
                break

        print()
        printInfo('ViSenze mapping latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')

    def fix_description(self):
        local_count = 0
        time_start = time.perf_counter()
        printProgressBar(local_count, self.nb_records, startTime=time_start)
        # progress_bar = tqdm.tqdm(total=self.nb_records)
        nb_docs_skip = 0
        while True:
            docs = self.get_db_records(nb_docs_skip)
            record_count = 0
            for db_record in docs:
                if not 'labeling' in db_record:
                    continue
                is_update = False

                description = db_record['labeling']['annotations']['description']['text']

                # Replace / for Rasa NLU
                description, nb_dashes = re.subn('(?<!\s)/(?!\s)', ' / ', description)

                # Add spaces before and after / for Rasa NLU
                description, nb_slashes = re.subn('(?<!\s)/(?!\s)', ' / ', description)

                is_update = nb_dashes > 0 or nb_slashes > 0
                record_count += 1
                local_count  += 1
                printProgressBar(local_count, self.nb_records, startTime=time_start)
                # progress_bar.update(1)
                if is_update:
                    db_record['labeling']['annotations']['description']['text'] = description
                    try:
                        self.save_record(db_record)
                    except:
                        # Reset the counter and read
                        local_count -= record_count
                        nb_docs_skip -= LIMIT_DOCS_PER_QUERY
                        break
            nb_docs_skip += LIMIT_DOCS_PER_QUERY
            if record_count == 0:
                break
        
        # progress_bar.close()
        print()
        printInfo('Description fix latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')


    def collect_existing_tags(self, is_force_update = True):        
        if not is_force_update and self.is_use_cache and os.path.isfile(self.PRODUCTS_CACHE_FILE_NAME):
            self.tagged_products = json.load(open(self.PRODUCTS_CACHE_FILE_NAME, 'r'))
            count_tagged = len(self.tagged_products)
        else:
            printInfo(f'Checking {self.db_name} for tagged products...')
            local_count  = 0
            count_tagged = 0
            nb_docs_skip = 0
            self.count_number_of_records()
            time_start = time.perf_counter()
            printProgressBar(local_count, self.nb_records, startTime=time_start)
            # progress_bar = tqdm.tqdm(total=self.nb_records)
            self.tagged_products = {}
            while True:
                docs = self.get_db_records(nb_docs_skip)
                record_count = 0
                for db_record in docs:
                    if not 'labeling' in db_record:
                        continue
                    record_count += 1
                    local_count  += 1
                    printProgressBar(local_count, self.nb_records, startTime=time_start)
                    # progress_bar.update(1)

                    product_name = db_record['labeling']['annotations']['name']['text']

                    # Check for tagging information
                    if len(db_record['labeling']['annotations']['name']['tags']) == 0 and len(db_record['labeling']['annotations']['description']['tags']) == 0:
                        continue
                    
                    count_tagged += 1

                    if product_name in self.tagged_products:
                        name_diff = DeepDiff(self.tagged_products[product_name]['name']['tags'], db_record['labeling']['annotations']['name']['tags'])
                        description_diff = DeepDiff(self.tagged_products[product_name]['description']['tags'], db_record['labeling']['annotations']['description']['tags'])
                        if len(name_diff) > 0 and len(description_diff) > 0 and not db_record['labeling']['annotations']['description']['text'] == self.tagged_products['description']['text']:
                            db_record['labeling']['annotations']['name']['tags'] = self.tagged_products['name']['tags']
                            db_record['labeling']['annotations']['description']['tags'] = self.tagged_products['description']['tags']
                            try:
                                self.save_record(db_record)
                            except:
                                # Reset the counter and read
                                local_count -= record_count
                                nb_docs_skip -= LIMIT_DOCS_PER_QUERY
                                break
                    else:
                        self.tagged_products[product_name] = {
                            'id' : db_record['_id'],
                            'name': db_record['labeling']['annotations']['name'], 
                            'description': db_record['labeling']['annotations']['description']}

                nb_docs_skip += LIMIT_DOCS_PER_QUERY
                if record_count == 0:
                    break

            # progress_bar.close()
            json.dump(self.tagged_products, open(self.PRODUCTS_CACHE_FILE_NAME, 'w'))

            self.nb_tagged_products = count_tagged

    def tag_products(self, tag_target=None, llm_type='GPT4'):
        # printInfo(f'\nGenerating tags for {tag_target} products...')
        # response = requests.get(f'{self.dyson_url}/productDatabases/{self.db_name}/dump')
        # if response.status_code == 200:
        #     time_start = time.perf_counter()
        #     db_content = json.loads(response.content)

        # time_start = time.perf_counter()
        # count_tagged = len(self.tagged_products)
        # if count_tagged >= tag_target:
        #     printInfo(f'{count_tagged} products tagged in {self.db_name}')
        #     return
        # printProgressBar(count_tagged, tag_target, startTime=time_start, startOffset=self.nb_tagged_products)
        # count_to_tag = 0
        # newly_tagged_products = {}
        # for product in db_content:
        #     is_tagged = False
        #     for tagged_product in self.tagged_products:
        #         if tagged_product['id'] == product['_id']:
        #             is_tagged = True
        #             break
        #     if not is_tagged:
        #         print('Tag IT')
        #         count_to_tag += 1
        #         newly_tagged_products[product['name']] = product
        #     if count_tagged + count_to_tag == tag_target:
        #         break
        print()
        printInfo(f'Updating {tag_target} products...')
        api_map = {'name': 'title_tags', 'description': 'description_tags'}
        time_start = time.perf_counter()
        count_tagged = len(self.tagged_products)
        printProgressBar(count_tagged, tag_target, startTime=time_start, startOffset=self.nb_tagged_products)
        nb_docs_skip = 0
        while True:
            docs = self.get_db_records(nb_docs_skip)
            record_count = 0
            for db_record in docs:
                if not 'labeling' in db_record:
                    continue
                
                record_count += 1

                product_name = db_record['labeling']['annotations']['name']['text']
                product_description = db_record['labeling']['annotations']['description']['text']
                if product_name in self.tagged_products:
                    continue

                form_data = {'title': product_name, 'description': product_description, 
                             'ontology': self.ontology, 'colour': 'BLUE',
                             'llm': llm_type, 'products': [], 'delay': 0}

                session = requests.Session()
                response = session.post('http://127.0.0.1:443/post/getTags', data=form_data)
                
                tagging_results = json.loads(response.text)
                is_update = False
                for label_category in ['name', 'description']:                
                    diff = DeepDiff(tagging_results[api_map[label_category]], db_record['labeling']['annotations'][label_category]['tags'])
                    if len(tagging_results[api_map[label_category]]) > 0 and len(diff) > 0:
                        is_update = True                
                        db_record['labeling']['annotations'][label_category]['tags'] += tagging_results[api_map[label_category]]
                if is_update:
                    try:
                        try:
                            self.save_record(db_record)
                        except:
                            # Reset the counter and read
                            nb_docs_skip -= LIMIT_DOCS_PER_QUERY
                            break
                        count_tagged += 1
                        # If write sucessful, update progress bar and cache
                        printProgressBar(count_tagged, tag_target, startTime=time_start)
                        self.tagged_products[product_name] = {
                            'name': db_record['labeling']['annotations']['name'], 
                            'description': db_record['labeling']['annotations']['description']}
                    except:
                        json.dump(self.tagged_products, open(self.PRODUCTS_CACHE_FILE_NAME, 'w'))
                        print()
                        throwError(f'Couchdb [{self.db_name}] write failed')

                if count_tagged == tag_target:
                    print()
                    printInfo(f'LLM tagging [{count_tagged} items tagged] latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')
                    return
            nb_docs_skip += LIMIT_DOCS_PER_QUERY
            if record_count == 0:
                break

        if count_tagged < tag_target:
            print()
        printInfo(f'LLM tagging [{count_tagged} items tagged] latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')

    def correct_tags(self, wrong_tag_mapping, is_fix = True):
        local_count  = 0
        count_tagged_products = 0
        count_fixed_products  = 0

        nb_docs_skip = 0
        time_start = time.perf_counter()
        printProgressBar(local_count, self.nb_records, startTime=time_start)
        while True:
            docs = self.get_db_records(nb_docs_skip)
            record_count = 0
            for db_record in docs:
                local_count += 1
                if not 'labeling' in db_record:
                    continue
                
                record_count += 1
                printProgressBar(local_count, self.nb_records, startTime=time_start)
                # Nothing to see here... move along
                if len(db_record['labeling']['annotations']['name']['tags']) == 0 and len(db_record['labeling']['annotations']['description']['tags']) == 0:
                    continue
                count_tagged_products += 1
                print('\n>> ' + db_record['labeling']['annotations']['name']['text'])
                is_changed = False
                for field in ['name', 'description']:
                    print('\n\t' + field.upper())

                    content = db_record['labeling']['annotations'][field]

                    is_wrong, content['tags'] = remove_wrong_tags(content['text'], content['tags'], wrong_tag_mapping)

                    is_punctuation, content['tags'] = fix_punctuation(content['text'], content['tags'])

                    is_embedded, content['tags'] = fix_embedded_tags(content['text'], content['tags'])                    

                    is_duplicate, content['tags'] = remove_duplicate_tags(content['text'], content['tags'])

                    is_changed = is_wrong | is_punctuation | is_embedded | is_duplicate | is_changed
                print()                
                if is_changed:
                    print('UPDATING: ' + db_record['labeling']['annotations']['name']['text'])
                    if is_fix:
                        try:
                            self.save_record(db_record)
                        except:
                            # Reset the counter and read
                            local_count -= record_count
                            count_tagged_products -= 1
                            nb_docs_skip -= LIMIT_DOCS_PER_QUERY
                            break
                        count_fixed_products += 1
            nb_docs_skip += LIMIT_DOCS_PER_QUERY
            if record_count == 0:
                break

        print(f'Total {local_count} / LLM Tagged {count_tagged_products} / Fixed {count_fixed_products}')

        return count_fixed_products

    def validate_clu(self):
        self.db_name = 'Saks-Jeans-LLM-fix'
        try:
            count_clu_train = 0
            response = requests.post(f'{self.dyson_url}/productDatabases/{self.db_name}/train?force=true')
            if response.status_code == 200:
                process_id = int(response.content)
                is_in_progress = True
                while is_in_progress:
                    response = requests.get(f'{self.dyson_url}/productDatabaseProcesses/{process_id}')
                    is_in_progress = json.loads(response.content)['completed'] == False
                    time.sleep(60) # wait a minute before asking again
                    count_clu_train += 1
                    # Wait max 1 hr for training to finish
                    if count_clu_train == 60:
                        raise Exception()
                pass
            else:
                raise Exception()
        except:
            throwError(f'Could not validate {self.db_name} for CLU usage')

    def collect_representations(self):
        self.representations = {}

        for product_name in self.tagged_products:
            for field in ['name', 'description']:
                content = self.tagged_products[product_name][field]['text']
                tags    = self.tagged_products[product_name][field]['tags']
                for tag in tags:
                    label = get_label_suffix(tag['label'])
                    if not label in self.representations:
                        self.representations[label] = set()
                    self.representations[label].add(content[tag['start']:tag['end']].lower())

    def set_tag_usage(self):
        self.collect_existing_tags()
        self.collect_representations()

        with open(f'_stats_{self.category}_products.csv', 'w') as stats_file:
            self.description_tag_density = {}
            for product in self.tagged_products:
                nb_of_tokens = len(self.tagged_products[product]['description']['text'].split())
                nb_of_tags   = len(self.tagged_products[product]['description']['tags'])
                self.description_tag_density[product] = {
                    'nb_tokens': nb_of_tokens, 
                    'nb_tags': nb_of_tags
                    }
                stats_file.write(f'{product},{nb_of_tokens},{nb_of_tags}\n')
