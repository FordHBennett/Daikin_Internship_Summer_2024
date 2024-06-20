from typing import List, Dict, Any

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

def Get_ALL_JSON_Paths(dir: str) -> List[str]:
    from os import walk as os_walk
    from os.path import join as os_path_join
    json_paths: List[str] = []

    def Recursive_Get_JSON_Paths(directory: str) -> None:
        for root, dirs, files in os_walk(directory):
            for file in files:
                if file.endswith('.json'):
                    json_paths.append(os_path_join(root, file))
            for folder in dirs:
                Recursive_Get_JSON_Paths(os_path_join(root, folder))

    Recursive_Get_JSON_Paths(dir)
    return json_paths

def Get_ALL_CSV_Paths(dir: str) -> List[str]:
    from os import walk as os_walk
    from os.path import join as os_path_join
    csv_paths: List[str] = []

    def Recursive_Get_CSV_Paths(directory: str) -> None:
        for root, dirs, files in os_walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    csv_paths.append(os_path_join(root, file))
            for folder in dirs:
                Recursive_Get_CSV_Paths(os_path_join(root, folder))

    Recursive_Get_CSV_Paths(dir)
    return csv_paths

def Read_Json_Files(json_files: List[str], is_test=False) -> Dict[str, Dict[str, Any]]:
    from json import load as json_load
    from os.path import basename as os_path_basename
    from copy import deepcopy as copy_deepcopy
    from concurrent.futures import ThreadPoolExecutor
    from base.base_functions import log_message
    ignition_json: Dict[str, Any] = {}

    def read_file(json_file):
        json_structure = {}
        with open(json_file, 'r') as f:
            json_structure = json_load(f)
        
        new_file_name = ''
        if not is_test:
            for key in json_structure["tags"]:
                if 'opcItemPath' in key:
                    new_file_name =  copy_deepcopy(key["opcItemPath"][key["opcItemPath"].rfind("=") + 1:key["opcItemPath"].find(".")])
                    log_message(f"{os_path_basename(json_file)[:os_path_basename(json_file).find('.')]} Changed to {new_file_name}", 'info')
                    break
        else:
            new_file_name = os_path_basename(json_file)[:os_path_basename(json_file).find('.')]

        ignition_json[new_file_name] = json_structure
        ignition_json[new_file_name]["name"] = new_file_name
    
    with ThreadPoolExecutor() as executor:
        list(executor.map(read_file, json_files))
    return ignition_json


def Read_CSV_Files(csv_files):
    from pandas import read_csv as pd_read_csv    
    from pandas import DataFrame as pd_DataFrame

    csv_df: Dict[str, pd_DataFrame] = {}
    for csv_file in csv_files:
            df = pd_read_csv(csv_file)
            csv_df[Get_Basename_Without_Extension(csv_file)] = df
    return csv_df


def Write_Json_Files(json_data, output_dir):
    from concurrent.futures import ThreadPoolExecutor
    from json import dump as json_dump
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists

    output_dir = f'{output_dir}/json'
    if not os_path_exists(output_dir):
        os_makedirs(output_dir)
    def write_file(file_path, data):
        with open(file_path, 'w') as f:
            json_dump(data, f, indent=4)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(write_file, f"{output_dir}/{key}.json", data)
            for key, data in json_data.items()
        ]
        for future in futures:
            future.result()

def Write_Address_CSV(address_csv: Dict[str, Any], dir: str) -> None:
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists
    from concurrent.futures import ThreadPoolExecutor

    out_dir = f'{dir}/csv'
    if not os_path_exists(out_dir):
        os_makedirs(out_dir)
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(df.to_csv, os_path_join(out_dir, f'{key}.csv'), index=False)
            for key, df in address_csv.items()
        ]
        for future in futures:
            future.result()