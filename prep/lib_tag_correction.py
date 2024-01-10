import itertools
import re

def get_label_suffix(uri):
    return uri.split('/')[-1].lower()

def extract_substring(string_match, input_string):

    # Define a regular expression pattern for the desired substring
    pattern = re.compile(r'(^|\s)([\w\-]*' + string_match + '[\w\-]*?)(\s|\;+|\.+|$)')

    # Use the findall function to extract all matching substrings
    matches = re.search(pattern, input_string)

    # Get the start of the match
    start = input_string.index(matches.group(2))

    return matches.group(2), start

def remove_duplicate_tags(content, tags):
    is_changed = False
    str_tags = []
    for tag in tags:
        str_tags.append(str(tag))

    duplicate_tag_indicies = []
    for idx, tag in enumerate(tags):
        if str(tag) in str_tags and not str_tags.index(str(tag)) == idx:
            duplicate_tag_indicies.append(idx)

    if len(duplicate_tag_indicies) > 0:
        is_changed = True
        remove_count = 0
        for idx in duplicate_tag_indicies:
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
            if inner_tag['start'] >= outer_tag['start'] and inner_tag['end'] <= outer_tag['end']:
                embedded_tag_indicies.append(sorted([i, j]))
    embedded_tag_indicies.sort()
    embedded_tag_indicies = list(embedded_tag_indicies for embedded_tag_indicies,_ in itertools.groupby(embedded_tag_indicies))
    return embedded_tag_indicies

def fix_embedded_tags(content, tags):
    is_changed = False

    # Check for overlaping tags
    embedded_tag_indicies = get_embedded_tag_ids(tags)
    if len(embedded_tag_indicies) == 0:
        return is_changed, tags

    # Try to detangle the tags
    for clash_ids in embedded_tag_indicies:
        for idx in clash_ids:
            tag_text    = content[tags[idx]['start']:tags[idx]['end']].lower()
            label_match = tags[idx]['label'].split('/')[-1].lower()
            if label_match in tag_text:
                word_match, word_start = extract_substring(label_match, tag_text)
                print(content[tags[idx]['start']:tags[idx]['end']].lower())
                tags[idx]['start'] = tags[idx]['start'] + word_start
                tags[idx]['end']   = tags[idx]['start'] + len(word_match)
                print('\t\t--> '+ content[tags[idx]['start']:tags[idx]['end']].lower())
                is_changed = True

    # Check again
    embedded_tag_indicies = get_embedded_tag_ids(tags)

    # Remove any remaining overlaping tags
    while len(embedded_tag_indicies) > 0:
        is_changed = True
        ids = embedded_tag_indicies[0]
        print(content[tags[ids[1]]['start']:tags[ids[1]]['end']].lower() + '\n\t\t--> REMOVED (embedded)')
        del tags[ids[1]]
        embedded_tag_indicies = get_embedded_tag_ids(tags)

    return is_changed, tags

def fix_punctuation(content, tags):
    is_changed = False
    idx = 0
    # print(description['tags'])
    for tag in tags[:]:
        tag_text    = content[tag['start']:tag['end']].lower()

        print(tag_text)
        label_match = get_label_suffix(tag['label'])

        if tag_text.startswith('lining:'):
            tag['end'] = tag['start'] + len('lining')
            is_changed = True
            print('\t\t--> ' + content[tag['start']:tag['end']])
        
        tag_text = content[tag['start']:tag['end']].lower()
        if tag_text.endswith('%'):            
            # Very common for % to be included in material types
            if label_match in tag_text:
                match_start = tag_text.index(label_match)
                tag['start'] = tag['start'] + match_start
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
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
                            print('\t\t--> ' + content[tag['start']:tag['end']])
                        else:
                            del tags[idx]
                            print('\t\t--> REMOVED (% in text)')
                            continue
                    except:
                        del tags[idx]
                        print('\t\t--> REMOVED (% in text)')
                        continue                    
        elif len(tag_text) < 3:
            del tags[idx]
            is_changed = True
            print('\t\t--> REMOVED (too short)')
            continue

        tag_text = content[tag['start']:tag['end']].lower()
        if '/' in tag_text or '%' in tag_text or '.' in tag_text:
            matches = re.search(label_match, tag_text)
            if not matches == None:
                tag['start'] = tag['start'] + tag_text.index(label_match)
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
                print('\t\t--> ' + content[tag['start']:tag['end']])
            else:
                del tags[idx]
                is_changed = True
                print('\t\t--> REMOVED (punctuation)')
                continue
        
        tag_text = content[tag['start']:tag['end']].lower()
        if '% ' in tag_text:
            if tag_text[tag_text.index('% ') + 2:tag_text.index('% ') + 2 + len(label_match)].lower() == label_match:
                tag['start'] = tag['start'] + tag_text.index('% ') + 2
                tag['end']   = tag['start'] + len(label_match)
                is_changed = True
                print('\t\t--> ' + content[tag['start']:tag['end']])
            else:
                tag['start'] = tag['start'] + tag_text.index('% ') + 2
                is_changed = True
                print('\t\t--> ' + content[tag['start']:tag['end']])

        tag_text = content[tag['start']:tag['end']].lower()
        if tag_text[-1] in ['.', ':', ';']:
            tag['end'] -= 1
            is_changed = True
            print('\t\t--> ' + content[tag['start']:tag['end']])
        idx += 1

    return is_changed, tags

def remove_wrong_tags(content, tags, wrong_tag_map):
    is_changed = False
    remove_count = 0
    for idx, tag in enumerate(tags[:]):
        label = get_label_suffix(tag['label'])
        if label in wrong_tag_map:
            tag_text = content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower()
            if tag_text in wrong_tag_map[label]:
                print(tag_text + '\n\t\t--> REMOVED (wrong)')
                del tags[idx - remove_count]
                remove_count += 1
                is_changed = True

    remove_count = 0
    for idx, tag in enumerate(tags[:]):
        tag_text = content[tags[idx - remove_count]['start']:tags[idx - remove_count]['end']].lower()
        if tag_text in wrong_tag_map['*']:
            print(tag_text + '\n\t\t--> REMOVED (wrong)')
            del tags[idx - remove_count]
            remove_count += 1
            is_changed = True
    return is_changed, tags
