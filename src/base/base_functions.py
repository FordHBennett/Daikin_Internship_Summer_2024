#!/usr/bin/env python
from pandas import DataFrame as pd_DataFrame
from typing import Dict, Any, List, Tuple

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


def Get_Basename_Without_Extension(file_path: str) -> str:
    from os.path import basename as os_path_basename
    from os.path import splitext as os_path_splitext
    """
    Returns the base name of a file path without the file extension.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The base name of the file without the extension.
    """
    base_name = os_path_basename(file_path)
    name, _ = os_path_splitext(base_name)
    return name

def Remove_Invalid_Tag_Name_Characters(tag_name: str) -> str:
    from re import sub as re_sub
    return re_sub(r'[^a-zA-Z0-9-_ .]', '', tag_name)

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

def Get_ALL_JSON_Paths(dir: str) -> List[str]:
    from os import walk as os_walk
    from os.path import join as os_path_join

    dir = os_path_join(dir, 'json')
    json_paths: List[str] = []
    for root, _, files in os_walk(dir):
        for file in files:
            if file.endswith('.json'):
                json_paths.append(os_path_join(root, file))
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    from os import walk as os_walk
    from os.path import join as os_path_join
    dir = os_path_join(dir, 'csv')
    csv_paths: List[str] = []
    for root, _, files in os_walk(dir):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os_path_join(root, file))
    return csv_paths

def Read_Json_Files(json_files: List[str]) -> Dict[str, Dict[str, Any]]:
    from os.path import basename as os_path_basename
    from json import load as json_load
    from copy import deepcopy as copy_deepcopy
    templete_json: Dict[str, Any] = {}
    ignition_json: Dict[str, Any] = {}
    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_structure = json_load(f)
            keys = Get_All_Keys(json_structure)
            templete_json.update(keys)
            new_file_name = ''
            for key in json_structure["tags"]:
                if 'opcItemPath' in key:
                    new_file_name =  copy_deepcopy(key["opcItemPath"][key["opcItemPath"].rfind("=") + 1:key["opcItemPath"].find(".")])
                    log_message(f"{os_path_basename(json_file)[:os_path_basename(json_file).find('.')]} Changed to {new_file_name}", 'info')
                    break
            ignition_json[new_file_name] = json_structure
            ignition_json[new_file_name]["name"] = new_file_name
    return ignition_json

def Read_CSV_Files(csv_files: List[str]) -> Dict[str, pd_DataFrame]:
    from pandas import read_csv as pd_read_csv
    csv_df: Dict[str, pd_DataFrame] = {}
    for csv_file in csv_files:
            df = pd_read_csv(csv_file)
            csv_df[Get_Basename_Without_Extension(csv_file)] = df
    return csv_df

def Write_Json_Files(ingnition_json: Dict[str, Any], dir: str) -> None:
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists
    from json import dump as json_dump
    out_dir = f'{dir}/json'
    if not os_path_exists(out_dir):
        os_makedirs(out_dir)
    for key in ingnition_json:
        with open(os_path_join(out_dir, f"{ingnition_json[key]['name']}.json"), 'w') as f:
            json_dump(ingnition_json[key], f, indent=4)

def Write_Address_CSV(address_csv: Dict[str, Any], dir: str) -> None:
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists

    out_dir = f'{dir}/csv'
    if not os_path_exists(out_dir):
        os_makedirs(out_dir)
    for key, df in address_csv.items():
        df.to_csv(os_path_join(out_dir, f'{key}.csv'), index=False)

    
def Find_Row_By_Tag_Name(df: pd_DataFrame, tag_name: str) -> pd_DataFrame:
    return df[df['Tag Name'] == tag_name]

def Extract_Tag_Name(opc_item_path: str) -> str:
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def Extract_Area_And_Offset(address: str) -> Tuple[str, str]:
    from re import search as re_search
    match = re_search(r'\d+', address)
    if match:
        if 'X' in address:
            area = 'X'
            hex_address = address.split('X')[1]
            # Convert hex to decimal
            offset = str(int(hex_address.lstrip('0') or '0', 16))
            return area, offset
        else:
            first_number_index = match.start()
            area = address[:first_number_index]
            offset = address[first_number_index:].lstrip('0') or '0'
            return area, offset
    else:
        exit(f"Invalid address format: {address}")


def Extract_Offset_And_Array_Size(offset: str) -> Tuple[str, str]:
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]
        return offset, array_size
    return offset, ''