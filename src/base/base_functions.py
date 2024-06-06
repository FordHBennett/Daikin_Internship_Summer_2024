#!/usr/bin/env python

import os
import json
import pandas as pd
from typing import Dict, Any, List

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

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    """
    Finds rows in a DataFrame based on a given tag name.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search in.
    - tag_name (str): The tag name to search for.

    Returns:
    - pd.DataFrame: A DataFrame containing the rows that match the tag name.
    """
    condition = (df.iloc[:, 0] == tag_name) | (df.iloc[:, 0].apply(lambda x: x.split('.')[-1]) == tag_name)
    return df.loc[condition]

def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
    """
    Recursively extracts all keys from a JSON structure.

    Args:
        json_structure (Any): The JSON structure to extract keys from.

    Returns:
        Dict[str, Any]: A dictionary containing all the extracted keys.
    """
    def Recursive_Extract_Keys(obj: Any, parent_key: str = '', keys_set: set = None) -> Dict[str, Any]:
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
            for i, item in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                if full_key not in keys_set:
                    keys_set.add(full_key)
                    keys.update(Recursive_Extract_Keys(item, full_key, keys_set))
        else:
            return None
        return keys

    return Recursive_Extract_Keys(json_structure)


def Get_ALL_JSON_Paths(dir: str) -> List[str]:
    """
    Get all JSON file paths within a directory and its subdirectories.

    Args:
        dir (str): The directory path to search for JSON files.

    Returns:
        List[str]: A list of JSON file paths found within the directory and its subdirectories.
    """
    json_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.json'):
                json_paths.append(os.path.join(root, file))
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    """
    Get all the paths of CSV files within a directory and its subdirectories.

    Args:
        dir (str): The directory path to search for CSV files.

    Returns:
        List[str]: A list of paths to CSV files found within the directory and its subdirectories.
    """
    csv_paths: List[str] = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), dir)):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths


def Read_Json_Files(json_files: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Reads a list of JSON files and returns a dictionary containing the contents of each file.

    Args:
        json_files (List[str]): A list of file paths to JSON files.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary where the keys are the base names of the JSON files
        (without the file extension) and the values are the contents of each JSON file.

    """
    templete_json: Dict[str, Any] = {}
    ignition_json: Dict[str, Any] = {}
    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_structure = json.load(f)
            keys = Get_All_Keys(json_structure)
            templete_json.update(keys)
            ignition_json[Get_Basename_Without_Extension(json_file)] = json_structure
    return ignition_json

def Read_CSV_Files(csv_files: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Read multiple CSV files and return a dictionary of DataFrames.

        Parameters:
        - csv_files (List[str]): A list of file paths to the CSV files.

        Returns:
        - csv_df (Dict[str, pd.DataFrame]): A dictionary where the keys are the base names of the CSV files
            (without the file extension) and the values are the corresponding DataFrames read from the CSV files.
        """
        csv_df: Dict[str, pd.DataFrame] = {}
        for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                csv_df[Get_Basename_Without_Extension(csv_file)] = df
        return csv_df

def Write_Json_Files(ignition_json: Dict[str, Any], dir: str) -> None:
    """
    Write the given Ignition JSON data to individual JSON files.

    Args:
        ignition_json (Dict[str, Any]): The Ignition JSON data to be written.
        dir (str): The directory where the output files will be saved.

    Returns:
        None
    """
    out_dir = os.path.join('output_files', dir, 'ignition_client_tags_json')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key in ignition_json:
        with open(os.path.join(out_dir, f"{ignition_json[key]['name']}.json"), 'w') as f:
            json.dump(ignition_json[key], f, indent=4)

def Write_Address_CSV(address_csv: Dict[str, Any], dir: str) -> None:
    """
    Write the address CSV files to the specified directory.

    Args:
        address_csv (Dict[str, Any]): A dictionary containing the address CSV data.
        dir (str): The directory where the CSV files will be written.

    Returns:
        None
    """
    dir = dir.split(os.path.sep)[1]
    out_dir = os.path.join('output_files', dir, 'ignition_gateway_device_address_csv')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key, df in address_csv.items():
        df.to_csv(os.path.join(out_dir, f'{key}.csv'), index=False)

