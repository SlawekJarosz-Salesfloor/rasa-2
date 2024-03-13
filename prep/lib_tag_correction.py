import re
import unicodedata

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

def strip_accents(input_string):
   return ''.join(c for c in unicodedata.normalize('NFD', input_string)
                  if unicodedata.category(c) != 'Mn')

def get_label_suffix(uri):
    return uri.split('/')[-1].lower()


def get_tokens_positions(content):

    # Define a regex pattern to identify tokens
    token_pattern = r"\b(?:\w+['%]?\w*%?\w*)\b"

    # Find all matches with start and end positions
    matches = list(re.finditer(token_pattern, content.lower()))

    # Extract tokens and their positions
    tokens_with_positions = [(match.group(), match.start(), match.end()) for match in matches]

    return tokens_with_positions


def extract_substring(target_word, sentence):
    tokens_with_positions = get_tokens_positions(sentence)

    word_found = None
    response = None, []
    if len(tokens_with_positions) > 0:
        start_positions = []
        for occurrence in tokens_with_positions:
            if occurrence[0] == target_word:
                word_found = target_word
                start_positions.append(occurrence[1])

        response = word_found, start_positions

    return response

def remove_duplicate_tags(content, tags, is_verbose = True):
    if len(tags) == 0:
        return False, []
    
    is_changed = False
    str_tags = []
    for tag in tags:
        str_tags.append(str(tag))

    tag_start_ends = []
    for tag in tags:
        tag_start_ends.append({'start': tag['start'], 'end': tag['end']})

    duplicate_tag_indicies = []

    # Check for exact duplicates
    for idx, tag in enumerate(tags):
        if str(tag) in str_tags and not str_tags.index(str(tag)) == idx:
            duplicate_tag_indicies.append(idx)

    # Check for same tag text duplicates
    for idx, tag in enumerate(tags):
        for jdx, tag_position in enumerate(tag_start_ends):
            if idx >= jdx:
                continue
            if jdx in duplicate_tag_indicies:
                continue
            if tag['start'] == tag_position['start'] and tag['end'] == tag_position['end']:
                duplicate_tag_indicies.append(jdx)

    duplicate_tag_indicies = set(duplicate_tag_indicies)
    if len(duplicate_tag_indicies) > 0:
        is_changed = True
        remove_count = 0
        for idx in duplicate_tag_indicies:
            if is_verbose:
                print(content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower() + '\n\t\t--> REMOVED (duplicate)')
            del tags[idx - remove_count]
            remove_count += 1

    return is_changed, tags

def get_embedded_tag_ids(tags):    
    embedded_tag_indicies = []
    prev_end   = -1
    prev_start = -1
    sorted_tags =  sorted(tags, key=lambda x: x['start'])
    for idx, tag in enumerate(sorted_tags):
        if tag['start'] == prev_start and tag['end'] == prev_end:
            embedded_tag_indicies.append((idx, True))
        elif prev_end > tag['start']:
            embedded_tag_indicies.append((idx, False))

        prev_start = tag['start']
        prev_end = tag['end']

    return embedded_tag_indicies

def fix_embedded_tags(content, tags, is_verbose = True):
    is_changed = False

    # Check for overlaping tags
    embedded_tag_indicies = get_embedded_tag_ids(tags)
    if len(embedded_tag_indicies) == 0:
        return is_changed, tags

    # Try to correct tags start and end values
    for idx, __ in embedded_tag_indicies:
        tag_text    = content[tags[idx]['start']:tags[idx]['end']].lower()
        label_match = tags[idx]['label'].split('/')[-1].lower()
        if label_match in tag_text:
            word_match, word_starts = extract_substring(label_match, tag_text)
            if word_match == None:
                continue
            for start in word_starts:
                new_start = tags[idx]['start'] + start
                new_end   = tags[idx]['start'] + len(word_match)
                if tags[idx]['start'] == new_start and tags[idx]['end'] == new_end:
                    continue
                if is_verbose:
                    print(content[tags[idx]['start']:tags[idx]['end']].lower())
                if is_verbose:
                    print(f'\t\t--> {content[tags[idx]["start"]:tags[idx]["end"]].lower()} ({tags[idx]["start"]}:{tags[idx]["end"]}) >> ', end='')
                tags[idx]['start'] = new_start
                tags[idx]['end']   = new_end
                if is_verbose:
                    print(f'({tags[idx]["start"]}:{tags[idx]["end"]})')
            is_changed = True

    # Check again
    embedded_tag_indicies = get_embedded_tag_ids(tags)

    # Remove any remaining overlaping tags
    while len(embedded_tag_indicies) > 0:
        is_changed = True
        id, is_duplicate = embedded_tag_indicies[0]
        if is_verbose:
            if is_duplicate:
                print(content[tags[id]['start']:tags[id]['end']].lower() + '\n\t\t--> REMOVED (duplicate)')
            else:
                print(content[tags[id]['start']:tags[id]['end']].lower() + '\n\t\t--> REMOVED (embedded)')
        del tags[id]
        embedded_tag_indicies = get_embedded_tag_ids(tags)

    return is_changed, tags

def fix_punctuation(content, tags, is_verbose = True):
    is_changed = False
    idx = 0
    # print(description['tags'])
    for tag in tags[:]:
        tag_text    = content[tag['start']:tag['end']].lower()
        if is_verbose:
            print(tag_text)
        label_match = get_label_suffix(tag['label'])

        tag_text = content[tag['start']:tag['end']].lower()
        if tag_text.endswith('%'):            
            # Very common for % to be included in material types
            if label_match in tag_text:
                match_start = tag_text.index(label_match)
                tag['start'] = tag['start'] + match_start
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
                if is_verbose:
                    print('\t\t--> ' + content[tag['start']:tag['end']])
            # Another common tagging error
            else:
                if bool(re.search('(\d*%)', tag_text)):
                    is_changed = True
                    try:
                        # Percentages being tagged as material.  Try to correct
                        if content[(tag['end'] + 1):(tag['end'] + 1 + len(label_match))].lower() == label_match.lower():
                            tag['start'] = tag['end'] + 1
                            tag['end']   = tag['start'] + len(label_match)
                            if is_verbose:
                                print('\t\t--> ' + content[tag['start']:tag['end']])
                        else:
                            del tags[idx]
                            if is_verbose:
                                print('\t\t--> REMOVED (% in text)')
                            continue
                    except:
                        del tags[idx]
                        if is_verbose:
                            print('\t\t--> REMOVED (% in text)')
                        continue                    
        elif len(tag_text) < 3:
            del tags[idx]
            is_changed = True
            if is_verbose:
                print('\t\t--> REMOVED (too short)')
            continue

        tag_text = content[tag['start']:tag['end']].lower()
        if '/' in tag_text or '%' in tag_text or '.' in tag_text:
            matches = re.search(label_match, tag_text)
            if not matches == None:
                tag['start'] = tag['start'] + tag_text.index(label_match)
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
                if is_verbose:
                    print('\t\t--> ' + content[tag['start']:tag['end']])
            else:
                del tags[idx]
                is_changed = True
                if is_verbose:
                    print('\t\t--> REMOVED (punctuation)')
                continue
        
        tag_text = content[tag['start']:tag['end']].lower()
        if '% ' in tag_text:
            if tag_text[tag_text.index('% ') + 2:tag_text.index('% ') + 2 + len(label_match)].lower() == label_match:
                tag['start'] = tag['start'] + tag_text.index('% ') + 2
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
                if is_verbose:
                    print('\t\t--> ' + content[tag['start']:tag['end']])
            else:
                tag['start'] = tag['start'] + tag_text.index('% ') + 2
                is_changed = True
                if is_verbose:
                    print('\t\t--> ' + content[tag['start']:tag['end']])

        tag_text = content[tag['start']:tag['end']].lower()
        if tag_text[-1] in ['.', ':', ';']:
            tag['end'] -= 1
            is_changed = True
            if is_verbose:
                print('\t\t--> ' + content[tag['start']:tag['end']])
        idx += 1

    return is_changed, tags

def remove_wrong_tags(content, tags, wrong_tag_map, is_verbose = True):
    is_changed = False
    remove_count = 0
    for idx, tag in enumerate(tags[:]):
        label = get_label_suffix(tag['label'])
        if label in wrong_tag_map:
            tag_text = content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower()
            if tag_text in wrong_tag_map[label]:
                if is_verbose:
                    print(tag_text + '\n\t\t--> REMOVED (wrong)')
                del tags[idx - remove_count]
                remove_count += 1
                is_changed = True

    remove_count = 0
    for idx, tag in enumerate(tags[:]):
        tag_text = content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower()
        if tag_text in wrong_tag_map['*']:
            if is_verbose:
                print(tag_text + '\n\t\t--> REMOVED (wrong)')
            del tags[idx - remove_count]
            remove_count += 1
            is_changed = True
    return is_changed, tags

def remove_product_category(content, tags, name_url_mapping, is_verbose = True):
    product_category_uri_suffix = None
    for name_path in name_url_mapping:
        if name_path.startswith('product category|'):
            product_category_uri_suffix = name_url_mapping[name_path]
            break
    if product_category_uri_suffix == None:
        return False, tags
    
    is_changed = False
    remove_count = 0
    for idx, tag in enumerate(tags[:]):
        if tag['label'].endswith(product_category_uri_suffix):
            tag_text = content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower()
            if is_verbose:
                print(tag_text + '\n\t\t--> REMOVED (product category)')
            del tags[idx - remove_count]
            remove_count += 1
            is_changed = True

    return is_changed, tags

def remove_wrong_mapping(content, tags, name_url_mapping, is_verbose = True):
    is_found = False
    swapped_mapping = {value: key for key, value in name_url_mapping.items()}
    count_removed = 0
    for idx, tag in enumerate(tags[:]):
        if tag['label'].split('/')[-1] in swapped_mapping:
            is_found = True
            break

        if not is_found:
            if is_verbose:
                print(tag['label'] + '\n\t\t--> REMOVED (not in ontology)')
            del tags[idx - count_removed]
            count_removed += 1

    return count_removed > 0, tags

def remove_uri_entity_mismatches(content, tags, name_url_mapping, is_verbose = True):
    is_changed = False
    label_paths = list(name_url_mapping.keys())
    for idx, name_path in enumerate(label_paths):
        parts = name_path.split('|')
        if len(parts) > 1:
            label_paths[idx] = parts[0].replace('-', '') + '|' + parts[-1].replace('-', '')
        else:
            label_paths[idx] = parts[0].replace('-', '')
        label_paths[idx] = strip_accents(label_paths[idx])

    correction_prefix = 'Corrected Entity: '
    for idx, tag in enumerate(tags[:]):
        if tag['entity'].startswith(correction_prefix):
            continue
        label_suffix = tag['label'].split('/')[-1].lower()
        for name_path in name_url_mapping:
            if name_path.lower().endswith('|' + label_suffix) and not name_url_mapping[name_path].lower() == label_suffix:
                tag_text = content[tags[idx]['start']:tags[idx]['end']].lower()
                if is_verbose:
                    print(tag_text + '\n\t\t--> UPDATED (entity to URI mismatch)')
                tag['entity'] = correction_prefix + name_path.split('|')[0].title() + '.' + label_suffix.title()
                is_changed = True

    return is_changed, tags

def fix_boundries(content, tags, is_verbose = True):
    is_changed = False
    
    tokens_with_positions = get_tokens_positions(content)
    token_starts = []
    token_ends   = []
    for token, start, end in tokens_with_positions:
        token_starts.append(start)
        token_ends.append(end)

    for idx, tag in enumerate(tags):
        if tag['start'] in token_starts and tag['end'] in token_ends:
            continue

        if not tag['start'] in token_starts:
            for idx, __ in enumerate(token_starts[1:]):
                if tag['start'] >= token_ends[idx - 1] and tag['start'] < token_starts[idx]:
                    prev_tag_text = content[tag['start']:tag['end']].lower()
                    tag['start'] = token_starts[idx]
                    new_tag_text = content[tag['start']:tag['end']].lower()
                    if is_verbose:
                        print(f'{prev_tag_text} -> {new_tag_text}\n\t\t--> UPDATED (token boundries [start])')
                    is_changed = True
                    break

        if not tag['end'] in token_ends:
            for idx, __ in enumerate(token_ends[:-1]):
                if tag['end'] < token_starts[idx + 1] and tag['end'] < token_ends[idx]:
                        prev_tag_text = content[tag['start']:tag['end']].lower()
                        tag['end'] = token_ends[idx]
                        new_tag_text = content[tag['start']:tag['end']].lower()
                        if is_verbose:
                            print(f'{prev_tag_text} -> {new_tag_text}\n\t\t--> UPDATED (token boundries [end])')
                        is_changed = True
                        break

    return is_changed, tags

def remove_overtagging(content, tags, wrong_text_patterns, is_verbose = True):
    is_changed = False

    for pattern_group in wrong_text_patterns:
        for label in pattern_group:
            for regex_remove in pattern_group[label]:
                matches = re.finditer(regex_remove, content, flags=re.IGNORECASE)
                for match in matches:
                    for positions in match.regs:
                        for idx, tag in enumerate(tags):
                            uri_suffix = tag['label'].split('/')[-1].lower()
                            if tag['start'] >= positions[0] and tag['end'] <= positions[1] and label == uri_suffix:
                                del tags[idx]
                                is_changed = True
                                if is_verbose:
                                    print(label + f'\n\t\t--> REMOVED (overtagging)')
        
    return is_changed, tags

def helper_correct_tags(content, tags, name_url_map, wrong_tag_mapping, wrong_text_pattern):
    tags =  sorted(tags, key=lambda x: x['start'])

    print()
    
    is_mapping, tags     = remove_wrong_mapping(content, tags, name_url_map)

    is_boundry, tags     = fix_boundries(content, tags)

    is_product, tags     = remove_product_category(content, tags, name_url_map)

    is_entity, tags      = remove_uri_entity_mismatches(content, tags, name_url_map)

    is_wrong, tags       = remove_wrong_tags(content, tags, wrong_tag_mapping)

    is_punctuation, tags = fix_punctuation(content, tags)

    is_embedded, tags    = fix_embedded_tags(content, tags)                    

    is_duplicate, tags   = remove_duplicate_tags(content, tags)

    is_over_tag, tags    = remove_overtagging(content, tags, wrong_text_pattern)

    print()

    return (is_boundry | is_product | is_entity | is_wrong | is_punctuation | is_embedded | is_duplicate | is_mapping | is_over_tag), content, tags

# main driver function
if __name__ == '__main__':
    print(fix_boundries(
        'From the Prom Collection. Sequined with floral designs; Mac Duggal\'s stunning gown shimmers with each movement. This charming piece features a romantic sweetheart neck and a classic strapless silhouette. Sweetheart neck. Strapless. Back-zip closure. 100% polyester. Lining: 100% polyester. Spot clean. Imported.', []))