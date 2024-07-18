#!/usr/bin/env python
import os
import json
def get_basename_without_extension(file_path:os.path)  -> str:
    """
    Returns the base name of a file path without the file extension.

    Args:
        file_path (os.path): The path of the file.

    Returns:
        str: The base name of the file without the extension.
    """
    try:
        return os.path.splitext(os.path.basename(file_path))[0]
    except Exception as e:
        # print(f"Error getting base name without extension: {file_path}")
        # raise e
        raise f"Error getting base name without extension: {file_path} \n ERROR: {e}"


def get_all_files(dir: os.path, extension: str) -> tuple:
    """
    Get a tuple of all files with a specific extension in a directory and its subdirectories.

    Args:
        dir (os.path): The directory to search for files.
        extension (str): The file extension to filter by.

    Returns:
        tuple: A tuple of file paths that match the given extension.

    Raises:
        FileNotFoundError: If no files are found with the given extension in the specified directory.
    """
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"The directory {dir} does not exist")

    paths = tuple(
        os.path.join(root, file)
        for root, _, files in os.walk(dir)
        for file in files if file.endswith(extension)
    )

    if not paths:
        raise FileNotFoundError(f'Check the input/{dir} directory for {extension} files')
    return paths

def get_dict_from_json_files(json_files:tuple) -> dict:
    """
    Reads a tuple of JSON files and returns a dictionary where the keys are the basenames of the files
    (without the file extension) and the values are the corresponding JSON structures.

    Args:
        json_files (tuple): A tuple of file paths to JSON files.

    Returns:
        dict: A dictionary where the keys are the basenames of the files and the values are the JSON structures.

    """
    ignition_json = {}

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_structure = json.load(f)
        except Exception as e:
            raise f"Error reading JSON file: {json_file} \n ERROR: {e}"
        ignition_json[get_basename_without_extension(json_file)] = json_structure

    return ignition_json

def get_dict_of_dfs_from_csv_files(csv_files:tuple, read_csv) -> dict:
    """
    Reads multiple CSV files and returns a dictionary of pandas DataFrames.

    Args:
        csv_files (tuple): A tuple of file paths to the CSV files.
        read_csv (function): A function to read a CSV file and return a pandas DataFrame.

    Returns:
        dict: A dictionary where the keys are the base names of the CSV files without the extension,
              and the values are the corresponding pandas DataFrames.

    """
    csv_df = dict(
        map(
            lambda csv_file: (
                get_basename_without_extension(csv_file), 
                read_csv(csv_file)
            ), 
            csv_files
        )
    )

    # Remove invalid characters from tag names if running on Windows
    if os.name == 'nt':
        import tag_generator.base.constants as constants

        def get_all_keys(dictionary:dict) -> set:
            """
            Recursively retrieves all keys from a nested dictionary.

            Args:
                dictionary (dict): The dictionary to retrieve keys from.

            Returns:
                set: A set of all keys in the dictionary.

            """
            keys = set()
            for key, value in dictionary.items():
                keys.add(key)
                if isinstance(value, dict):
                    keys.update(get_all_keys(value))
            return keys

        for df in csv_df.values():
            all_keys = get_all_keys(df)
            for key in all_keys:
                new_key = constants.TAG_NAME_PATTERN.sub('',key)
                df[new_key] = df.pop(key)
        
    return csv_df


def write_json_files(json_data: dict, output_dir: os.path) -> None:
    """
    Write JSON files from the given JSON data to the specified output directory.

    Args:
        json_data (dict): The JSON data to be written to files.
        output_dir (os.path): The output directory where the JSON files will be saved.

    Returns:
        None
    """
    output_dir = f'{output_dir}/json'
    
    os.makedirs(output_dir, exist_ok=True)
    def write_file(file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise (f"Error writing file: {file_path} \n ERROR: {e}")
            
    first_key, first_value = next(iter(json_data.items()))
    write_file(f"{os.path.join(output_dir, first_key)}.json", first_value)

def write_csv_files(address_csv:dict, dir:os.path) -> None:
    """
    Write DataFrame objects to CSV files in the subdirectory csv in the specified directory.

    Args:
        address_csv (dict): A dictionary containing DataFrame objects as values, where the keys represent the file names.
        dir (os.path): The directory path where the CSV files will be saved.

    Returns:
        None
    """

    out_dir = f'{dir}/csv'

    os.makedirs(out_dir, exist_ok=True)

    try:
        for key, value in address_csv.items():
            value.to_csv(os.path.join(out_dir, f'{key}.csv'), index=False)
    except Exception as e:

        raise f"Error writing file: {next(iter(address_csv))}.csv \n ERROR: {e}"

def clean_files_dir() -> None:
    """
    Clean the files directory by removing the 'logs' and 'output' subdirectories.

    Args:
        path (os.path): The base path of the files directory.

    Returns:
        None
    """
    try:
        import shutil
        shutil.rmtree(os.path.join('files', 'logs'))
        shutil.rmtree(os.path.join('files', 'output'))
    except Exception:
        pass
