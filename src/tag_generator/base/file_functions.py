#!/usr/bin/env python


import json
from math import log
from .tag_functions import remove_invalid_tag_name_characters


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


def get_all_files(dir, extension):
    """
    Recursively retrieves all files with a specific extension in a given directory.

    Args:
        dir (str): The directory to search for files.
        extension (str): The file extension to filter files.

    Returns:
        tuple: A tuple containing the paths of all files found.

    Raises:
        FileNotFoundError: If no files are found with the specified extension in the given directory.
    """
    import os
    paths = []

    def recursive_get_files(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    paths.append(os.path.join(root, file))

    recursive_get_files(dir)

    if not paths:
        raise FileNotFoundError(f"No files found with extension {extension} in {dir}")
    return tuple(paths)

def get_dict_from_json_files(json_files, is_test=False, logger=None):
    """
    Reads a list of JSON files and returns a dictionary containing the contents of the files. 
    Changes the name of the JSON file to the name of the tag in the JSON file.
    Logs the changes made to the file names.

    Args:
        json_files (list): A list of JSON file paths.
        is_test (bool, optional): Indicates whether the function is being used for testing purposes. Defaults to False.
        logger (Logger, optional): An instance of a logger object for logging purposes. Defaults to None.

    Returns:
        dict: A dictionary containing the contents of the JSON files, with the file names as keys.

    """
    from json import load as json_load
    from os.path import basename as os_path_basename, join as os_path_join

    log_messages = []
    ignition_json = {}

    def read_file(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            json_structure = json_load(f)

        new_file_name = ''
        if not is_test:
            for key in json_structure.get("tags", []):
                if 'opcItemPath' in key:
                    new_file_name = key["opcItemPath"].split('=')[-1].split('.')[0]
                    break
            log_messages.append(f"{os_path_basename(json_file)} Changed to {json_structure['name']}.json")
            json_file = get_basename_without_extension(json_file)
        else:
            new_file_name = os_path_basename(json_file).split('.')[0]

        ignition_json[new_file_name] = json_structure

    for json_file in json_files:
        read_file(json_file)

    if logger:
        logger.change_log_file(os_path_join('files', 'logs', 'mitsubishi', 'name_change.log'))
        logger.set_level('NAME_CHANGE')
        for message in log_messages:
            logger.log_message(message, 'NAME_CHANGE')

    return ignition_json

def get_dict_of_dfs_from_csv_files(csv_files):
    """
    Reads CSV files and returns a dictionary of pandas DataFrames.

    Parameters:
    csv_files (list): A list of file paths to the CSV files.

    Returns:
    dict: A dictionary where the keys are the base names of the CSV files without the file extension,
          and the values are pandas DataFrames containing the data from the CSV files.
    """
    from pandas import read_csv as pd_read_csv
    import os

    csv_df = {}
    for csv_file in csv_files:
        with open(csv_file, 'r') as f:
            csv_df[get_basename_without_extension(csv_file)] = pd_read_csv(f)

    # Remove invalid characters from tag names if running on Windows
    if os.name == 'nt':
        for df in csv_df.values():
            for key in df.keys():
                new_key = remove_invalid_tag_name_characters(key)
                df[new_key] = df.pop(key)
    
    return csv_df


def write_json_files(json_data, output_dir):
    """
    Write JSON files to the the subdirectory json in the specified output directory.

    Args:
        json_data (dict): A dictionary containing the JSON data to be written.
        output_dir (str): The directory where the JSON files will be written.

    Returns:
        None
    """
    from json import dump as json_dump
    from os import makedirs as os_makedirs

    output_dir = f'{output_dir}/json'
    
    os_makedirs(output_dir, exist_ok=True)
    def write_file(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json_dump(data, f, indent=4)
                

    for key, data in json_data.items():
        write_file(f"{output_dir}/{json_data[key]['name']}.json", data)

def write_csv_files(address_csv, dir) -> None:
    """
    Write DataFrame objects to CSV files in the subdirectory csv in the specified directory.

    Args:
        address_csv (dict): A dictionary containing DataFrame objects as values, where the keys represent the file names.
        dir (str): The directory path where the CSV files will be saved.

    Returns:
        None
    """
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs

    out_dir = f'{dir}/csv'

    os_makedirs(out_dir, exist_ok=True)

    for key, df in address_csv.items():
        df.to_csv(os_path_join(out_dir, f'{key}.csv'), index=False)

