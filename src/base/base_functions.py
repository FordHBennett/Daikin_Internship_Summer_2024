#!/usr/bin/env python

from typing import Dict, Any, List, Tuple, Union
from functools import lru_cache
from re import compile as re_compile, sub
import logging


logging.basicConfig(
    filename='tag_generation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',  
    style='%'  
)

def log_message(message: str, level: str = 'info'):
    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'Name Change':
        logging.debug(message)
    else:
        logging.info(message)  


ADDRESS_PATTERN = re_compile(r'\d+')
TAG_NAME_PATTERN = re_compile(r'[^a-zA-Z0-9-_ .]')

DATA_TYPE_MAPPINGS = {
    'Short': ('Int2', 'Int16'),
    'Int2': ('Int2', 'Int16'),
    'Word': ('Int2', 'Int16'),
    'Integer': ('Int4', 'Int32'),
    'Int4': ('Int4', 'Int32'),
    'BCD': ('Int4', 'Int32'),
    'Boolean': ('Boolean', 'Bool')
}

REQUIRED_KEYS = ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']

def Remove_Invalid_Tag_Name_Characters(tag_name: str) -> str:
    
    return TAG_NAME_PATTERN.sub('', tag_name)

def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
    """
    Recursively extracts all keys from a JSON structure.

    Args:
        json_structure (Any): The JSON structure to extract keys from.

    Returns:
        Dict[str, Any]: A dictionary containing all the extracted keys.
    """
    def Recursive_Extract_Keys(obj: Any, parent_key: str = '', keys_set: set[str] = None) -> Dict[str, Any]:
        if keys_set is None:
            keys_set = set()

        keys = {}
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys[key] = Recursive_Extract_Keys(value, full_key, keys_set)
        elif isinstance(obj, list):
            list_keys = []
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    list_keys.append(Recursive_Extract_Keys(item, full_key, keys_set))
            return list_keys
        else:
            return None
        return keys

    return Recursive_Extract_Keys(json_structure)



def Create_Tag_Builder_Properties() -> Dict[str, Any]:
    return {
        "path_data_type": None,
        "data_type": None,
        "tag_name": None,
        "tag_name_path": None,
        "address": None,
        "area": None,
        "offset": None,
        "array_size": None,
        "row": None,
        "device_name": None,
        "kepware_tag_name": None,
        "is_tag_from_csv_flag": False
    }

def Reset_Tag_Builder_Properties(tag_builder_properties: Dict[str, Any] = {}) -> None:
    tag_builder_properties.update(Create_Tag_Builder_Properties())
    
def Find_Row_By_Tag_Name(df, tag_name):

    return df[df['Tag Name'] == tag_name]

def Extract_Kepware_Tag_Name(opc_item_path: str) -> str:
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def Extract_Area_And_Offset(address: str) -> Tuple[str, str]:
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
    


def Extract_Offset_And_Array_Size(offset: str) -> Tuple[str, str]:
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]
        return offset, array_size
    return offset, ''

@lru_cache(maxsize=None)
def Convert_Data_Type(data_type: str) -> Tuple[str, str]:
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))

def Find_Missing_Tag_Properties(tags, new_tag) -> None:
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


def Generate_Full_Path_From_Name_Parts(name_parts):
    return ('/'.join(name_parts)).rstrip('/')


def Set_New_Tag_Properties(tags: Union[Dict[str, Any], List[Dict[str, Any]]], new_tag: Dict[str, Any]) -> None:
    Find_Missing_Tag_Properties(tags, new_tag)
    new_tag.update({
        'enabled': False,
        'valueSource': 'opc',
        'tagGroup': 'default' # Remove once this in production
    })

def Set_Existing_Tag_Properties(current_tag, new_tag):
    new_tag['tagGroup'] = 'default' # Remove once this in production
    new_tag['tagType'] = current_tag['tagType']
    for key in ['historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']:
        if key in current_tag:
            new_tag[key] = current_tag[key]
    new_tag['enabled'] = True

def Set_Tag_Properties(tags={}, new_tag={}, current_tag={}):
    if tags:
        Set_New_Tag_Properties(tags, new_tag)
    else:
        Set_Existing_Tag_Properties(current_tag, new_tag)

def Build_Tag_Hierarchy(tags, name_parts):
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