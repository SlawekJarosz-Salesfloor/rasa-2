import itertools
import re
import unicodedata

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
    for i, outer_tag in enumerate(tags):
        for j, inner_tag in enumerate(tags):
            if i == j:
                continue
            if inner_tag['start'] == outer_tag['start'] and inner_tag['end'] == outer_tag['end'] and inner_tag['label'] == outer_tag['label']:
                embedded_tag_indicies.append((sorted([i, j]), True))
            elif inner_tag['start'] >= outer_tag['start'] and inner_tag['end'] <= outer_tag['end']:
                embedded_tag_indicies.append((sorted([i, j]), False))
    embedded_tag_indicies.sort()
    embedded_tag_indicies = list(embedded_tag_indicies for embedded_tag_indicies,_ in itertools.groupby(embedded_tag_indicies))
    return embedded_tag_indicies

def fix_embedded_tags(content, tags, is_verbose = True):
    is_changed = False

    # Check for overlaping tags
    embedded_tag_indicies = get_embedded_tag_ids(tags)
    if len(embedded_tag_indicies) == 0:
        return is_changed, tags

    # Try to correct tags start and end values
    for clash_ids, __ in embedded_tag_indicies:
        for idx in clash_ids:
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
        ids, is_duplicate = embedded_tag_indicies[0]
        if is_verbose:
            if is_duplicate:
                print(content[tags[ids[1]]['start']:tags[ids[1]]['end']].lower() + '\n\t\t--> REMOVED (duplicate)')
            else:
                print(content[tags[ids[1]]['start']:tags[ids[1]]['end']].lower() + '\n\t\t--> REMOVED (embedded)')
        del tags[ids[1]]
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
            if name_path.lower().endswith('|' + label_suffix):
                tag_text = content[tags[idx]['start']:tags[idx]['end']].lower()
                if is_verbose:
                    print(tag_text + '\n\t\t--> UPDATED (entity to URI mismatch)')
                tag['entity'] = correction_prefix + name_path.split('|')[0].title() + '.' + label_suffix.title()
                is_changed = True

    return is_changed, tags

def fix_boundries(content, tags, is_verbose = True):
    is_changed = False
    
    tokens_with_positions = get_tokens_positions(content)

    # Display the result
    for idx, token_tuple in enumerate(tokens_with_positions):
        token, __, ___ = token_tuple
        # print(f"Token: '{token}', Start: {start}, End: {end}")
        # Remove unwanted tokens
        if token.isnumeric():
            del tokens_with_positions[idx]
        elif len(token) < 3:
            del tokens_with_positions[idx]

    for idx, tag in enumerate(tags):
        for token, start, end in tokens_with_positions:
            if tag['start'] >= start and tag['end'] < end:
                tag_text = content[tags[idx]['start']:tags[idx]['end']].lower()
                if is_verbose:
                    print(f'{tag_text} -> {token}\n\t\t--> UPDATED (token boundries)')
                tag['end'] = end
                is_changed = True

    return is_changed, tags


# main driver function
if __name__ == '__main__':
    print(fix_boundries(
        'From the Prom Collection. Sequined with floral designs; Mac Duggal\'s stunning gown shimmers with each movement. This charming piece features a romantic sweetheart neck and a classic strapless silhouette. Sweetheart neck. Strapless. Back-zip closure. 100% polyester. Lining: 100% polyester. Spot clean. Imported.', []))