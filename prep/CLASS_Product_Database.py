import binascii
import copy
import couchdb
import datetime
import json
import numpy
import os
import re
import requests
import sys
import time
import traceback
import zipfile
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
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", startTime = None, iterationTimes = []):
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
        time_remaining    = '?'
        average_time_left = '?'
        # Remaining time can only be estimated after 20% of the task has been done
        if total == iteration:
            time_remaining = timedelta(seconds=0)
            average_time_left = time_remaining
        else:
            if (iteration/total) > 0.2:
                time_remaining = timedelta(seconds=int((time.perf_counter() - startTime)*(total-iteration)/iteration))
            if len(iterationTimes) > 10:
                average_time_left = timedelta(seconds=int(numpy.average(iterationTimes[-10:])*(total-iteration)))
        suffix = f'ETA: {time_remaining}|{average_time_left}'

    print(f'\r{prefix} |{bar}| {percent}% [{iteration}/{total}] {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# From https://stackoverflow.com/questions/60978672/python-string-to-camelcase
def to_db_uri(db_name, category):
    if len(db_name) == 0:
        return db_name
    db_name = db_name.replace("-", " ").replace("_", " ")
    parts = db_name.split()
    for idx, part in enumerate(parts):
        if part == category:
            continue
        parts[idx] = part.title()
    
    return ''.join(parts)

def get_complex_name(name, description_text):
    description_crc = binascii.crc32(description_text.encode('utf8'))
    return name + ' ' + str(description_crc)

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

RECONNECTION_SLEEP = 10 # in seconds
NB_RETRY_ATTEMPTS      = 10

MONITOR_SLEEP    = 30 # in seconds
MONITOR_ATTEMPT  = 60

class Product_Database():
    def __init__(self, category) -> None:
        self.db_name     = None
        self.is_db_fresh = False
        self.db_content  = None
        self.db_step     = None
        
        self.category = category

        self.tagged_products = {}
        self.couchdb_db_url = 'http://admin:admin@127.0.0.1:5984'
        self.dyson_url      = 'http://localhost:9005'
        self.tagging_url    = 'http://127.0.0.1:443'

        self.nb_records = 0
        self.nb_tagged_products = 0

        self.is_verbose = True

        self.wrong_tag_mapping = {}
        if os.path.isfile('./prep/wrong_labels.json'):
            self.wrong_tag_mapping = json.load(open('./prep/wrong_labels.json', 'r'))
        self.debug_products = []
        if os.path.isfile('./prep/_debug_product_names.json'):
            self.debug_products = json.load(open('./prep/_debug_product_names.json', 'r'))


    def destroy(self):
        printInfo(f'Deleting {self.db_name} database.')
        count_delete = 0 
        while count_delete < NB_RETRY_ATTEMPTS:
            count_delete += 1
            try:
                response = requests.delete(f'{self.dyson_url}/productDatabases/{self.db_name}')
                if response.status_code == 200:
                    printInfo(f'{self.db_name} deleted.')
                    return
                else:
                    printWarning(f'Unable to delete {self.db_name}. Trying again [attempt #{count_delete}].')
            except Exception:
                printWarning(f'Unable to delete {self.db_name}. Trying again [attempt #{count_delete}].')
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
        self.db_step = step_enum
        self.db_name = 'Saks-!CATEGORY!-!#!-!STEP_NAME!'.replace('!CATEGORY!', self.category).replace('!#!', str(step_enum.value)).replace('!STEP_NAME!', STEP_SUFFIX_MAPPING[step_enum])

    def get_db_name(self):
        return self.db_name

    def set_nb_records(self, overwrite_nb_records):
        if not overwrite_nb_records == None:
            self.nb_records = overwrite_nb_records
            printInfo(f'{self.nb_records} items in {self.db_name} [overwrite]')
    
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
                elif count_connect_attempt == NB_RETRY_ATTEMPTS:
                    throwError(f'Could not save doc into {self.db_name}')
                printWarning(f'Disconnected from {self.db_name} during write. Trying again in {RECONNECTION_SLEEP} seconds [attempt #{count_connect_attempt}]...')
                time.sleep(RECONNECTION_SLEEP)


    def helper_requests(self, request_type, request_url, json_post_data=None, expected_nb_records=None, process_description=''):
        count_negative_response = 1
        is_db_exist = True
        while True: 
            try:
                if request_type == 'get':
                    response = requests.get(request_url)
                    if response.status_code == 200:
                        return response
                    elif response.status_code == 404:
                        if response.reason == 'Not Found':
                            is_db_exist = False
                            break
                    printWarning(f'Process failed.  Trying again in {RECONNECTION_SLEEP} seconds [attempt #{count_negative_response}]...')
                else:
                    response = requests.post(request_url, json=json_post_data)
                    if response.status_code == 200:
                        process_response = self.monitor_process(response, process_description)
                        response_content = json.loads(process_response.content)
                        if response_content['completed']:
                            actual_nb_records = self.count_number_of_records()
                            if expected_nb_records == None:
                                return response
                            if actual_nb_records == expected_nb_records:
                                return response
                            else:
                                printWarning(f'Expected {expected_nb_records} in db but found {actual_nb_records}.  Retrying.')
                    elif response.status_code == 404:
                        if response.reason == 'Not Found':
                            is_db_exist = False
                            break

            except:
                printWarning(f'Process failed.  Trying again in {RECONNECTION_SLEEP} seconds [attempt #{count_negative_response}]...')

            count_negative_response += 1

            if count_negative_response == NB_RETRY_ATTEMPTS:
                throwError(f'Cannot connect to server')
            
            time.sleep(RECONNECTION_SLEEP)

        if not is_db_exist:
            throwError(f'Database {self.db_name} does not exist.')

    def count_number_of_records(self):
        self.nb_records = None
        count_negative_response = 0
        while True: 
            response = self.helper_requests('get', f'{self.couchdb_db_url}/product-recommendation/_design/dyson/_view/dbStats?reduce=true&group=true&keys=%5B%22{self.db_name}%22%5D')
            try:
                db_stats = json.loads(response.text)
                self.nb_records = db_stats['rows'][0]['value']['total']
                break
            except:
                printWarning(f'Still updating record count for {self.db_name}.')

            count_negative_response += 1

            if count_negative_response == 2:
                throwError(f'Cannot get number of records for {self.db_name}.')

            time.sleep(RECONNECTION_SLEEP)

        printInfo(f'{self.nb_records} items in {self.db_name}')

        return self.nb_records

    def get_ontology(self):
        # while true ; do kubectl --context playground -n maestro-v2-dev port-forward services/dyson 9005 ; done
        self.ontology = None
        response = self.helper_requests('get', f'{self.dyson_url}/productDatabases/{self.db_name}/ontology')
        self.ontology = response.text
        matches = re.search(': "(.*)-1"\,', self.ontology)
        if bool(matches):
            printWarning(f"Duplicate leaf name found: {matches.group(1)}")

    def update_ontology(self, is_rebase = False):
        response = self.helper_requests('get', f'{self.dyson_url}/productDatabases/{self.db_name}/ontology')
        if response.status_code == 200:
            db_ontology = response.text
            original_revison = json.loads(db_ontology)['revision']
            if is_rebase:
                db_ontology = ''.join(self.base_ontology)
            else:                
                uri_db_name = to_db_uri(self.db_name, self.category)
                db_ontology, nb_changes = re.subn('http://automat.ai/\w+/', f'http://automat.ai/{uri_db_name}/', db_ontology)
                db_ontology, base_count = re.subn('http://automat.ai/\w+/ProductCategory', f'http://automat.ai/base/ProductCategory', db_ontology)
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
        bare_ontology = json.loads(db_ontology)['ontology']
        post_json = {"rev": original_revison, "ontologyContent": bare_ontology, "userInfo": "URI Alignment", "migration": None}

        response = requests.post(f'{self.dyson_url}/productDatabases/{self.db_name}/ontology', json=post_json)
        if response.status_code == 200:
            if is_rebase:
                printInfo(f'Ontology for {self.db_name} rebased.')
            else:
                printInfo(f'Ontology for {self.db_name} updated [{nb_changes} changes].')
            self.get_ontology()
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
        self.base_uri      = to_db_uri(self.db_name, self.category)

    def compare_ontology(self, is_rebase = False):

        def simplify_uri(ontology):
            for key in ontology:
                ontology[key] = ontology[key].split('/')[-1]
            return ontology
        
        self.current_mapping = get_name_url_mapping(json.loads(self.ontology), {})
        self.current_mapping = simplify_uri(self.current_mapping)

        other_mapping = get_name_url_mapping(json.loads(self.base_ontology), {})
        other_mapping = simplify_uri(other_mapping)
        diff = DeepDiff(self.current_mapping, other_mapping)
        other_db_name = 'BASE ONTOLOGY'
        
        if len(diff) == 0:
            printInfo(f'No diffrences in the ontology detected between {self.db_name} and {other_db_name}.')
        else:
            if is_rebase:
                printInfo(f'{str(diff)} changed in ontology of {self.db_name}.')
                throwError()
            else:
                throwError(f'Ontologies do not match: ' + str(diff))

        # Make sure all URI use the ontology db 
        matches = re.findall('http://automat.ai/(\w+)/', self.ontology)
        matches = [x.lower() for x in matches]
        uri_diff = set(matches) - set(['base', self.base_uri.lower()])
        if len(uri_diff) > 0:
            throwError(f'Unexpected URI(s) [{uri_diff}] found in {self.db_name}.')

    def migrate_data(self, source_db):
        # 1. Get source data in text -> convert to JSON
        # 2. Remove all tags and approvedVersion from source data
        # 3. Copy over the base ontology into the source data
        # 4. Upload new database to newly created products db
        printInfo(f'Downloading data from {source_db}.')
        response = self.helper_requests('get', f'{self.dyson_url}/productDatabases/{source_db}/dump')
        printInfo(f'Data retrieved from {source_db}.')
        time_start = time.perf_counter()
        db_content = json.loads(response.content)
        # db_content['id']   = self.db_name
        # db_content['name'] = self.db_name
        nb_original_records = len(db_content['products'])
        for product in db_content['products']:
            if 'labelingApproval' in product:
                product['labelingApproval'] = 'Never Approved'
            if not 'labeling' in product:
                continue
            for annotation in product['labeling']['annotations']:
                if 'tags' in product['labeling']['annotations'][annotation]:
                    product['labeling']['annotations'][annotation]['tags'] = []
                if 'approvedVersion' in product['labeling']['annotations'][annotation]:
                    del product['labeling']['annotations'][annotation]['approvedVersion']
        db_content['ontology'] = json.loads(self.base_ontology)['ontology']
        self.destroy()
        printInfo(f'Uploading data to {self.db_name}.')
        response = self.helper_requests('post', f'{self.dyson_url}/productDatabases/{self.db_name}/dump?overwrite=true', db_content, nb_original_records, 'Data migration')
        if response.status_code == 200:
            printInfo(f'{self.db_name} updated with {nb_original_records} products from {source_db}')
        else:
            printWarning(str(response.content))
            throwError(f'Could not create {self.db_name} using data from {source_db}.')

        printInfo('Migration latency: ' +  str(round(time.perf_counter() - time_start, 3)) + ' seconds.')
        return nb_original_records
    
    def update_db_records(self, func_update, func_params=[], count_update_target = None, is_show_progress=False, process_description=''):
        time_start = time.perf_counter()

        if self.db_content == None:
            printInfo(f'Downloading {self.db_name}...')
            response = self.helper_requests('get', f'{self.dyson_url}/productDatabases/{self.db_name}/dump')
            printInfo(f'{self.db_name} downloaded in {round(time.perf_counter() - time_start, 3)} seconds.')
            self.db_content = json.loads(response.content)

        if count_update_target == None:
            end_count = self.nb_records
        else:
            end_count = count_update_target
        if not len(self.db_content['products']) == self.nb_records:
            throwError(f'Actual number of products [{len(self.db_content["products"])}] is different from expected [{self.nb_records}].')

        time_start = time.perf_counter()
        count_updated_products = 0
        iteration_times = []
        for idx, product in enumerate(self.db_content['products']):
            time_iteration_start = time.perf_counter()
            if not 'labeling' in product:
                continue

            is_update = False            
            if len(func_params) == 0:
                is_update = eval(f'{func_update}(product)')
            else:
                is_update = eval(f'{func_update}(product,{",".join(func_params)})')

            if is_update:
                count_updated_products += 1
            
            if is_show_progress:
                iteration_times.append(time.perf_counter() - time_iteration_start)
                printProgressBar(idx + 1, end_count, startTime=time_start, iterationTimes=iteration_times)

            if not count_update_target == None and self.nb_tagged_products == count_update_target:
                break

        if count_updated_products > 0:
            printInfo(f'{count_updated_products} products updated -> recreating {self.db_name}...')
            json.dump(self.db_content, open(f'./prep/_upload_{self.db_name}.json', 'w'))
            with zipfile.ZipFile(f'./prep/backup/_upload_{self.db_name}_{datetime.datetime.now()}.zip', 'w') as myzip:
                myzip.write(f'./prep/_upload_{self.db_name}.json')
            os.remove(f'./prep/_upload_{self.db_name}.json') 
            # self.destroy()
            self.helper_requests('post', f'{self.dyson_url}/productDatabases/{self.db_name}/dump?overwrite=true', self.db_content, self.nb_records, process_description)
            printInfo(f'{self.db_name} updated successfully.')

        return count_updated_products

    def map_product_tags(self, product):
        mapping_labels = {}
        for tag_category in product['labeling']['annotations']:
            if tag_category.startswith('vi_'):
                mapping_labels[tag_category[3:]] = product['labeling']['annotations'][tag_category]['text']

        session = requests.Session()
        response = session.post(f'{self.tagging_url}/post/getAllViSenzeMapping',
                                    data={"visenze_categories": json.dumps(mapping_labels), 
                                        "ontology": self.ontology,
                                        "colour": "GREEN"})
        
        tagging_results = json.loads(response.text)
        is_update = False
        for tag_category in tagging_results:                
            diff = DeepDiff(tagging_results[tag_category], product['labeling']['annotations']['vi_' + tag_category]['tags'])
            if len(tagging_results[tag_category]) > 0 and len(diff) > 0:
                is_update = True                
                product['labeling']['annotations']['vi_' + tag_category]['tags'] += tagging_results[tag_category]

        return is_update

    def map_to_visense(self):
        time_start = time.perf_counter()
        self.update_db_records('self.map_product_tags', count_update_target=None, is_show_progress=True, process_description='Mapping ViSenze taxonomy')
        printInfo(f'ViSenze mapping latency: {round(time.perf_counter() - time_start, 3)} seconds.')
    

    def fix_product_description(self, product):
        description = product['labeling']['annotations']['description']['text']

        # Might have negative effect: e.g. front-zip => front - zip might be interrupted as 2 words
        # # Add spaces before and after - for Rasa NLU
        # description, nb_dashes = re.subn(r'(?<!\s)-(?!\s)', r' - ', description)

        # Add spaces before and after / for Rasa NLU
        description, nb_slashes = re.subn(r'(?<!\s)/(?!\s)', r' / ', description)

        # Add spaces before and after / for Rasa NLU
        description, nb_percent = re.subn(r'%(?!\s)', r'% ', description)

        # Add 2 spaces after . for Rasa NLU except at the end and for acronyms
        description, nb_periods = re.subn(r'(?<!\b[A-Z]\.)\.(?=\S)', r'.  ', description)

        product['labeling']['annotations']['description']['text'] = description

        is_update = nb_slashes > 0 or nb_periods > 0 or nb_percent > 0

        return is_update

    def fix_descriptions(self):
        time_start = time.perf_counter()
        self.update_db_records('self.fix_product_description', process_description='Fixing product descriptions')
        printInfo(f'Fix descriptions latency: {round(time.perf_counter() - time_start, 3)} seconds.')

    def collect_product_tags(self, product):
        product_name = product['labeling']['annotations']['name']['text']
        product_description = product['labeling']['annotations']['description']['text']

        # Check for tagging information
        if len(product['labeling']['annotations']['name']['tags']) == 0 and len(product['labeling']['annotations']['description']['tags']) == 0:
            return False
        
        cache_name = get_complex_name(product_name, product_description)

        if not cache_name in self.tagged_products:
            self.tagged_products[cache_name] = {
                'name': product['labeling']['annotations']['name'], 
                'description': product['labeling']['annotations']['description']}        

        return False

    def collect_existing_tags(self):
        self.db_content      = None 
        self.tagged_products = {}
        printInfo(f'Checking {self.db_name} for tagged products...')
        time_start = time.perf_counter()
        self.update_db_records('self.collect_product_tags')
        printInfo(f'Tag collection latency: {round(time.perf_counter() - time_start, 3)} seconds.')


    def tag_product(self, product, llm_type):
        API_MAP = {'name': 'title_tags', 'description': 'description_tags'}    
        product_name = product['labeling']['annotations']['name']['text']
        product_description = product['labeling']['annotations']['description']['text']

        cache_name = get_complex_name(product_name, product_description)

        self.is_verbose = False
        if product_name in self.debug_products:
            self.is_verbose = True
            pass

        is_force_update = False
        if llm_type == 'Explicit':
            is_force_update = True

        if product['labelingApproval'] == 'Approved':
            # Do not overwrite existing tags
            if not cache_name in self.llm_tags_cache:
                self.llm_tags_cache[cache_name] = {
                    'name' : product['labeling']['annotations']['name'],
                    'description' : product['labeling']['annotations']['description']
                }
            if not is_force_update:
                self.nb_tagged_products += 1
                return False
        
        is_new_product = False
        if cache_name in self.llm_tags_cache and not is_force_update:
            tagging_results = {}
            tagging_results['title_tags'] = self.llm_tags_cache[cache_name]['name']['tags']
            tagging_results['description_tags'] = self.llm_tags_cache[cache_name]['description']['tags']
        else:
            # In the FIX step, update tags to products which were already tagged by LLM
            if self.db_step == Production_Step.FIX:
                if not cache_name in self.llm_tags_cache:
                    return False
            # Remove COLOUR and PRODUCT CATEGORY from ontology
            reduced_ontology = copy.deepcopy(self.ontology)
            reduced_ontology = json.loads(reduced_ontology)
            for idx, attribute in enumerate(reduced_ontology['ontology']['product']):
                if attribute['label'].endswith('ProductCategory'):
                    del reduced_ontology['ontology']['product'][idx]
                elif attribute['label'].endswith('Color'):
                    del reduced_ontology['ontology']['product'][idx]
            reduced_ontology = json.dumps(reduced_ontology)
            is_new_product = True
            form_data = {'title': product_name, 'description': product_description, 
                            'ontology': reduced_ontology, 'colour': 'BLUE',
                            'llm': llm_type, 'products': [], 'delay': 0}

            session = requests.Session()
            response = session.post(f'{self.tagging_url}/post/getTags', data=form_data)
            
            tagging_results = json.loads(response.text)

            if 'error' in tagging_results:
                throwError(tagging_results['error'])

        ### Ensure Uri in the tags
        tagging_results = json.dumps(tagging_results)
        tagging_results = re.sub('http://automat.ai/\w+/', f'http://automat.ai/{self.base_uri}/', tagging_results)
        tagging_results = json.loads(tagging_results)

        self.nb_tagged_products += 1

        is_update = False
        for label_category in ['name', 'description']:
            try:
                for tag in tagging_results[API_MAP[label_category]]:
                    del tag['text']
                    del tag['location']
            except:
                pass
            diff = DeepDiff(tagging_results[API_MAP[label_category]], product['labeling']['annotations'][label_category]['tags'], ignore_order=True)
            if len(tagging_results[API_MAP[label_category]]) > 0 and len(diff) > 0:
                product['labeling']['annotations'][label_category]['tags'].extend(tagging_results[API_MAP[label_category]])
                is_update = True

        # if 'Veronica Beard\'s Theron' in product_description:
        #     print(product_description)
        #     print(json.dumps(product['labeling']['annotations']['description']['tags'], indent=4))
        #     self.is_verbose = True

        is_update = is_update | self.correct_product_tags(product)

        # if 'Veronica Beard\'s Theron' in product_description:
        #     print(json.dumps(product['labeling']['annotations']['description']['tags'], indent=4))

        if is_new_product and llm_type == 'GPT4':
            self.llm_tags_cache[cache_name] = {
                'name' : product['labeling']['annotations']['name'],
                'description' : product['labeling']['annotations']['description']
            }
            json.dump(self.llm_tags_cache, open(self.cache_llm_file_name, 'w'))

        return is_update

    def get_cache_file_name(self):
        return f'./prep/_cache_{self.db_name}.json'
    
    def tag_products(self, tag_target=None, llm_type='GPT4'):
        current_db_name = self.db_name
        self.cache_llm_file_name = self.get_cache_file_name()
        self.db_name = current_db_name
        # if the file does not exist, create an empty one
        if not os.path.isfile(self.cache_llm_file_name):
            json.dump({}, open(self.cache_llm_file_name, 'w'))
            self.llm_tags_cache = {}
        else:
            self.llm_tags_cache = json.load(open(self.cache_llm_file_name, 'r'))
        time_start = time.perf_counter()
        self.nb_tagged_products = 0
        count_tagged = self.update_db_records('self.tag_product', [f'"{llm_type}"'], count_update_target=tag_target, is_show_progress=True, process_description=f'{llm_type} Tagging')
        if count_tagged > 0 and self.db_step == Production_Step.LLM:
            json.dump(self.llm_tags_cache, open(self.cache_llm_file_name, 'w'))
        printInfo(f'LLM tagging [{count_tagged} items tagged] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_tagged

    def correct_product_tags(self, product):
        # Nothing to see here... move along
        if len(product['labeling']['annotations']['name']['tags']) == 0 and len(product['labeling']['annotations']['description']['tags']) == 0:
            return False
        if not 'count_tagged_products' in locals():
            count_tagged_products = 0

        if product['name'] in self.debug_products:
            self.is_verbose = True
            pass

        count_tagged_products += 1
        if self.is_verbose:
            print('\n>> ' + product['labeling']['annotations']['name']['text'])

        for field in ['name', 'description']:
            if self.is_verbose:
                print('\n\t' + field.upper())

            content = product['labeling']['annotations'][field]
            content['tags'] =  sorted(content['tags'], key=lambda x: x['start'])

            is_mapping, content['tags']     = remove_wrong_mapping(content['text'], content['tags'], self.current_mapping, is_verbose=self.is_verbose)

            is_boundry, content['tags']     = fix_boundries(content['text'], content['tags'], is_verbose=self.is_verbose)

            is_product, content['tags']     = remove_product_category(content['text'], content['tags'], self.current_mapping, is_verbose=self.is_verbose)

            is_entity, content['tags']      = remove_uri_entity_mismatches(content['text'], content['tags'], self.current_mapping, is_verbose=self.is_verbose)

            is_wrong, content['tags']       = remove_wrong_tags(content['text'], content['tags'], self.wrong_tag_mapping, is_verbose=self.is_verbose)

            is_punctuation, content['tags'] = fix_punctuation(content['text'], content['tags'], is_verbose=self.is_verbose)

            is_embedded, content['tags']    = fix_embedded_tags(content['text'], content['tags'], is_verbose=self.is_verbose)                    

            is_duplicate, content['tags']   = remove_duplicate_tags(content['text'], content['tags'], is_verbose=self.is_verbose)

            is_changed = is_mapping | is_boundry | is_product | is_entity | is_wrong | is_punctuation | is_embedded | is_duplicate

            product['labeling']['annotations'][field] = content

        return is_changed

    def correct_tags(self, is_fix = True):
        time_start = time.perf_counter()
        count_corrected = self.update_db_records('self.correct_product_tags', count_update_target=None, is_show_progress=True, process_description='Correcting tags')
        printInfo(f'[{count_corrected} products corrected] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_corrected

    def monitor_process(self, response, process_description, nb_attempts = MONITOR_ATTEMPT):
        count_process_update = 0
        process_id = int(response.content)
        is_in_progress = True
        while is_in_progress:
            response = requests.get(f'{self.dyson_url}/productDatabaseProcesses/{process_id}')
            is_in_progress = json.loads(response.content)['completed'] == False
            if not is_in_progress:
                return response
            count_process_update += 1
            printInfo(f'Process {process_id} [{process_description}] still running.  Checking in {MONITOR_SLEEP} seconds [attempt #{count_process_update}]...')
            time.sleep(MONITOR_SLEEP) # wait before asking again
            # Wait max 1 hr for training to finish
            if count_process_update == nb_attempts:
                throwError(f'Process did not finish after {nb_attempts*MONITOR_SLEEP/60} minutes')
            
        return response

    def validate_clu(self):
        response = requests.post(f'{self.dyson_url}/productDatabases/{self.db_name}/train?force=true')
        if response.status_code == 200:
            self.monitor_process(response, "CLU Training", nb_attempts=120)  # Wait for 1 hr for CLU to be trained
        else:
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
                    if content[tag['start']:tag['end']].lower().startswith('double') and not label in ['doublebreasted', 'button', ]:
                        pass
                    self.representations[label].add(content[tag['start']:tag['end']].lower())

    def set_tag_usage(self):
        self.collect_existing_tags()
        self.collect_representations()

        with open(f'_stats_{self.category}_products.csv', 'w') as stats_file:
            self.description_tag_density = {}
            for cache_name in self.tagged_products:
                nb_of_tokens = len(self.tagged_products[cache_name]['description']['text'].split())
                nb_of_tags   = len(self.tagged_products[cache_name]['description']['tags'])
                tag_density = 0
                if nb_of_tokens > 0:
                    tag_density = round(nb_of_tags/nb_of_tokens,2)
                self.description_tag_density[cache_name] = {
                    'nb_tokens': nb_of_tokens, 
                    'nb_tags': nb_of_tags,
                    'tag_density': tag_density
                    }
                stats_file.write(f'{cache_name},{nb_of_tokens},{nb_of_tags},{tag_density}\n')

    def correct_uri(self, product):
        API_MAP = {'name': 'title_tags', 'description': 'description_tags'}    
        product_name = product['labeling']['annotations']['name']['text']
        product_description = product['labeling']['annotations']['description']['text']

        cache_name = get_complex_name(product_name, product_description)
        # Do not overwrite existing tags
        if cache_name in self.tagged_products:
            tagging_results = {}
            tagging_results['title_tags'] = self.tagged_products[cache_name]['name']['tags']
            tagging_results['description_tags'] = self.tagged_products[cache_name]['description']['tags']
        else:
            return False
    
        ### Ensure Uri in the tags
        tagging_results = json.dumps(tagging_results)
        tagging_results, change_count = re.subn('http://automat.ai/\w+/', f'http://automat.ai/{self.base_uri}/', tagging_results)
        if change_count == 0:
            return False
        tagging_results = json.loads(tagging_results)

        is_update = True
        for label_category in ['name', 'description']:
            product['labeling']['annotations'][label_category]['tags'] = tagging_results[API_MAP[label_category]]


        return is_update

    def update_all_uris(self):
        time_start = time.perf_counter()
        count_corrected = self.update_db_records('self.correct_uri', process_description='Correcting URIs')
        printInfo(f'[{count_corrected} URIs corrected] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_corrected

    def search_description(self, product, search_text):
        product_description = product['labeling']['annotations']['description']['text']
        if search_text in product_description.lower():
            self.found_products.append(product['labeling']['annotations']['name']['text'])
        return False

    def search_for_text(self, search_text):
        time_start = time.perf_counter()
        self.found_products = []
        self.update_db_records('self.search_description', [f'"{search_text.lower()}"'], process_description=f'Searching for {search_text}')
        printInfo(f'[{len(self.found_products)} products found] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return self.found_products

    def approve_product(self, product, approval='Approved'):
        product_name = product['labeling']['annotations']['name']['text']
        product_description = product['labeling']['annotations']['description']['text']

        cache_name = get_complex_name(product_name, product_description)
        # Approved tagged products which have never been approved
        if cache_name in self.tagged_products:
            if product['labelingApproval'] == 'Not Approved':
                product['labelingApproval'] = approval
                return True
        return False

    def approve_tagged_products(self):
        time_start = time.perf_counter()
        count_corrected = self.update_db_records('self.approve_product', process_description='Approving products')
        printInfo(f'[{count_corrected} products approved] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_corrected
    
    def partially_approve_tagged_products(self):
        time_start = time.perf_counter()
        count_corrected = self.update_db_records('self.approve_product', ['"Partially Approved"'], process_description='Partially approving products')
        printInfo(f'[{count_corrected} products approved] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_corrected
    
    def publish_product(self, product):
        if not product['publishState'] == 'New Product':
            print(product)
        product['publishState'] = 'Published'
        return True

    def publish_products(self):
        time_start = time.perf_counter()
        count_corrected = self.update_db_records('self.publish_product', process_description='Publishing products')
        printInfo(f'[{count_corrected} products published] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        return count_corrected
    
    def check_product(self, product):
        visual_tags = {}
        nlu_tags    = {}
        is_changed = False
        mapping_swap = {v: k for k, v in self.current_mapping.items()}

        nlu_fields = ['name', 'shortDescription', 'description']
        nlu_categories = set()

        for annotation in product['labeling']['annotations']:
            if 'tags' in product['labeling']['annotations'][annotation]:
                tags = product['labeling']['annotations'][annotation]['tags']
                for label_uri in tags:
                    if '|' in mapping_swap[label_uri['label']] and mapping_swap[label_uri['label']].split('|')[0] in self.categories_to_check:
                        if annotation.startswith('vi_'):
                            visual_tags[label_uri['label']] = mapping_swap[label_uri['label']]
                        elif annotation in nlu_fields:
                            nlu_tags[label_uri['label']] = mapping_swap[label_uri['label']]
                            nlu_categories.add(mapping_swap[label_uri['label']].split('|')[0])

        # Quick check if there are differences
        diff = DeepDiff(visual_tags, nlu_tags, ignore_order=True)
        if len(diff) == 0:
            return False

        key_copy = tuple(visual_tags.keys())
        for label_uri in key_copy:
            if label_uri in nlu_tags:
                continue
            visual_prefix = visual_tags[label_uri].split('|')[0]
            if visual_tags[label_uri].split('|')[0] in nlu_categories:
                nlu_difference = ''
                is_different = True
                for __, nlu_value in nlu_tags.items():
                    # If only the end leaf different, it's close enough
                    if nlu_value.startswith(visual_tags[label_uri]) or visual_tags[label_uri].startswith(nlu_value):
                        is_different = False
                        break
                    # Both are children of the same parent
                    elif '|'.join(nlu_value.split('|')[:-1]) == '|'.join(visual_tags[label_uri].split('|')[:-1]):
                        is_different = False
                        break
                if not is_different:
                    continue

                is_fixed = False
                if visual_prefix in self.categories_to_auto_correct:
                    for annotation in product['labeling']['annotations']:
                        if not annotation.startswith('vi_'):
                            continue
                        if 'tags' in product['labeling']['annotations'][annotation]:
                            product_tags = product['labeling']['annotations'][annotation]['tags']
                            for idx, db_tag in enumerate(product_tags):
                                if db_tag['label'] == label_uri:
                                    del product_tags[idx]
                                    is_fixed = True
                                    is_changed = True
                if is_fixed:
                    printWarning(f'{product["name"]}: Visual tag [{label_uri.split("/")[-1]}] was different from the text so was removed.')
                else:
                    printWarning(f'{product["name"]}: Visual tag [{label_uri.split("/")[-1]}] is different from the one in the name or description.')
                    self.consistency_report.write(f'=HYPERLINK("https://pim-maestro-v2-dev.app-play.salesfloor.net/product-inventory-management/{self.db_name}/{product["id"]["productId"]}";"{product["id"]["productId"]}"),{product["name"]},{label_uri.split("/")[-1]},{nlu_difference},{is_fixed}\n')

        return is_changed
    
    def check_for_contradictions(self):
        time_start = time.perf_counter()
        self.categories_to_check        = json.load(open('./prep/consistent_categories.json', 'r'))
        self.categories_to_auto_correct = json.load(open('./prep/consistent_categories_AUTO_CORRECT.json', 'r'))

        self.current_mapping = get_name_url_mapping(json.loads(self.ontology), {})
        self.consistency_report = open(f'./prep/consistency_report-{self.db_name}.csv', 'w')
        self.consistency_report.write('Product Link,Product Name,Visual Value,NLU Value,Auto-Fixed\n')
        count_corrected = self.update_db_records('self.check_product', process_description='Checking products')
        printInfo(f'[{count_corrected} product tags different] latency: {round(time.perf_counter() - time_start, 3)} seconds.')
        self.consistency_report.close()
        return count_corrected
    
    def upload_whole_db(self, json_db_file):
        request_url = f'{self.dyson_url}/productDatabases/{self.db_name}/dump?overwrite=true'
        db_content  = json.load(open(json_db_file, 'r'))
        if self.db_step == Production_Step.ONTOLOGY:
            self.helper_requests('post', request_url, json_post_data=db_content, process_description='Db Upload')
        else:
            self.helper_requests('post', request_url, json_post_data=db_content, expected_nb_records=len(db_content['products']), process_description='Db Upload')
