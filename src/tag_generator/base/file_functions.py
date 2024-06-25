#!/usr/bin/env python

# from typing import List, Dict, Any
# from memory_profiler import profile


# import json


import csv


def get_basename_without_extension(file_path):
    from os.path import basename as os_path_basename
    from os.path import splitext as os_path_splitext

    """
    Returns the base name of a file path without the file extension.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The base name of the file without the extension.
    """

    name, _ = os_path_splitext(os_path_basename(file_path))
    return name

def get_all_json_files(dir):

    from os import walk as os_walk
    json_paths = []

    def recursive_get_json_paths(directory) -> None:
        from os.path import join as os_path_join

        for root, _, files in os_walk(directory):
            for file in files:
                if file.endswith('.json'):
                    json_paths.append(os_path_join(root, file).encode('unicode-escape').decode())


    recursive_get_json_paths(dir)
    return tuple(json_paths)

def get_all_csv_files(dir):
    from os.path import join as os_path_join
    from os import walk as os_walk


    csv_paths= []

    def recursive_get_csv_files(directory) -> None:
        for root, _, files in os_walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    csv_paths.append(os_path_join(root, file).encode('unicode-escape').decode())

    recursive_get_csv_files(dir)
    return tuple(csv_paths)

def get_dict_from_json_files(json_files, is_test=False, logger=None):
    from json import load as json_load
    from os.path import basename as os_path_basename
    # from concurrent.futures import ThreadPoolExecutor
    # import mmap
    # import gc

    log_messages = []
    def read_file(json_file):
        json_structure = {}
        with open(json_file, 'r', encoding='utf-8') as f:
            json_structure = json_load(f)
        
        new_file_name = r''
        if not is_test:
            for key in json_structure["tags"]:
                if 'opcItemPath' in key:
                    new_file_name =  key["opcItemPath"][key["opcItemPath"].rfind("=") + 1:key["opcItemPath"].find(".")]
                    log_messages.append(f"{os_path_basename(json_file)[:os_path_basename(json_file).find('.')]} Changed to {new_file_name}")
                    break
        else:
            new_file_name = os_path_basename(json_file)[:os_path_basename(json_file).find('.')]

        ignition_json[new_file_name] = json_structure
        ignition_json[new_file_name]["name"] = new_file_name

    # ignition_json: Dict[str, Any] = {}
    # with ThreadPoolExecutor() as executor:
    #     list(executor.map(read_file, json_files))

    ignition_json = {}
    for json_file in json_files:
        read_file(json_file)


    if logger:
        from os.path import join as os_path_join
        logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'name_change.log'))
        logger.set_level('NAME_CHANGE')
        for message in log_messages:
            logger.log_message(message, 'NAME_CHANGE')
    
    # gc.collect()
    return ignition_json

# @profile
def get_dict_of_dfs_from_csv_files(csv_files):
    from pandas import read_csv as pd_read_csv
    # import mmap    

    csv_df = {}
    for csv_file in csv_files:
        with open(csv_file, 'r') as f:
            csv_df[get_basename_without_extension(csv_file)] = pd_read_csv(f)
    return csv_df


def write_json_files(json_data, output_dir):
    # from concurrent.futures import ThreadPoolExecutor
    from json import dump as json_dump
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists

    output_dir = f'{output_dir}/json'
    if not os_path_exists(output_dir):
        os_makedirs(output_dir)
    def write_file(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json_dump(data, f, indent=4)
                

    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(write_file, f"{output_dir}/{key}.json", data)
    #         for key, data in json_data.items()
    #     ]
    #     for future in futures:
    #         future.result()
    for key, data in json_data.items():
        write_file(f"{output_dir}/{key}.json", data)

def write_csv_files(address_csv, dir) -> None:
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs
    from os.path import exists as os_path_exists

    # from concurrent.futures import ThreadPoolExecutor

    out_dir = f'{dir}/csv'
    if not os_path_exists(out_dir):
        os_makedirs(out_dir)
    # with ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(df.to_csv, os_path_join(out_dir, f'{key}.csv'), index=False)
    #         for key, df in address_csv.items()
    #     ]
    #     for future in futures:
    #         future.result()
    for key, df in address_csv.items():
        df.to_csv(os_path_join(out_dir, f'{key}.csv'), index=False)