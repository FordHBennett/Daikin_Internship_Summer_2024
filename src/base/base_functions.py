#!/usr/bin/env python

import os
import json
import pandas as pd
from typing import Dict, Any, List, Tuple
import re
import logging

logging.basicConfig(
    filename='tag_generation.log',  # Log file path
    level=logging.INFO,          # Logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    style='%'  # String formatting style
)

def log_message(message: str, level: str = 'info'):
    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'debug':
        logging.debug(message)
    else:
        logging.info(message)  


def Get_Basename_Without_Extension(file_path: str) -> str:
    """
    Returns the base name of a file path without the file extension.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The base name of the file without the extension.
    """
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return name

def Remove_Invalid_Tag_Name_Characters(tag_name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9-_ .]', '', tag_name)

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

    dir = os.path.join(dir, 'ignition_json')
    json_paths: List[str] = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith('.json'):
                json_paths.append(os.path.join(root, file))
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    dir = os.path.join(dir, 'csv')
    csv_paths: List[str] = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

def Read_Json_Files(json_files: List[str]) -> Dict[str, Dict[str, Any]]:

    templete_json: Dict[str, Any] = {}
    ignition_json: Dict[str, Any] = {}
    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_structure = json.load(f)
            keys = Get_All_Keys(json_structure)
            templete_json.update(keys)
            for key in json_structure["tags"]:
                if 'opcItemPath' in key:
                    json_file =  key["opcItemPath"][key["opcItemPath"].rfind("=") + 1:key["opcItemPath"].find(".")]
                    break
            ignition_json[json_file] = json_structure
            ignition_json[json_file]["name"] = json_file
    return ignition_json

def Read_CSV_Files(csv_files: List[str]) -> Dict[str, pd.DataFrame]:

        csv_df: Dict[str, pd.DataFrame] = {}
        for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                csv_df[Get_Basename_Without_Extension(csv_file)] = df
        return csv_df

def Write_Json_Files(ignition_json: Dict[str, Any], dir: str) -> None:

    out_dir = f'{dir}/ignition_json'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key in ignition_json:
        with open(os.path.join(out_dir, f"{ignition_json[key]['name']}.json"), 'w') as f:
            json.dump(ignition_json[key], f, indent=4)

def Write_Address_CSV(address_csv: Dict[str, Any], dir: str) -> None:

    out_dir = f'{dir}/csv'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key, df in address_csv.items():
        df.to_csv(os.path.join(out_dir, f'{key}.csv'), index=False)

def Reset_Tag_Builder_Properties(tag_builder_properties: Dict[str, Any]):
    for property in tag_builder_properties:
        if isinstance(tag_builder_properties[property], dict):
            Reset_Tag_Builder_Properties(tag_builder_properties[property])
        elif isinstance(tag_builder_properties[property], list):
            for item in tag_builder_properties[property]:
                Reset_Tag_Builder_Properties(item)
        elif property == 'is_tag_from_csv_flag':
            tag_builder_properties[property] = False
        else:
            tag_builder_properties[property] = ''
    
def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    return df[df['Tag Name'] == tag_name]

def Extract_Tag_Name(opc_item_path: str) -> str:
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def Extract_Area_And_Offset(address: str) -> Tuple[str, str]:
    match = re.search(r'\d+', address)
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
