#!/usr/bin/env python

from typing import Dict, Any, List, Tuple, Union

def get_all_dict_keys(json_structure: Any) -> Dict[str, Any]:
    """
    Recursively extracts all keys from a JSON structure.

    Args:
        json_structure (Any): The JSON structure to extract keys from.

    Returns:
        Dict[str, Any]: A dictionary containing all the extracted keys.
    """
    def recursive_extract_keys(obj: Any, parent_key: str = '', keys_set: set[str] = None) -> Dict[str, Any]:
        if keys_set is None:
            keys_set = set()

        keys = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys[key] = recursive_extract_keys(value, full_key, keys_set)
        elif isinstance(obj, list):
            list_keys = []
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    list_keys.append(recursive_extract_keys(item, full_key, keys_set))
            return list_keys
        else:
            return None
        return keys

    return recursive_extract_keys(json_structure)

def remove_invalid_tag_name_characters(tag_name: str) -> str:
    from base.constants import TAG_NAME_PATTERN
    return TAG_NAME_PATTERN.sub('', tag_name)

def get_tag_builder() -> Dict[str, Any]:
    from base.constants import TAG_BUILDER_TEMPLATE
    return TAG_BUILDER_TEMPLATE.copy()

def reset_tag_builder(tag_builder: Dict[str, Any] = {}) -> None:
    from base.constants import TAG_BUILDER_TEMPLATE
    tag_builder.update(TAG_BUILDER_TEMPLATE)
    
def find_row_by_tag_name(df, tag_name):
    row = df[df['Tag Name'] == tag_name]
    return row.iloc[0] if not row.empty else None


def extract_kepware_tag_name(opc_item_path: str) -> str:
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def extract_area_and_offset(address: str) -> Tuple[str, str]:
    from base.constants import ADDRESS_PATTERN
    match = ADDRESS_PATTERN.search(address)
    if match:
        first_number_index = match.start()
        area = address[:first_number_index]
        if 'X' in address:
            offset = str(int(address[first_number_index:].lstrip('0') or '0', 16))
        else:
            offset = address[first_number_index:].lstrip('0') or '0'
        return area, offset
    else :
        exit(f"Could not find any numbers in address {address}")

def get_offset_and_array_size(offset: str) -> Tuple[str, str]:
    array_size = ''
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]

    return (offset, array_size)

def set_missing_tag_properties(tags, new_tag) -> None:
    from base.constants import REQUIRED_KEYS
    required_keys = REQUIRED_KEYS.copy()

    def handle_missing_tags(dummy_tag, new_tag):
        if required_keys == []:
            return True
        if 'tags' in dummy_tag:
            handle_missing_tags(dummy_tag['tags'], new_tag)
        else:
            for key in required_keys:
                if (key not in new_tag) and (key in dummy_tag) and (dummy_tag[key] != 'Folder'):
                    new_tag[key] = dummy_tag[key]
                    required_keys.remove(key)

    for dummy_tag in tags:
        if handle_missing_tags(dummy_tag, new_tag):
            break


def generate_full_path_from_name_parts(name_parts):
    return ('/'.join(name_parts)).rstrip('/')


def set_new_tag_properties(tags: Union[Dict[str, Any], List[Dict[str, Any]]], new_tag: Dict[str, Any]) -> None:
    set_missing_tag_properties(tags, new_tag)
    new_tag.update({
        'enabled': False,
        'valueSource': 'opc',
        'tagGroup': 'default' # Remove once this in production
    })

def set_existing_tag_properties(current_tag, new_tag):
    new_tag['tagGroup'] = 'default' # Remove once this in production
    new_tag['tagType'] = current_tag['tagType']
    for key in ['historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']:
        if key in current_tag:
            new_tag[key] = current_tag[key]
    new_tag['enabled'] = True

def set_tag_properties(tags={}, new_tag={}, current_tag={}):
    if tags:
        set_new_tag_properties(tags, new_tag)
    else:
        set_existing_tag_properties(current_tag, new_tag)

def build_tag_hierarchy(tags, name_parts):
    dummy_tags = tags
    for part in name_parts[:-1]:
        found = False
        for tag in dummy_tags:
            if tag['name'] == part:
                dummy_tags = tag['tags']
                found = True
                break
        if not found:
            new_folder_tag = {
                "name": part,
                "tagType": "Folder",
                "tags": []
            }
            dummy_tags.append(new_folder_tag)
            dummy_tags = new_folder_tag['tags']
    return dummy_tags