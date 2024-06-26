#!/usr/bin/env python


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
                    log_messages.append(f"{os_path_basename(json_file).split('.')[0]}.json Changed to {new_file_name}.json")
                    break
        else:
            new_file_name = os_path_basename(json_file).split('.')[0]

        ignition_json[new_file_name] = json_structure
        ignition_json[new_file_name]["name"] = new_file_name

    for json_file in json_files:
        read_file(json_file)

    if logger:
        logger.change_log_file(os_path_join('files', 'logs', 'mitsubishi', 'name_change.log'))
        logger.set_level('NAME_CHANGE')
        for message in log_messages:
            logger.log_message(message, 'NAME_CHANGE')

    return ignition_json

def get_dict_of_dfs_from_csv_files(csv_files):
    from pandas import read_csv as pd_read_csv
    import os

    csv_df = {}
    for csv_file in csv_files:
        with open(csv_file, 'r') as f:
            csv_df[get_basename_without_extension(csv_file)] = pd_read_csv(f)

    # only do this is the os is windows
    if os.name == 'nt':
        for df in csv_df.values():
            for key in df.keys():
                # remove all non alphanumeric characters from key
                new_key = remove_invalid_tag_name_characters(key)
                df[new_key] = df.pop(key)
    
    return csv_df


def write_json_files(json_data, output_dir):
    from json import dump as json_dump
    from os import makedirs as os_makedirs


    output_dir = f'{output_dir}/json'
    
    os_makedirs(output_dir, exist_ok=True)
    def write_file(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json_dump(data, f, indent=4)
                

    for key, data in json_data.items():
        write_file(f"{output_dir}/{key}.json", data)

def write_csv_files(address_csv, dir) -> None:
    from os.path import join as os_path_join
    from os import makedirs as os_makedirs


    out_dir = f'{dir}/csv'

    os_makedirs(out_dir, exist_ok=True)

    for key, df in address_csv.items():
        df.to_csv(os_path_join(out_dir, f'{key}.csv'), index=False)