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

    return os.path.splitext(os.path.basename(file_path))[0]


def get_all_files(dir: os.path, extension: str) -> list:
    """
    Get a list of all files with a specific extension in a directory and its subdirectories.

    Args:
        dir (os.path): The directory to search for files.
        extension (str): The file extension to filter by.

    Returns:
        list: A list of file paths that match the given extension.

    Raises:
        FileNotFoundError: If no files are found with the given extension in the specified directory.
    """

    paths: list = list(
        os.path.join(root, file)
        for root, _, files in os.walk(dir)
        for file in files if file.endswith(extension)
    )

    if not paths:
        raise FileNotFoundError(f"No files found with extension {extension} in {dir}")
    return paths

def get_dict_from_json_files(
    json_files:list, 
    is_test:bool=False, 
    logger:object=None,
    device:str=None) -> dict:
    """
    Reads a list of JSON files and returns a dictionary containing the contents of each file.

    Args:
        json_files (list): A list of paths to JSON files.
        is_test (bool, optional): Indicates whether the function is being used for testing purposes. Defaults to False.
        logger (object, optional): An optional logger object for logging messages. Defaults to None.
        device (str, optional): An optional device identifier. Defaults to None.

    Returns:
        dict: A dictionary containing the contents of each JSON file, with the file names as keys.

    """
    # log_messages = []
    ignition_json = {}
    # found_device_name_flag = False
    # def read_file(json_file) -> None:
    #     """
    #     Reads a JSON file and returns its contents as a dictionary.

    #     Args:
    #         json_file (str): The path to the JSON file.

    #     Returns:
            

    #     Raises:
    #         FileNotFoundError: If the specified JSON file does not exist.
    #         JSONDecodeError: If the JSON file is not valid and cannot be decoded.

    #     """
    #     with open(json_file, 'r', encoding='utf-8') as f:
    #         json_structure = json.load(f)

        
    #     get_new_file_name(json_file, json_structure['tags'], json_structure)

    # def get_new_file_name(json_file, tags, json_structure):
    #     new_file_name = ''
    #     nonlocal found_device_name_flag
    #     if not is_test:
    #         for tag in tags:
    #             if found_device_name_flag:
    #                 return
    #             if ('opcItemPath' in tag and ("ns=2;s=" in tag['opcItemPath'] or 'ThingWorx' in tag['opcItemPath'])):
    #                 opc_path = tag['opcItemPath']
    #                 new_file_name = opc_path.split('=')[-1].split('.')[0]
    #                 log_messages.append(f"{os.path.basename(json_file)} Changed to {new_file_name}.json")
    #                 found_device_name_flag = True
    #                 break
    #             elif 'tags' in tag:
    #                 get_new_file_name(json_file, tag['tags'], json_structure)
    #     else:
    #         new_file_name = os.path.basename(json_file).split('.')[0]

    #     # old_key = get_basename_without_extension(json_file)
    #     ignition_json[new_file_name] = json_structure
    #     return 

    # for json_file in json_files:
    #     read_file(json_file)

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_structure = json.load(f)
        ignition_json[get_basename_without_extension(json_file)] = json_structure

    # if logger:
    #     for message in log_messages:
    #         logger.log_message(message, device, 'NAME_CHANGE')

    return ignition_json

def get_dict_of_dfs_from_csv_files(csv_files:list, read_csv) -> dict:
    """
    Reads multiple CSV files and returns a dictionary of pandas DataFrames.

    Args:
        csv_files (list): A list of file paths to the CSV files.
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
                new_key = constants.TAG_NAME_PATTERN.sub('', key)
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
            print(f"Error writing file: {file_path}")
            print(e)
            
    
    write_file(f"{os.path.join(output_dir, next(iter(json_data)))}.json", next(iter(json_data.values())))

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
        key, value = next(iter(address_csv.items()))
        value.to_csv(os.path.join(out_dir, f'{key}.csv'), index=False)
    except Exception as e:
        print(f"Error writing file: {next(iter(address_csv))}.csv")
        print(e)


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
