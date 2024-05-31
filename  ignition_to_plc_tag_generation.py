# import csv
# from ctypes import addressof
import csv
from numpy import add
import pandas as pd
import json
from typing import Dict, Any, List
import os

'''
TODO:
    -Communitcate with the drivers to so I can send to and from ignition
'''

'''
MITSUBISHI DRIVER DOCUMENTATION:
    -https://forum.inductiveautomation.com/t/mitsubishi-driver/73741
    -https://www.docs.inductiveautomation.com/docs/8.1/ignition-modules/opc-ua/opc-ua-drivers/mitsubishi-tcp-driver
'''

'''
DON'T MAKE SENSE: Why do the documentation use csv files for importing/exporting tags but they keep on telling me it using json files
'''

'''
ADDRESSING:
    -R=ZR
    -SH=String
    -M=Boolean
'''

'''
opcItemPath: ns=1;s=[Device]Area{<DataType{[array]}>}Offset{.Bit}
'''

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



def Get_ALL_JSON_Paths(dir) -> List[str]:
    """
    Returns a list of all JSON file paths in a given directory.

    Args:
        dir (str): The directory path where the JSON files are located.

    Returns:
        List[str]: A list of all JSON file paths in the specified directory.
    """
    json_paths: List[str] = []
    for root, _, files in os.walk(os.path.join(os.getcwd(), f'tags_json/{dir}')):
        for file in files:
            json_paths.append(os.path.join(root, file))
    return json_paths



def Get_ALL_CSV_Paths(dir) -> List[str]:
    """
    Retrieves the paths of all CSV files within a specified directory.

    Args:
        dir (str): The directory to search for CSV files.

    Returns:
        List[str]: A list of paths to all CSV files found within the specified directory.
    """
    csv_paths: List[str] = []
    for root, _, files in os.walk(os.path.join(os.getcwd(), f'tags_csv/{dir}')):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

def Get_Basename_Without_Extension(file_path: str) -> str:
    """
    Returns the base name of a file without the extension.

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
        df (pd.DataFrame): The DataFrame to search in.
        tag_name (str): The tag name to search for.

    Returns:
        pd.DataFrame: A DataFrame containing the rows that match the given tag name.
    """
    
    condition = (df.iloc[:, 0] == tag_name) | (df.iloc[:, 0].apply(lambda x: x.split('.')[-1]) == tag_name)
    
    return df.loc[condition]

def Process_Tags(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> None:
    """
    Process the tags from a CSV file and update the corresponding tags in an Ignition JSON.

    Args:
        csv_df (Dict[str, pd.DataFrame]): A dictionary containing CSV dataframes, where the keys represent the file names.
        ignition_json (Dict[str, Any]): A dictionary representing the Ignition JSON.

    Returns:
        None
    """
    for key, df in csv_df.items():
        if key in ignition_json:
            for tags in ignition_json[key]['tags']:
                path_data_type = ''
                if 'dataType' in tags:
                    if tags['dataType'] == 'Int2':
                        path_data_type = 'Int16'
                    elif tags['dataType'] == 'Int4':
                        path_data_type = 'Int32'

                if 'opcItemPath' in tags:
                    tag_name = tags['opcItemPath'].split('.')[-1]
                    tags["name"] = tag_name

                    row = Find_Row_By_Tag_Name(df, tag_name)
                    if not row.empty:
                        address = row.iloc[0, 1]
                        area = address[:address.find('0')]
                        offset = address[address.find('0'):].lstrip('0') or '0'

                        array_size = ''
                        if 'SH' in area:
                            path_data_type = 'String'
                            area = area.replace('SH', '')
                            if "." in offset:
                                array_size = offset.split('.')[1]
                                array_size = array_size.lstrip('0')
                                offset = offset.split('.')[0]
                                if 'ZR' in area:
                                    array_size = f"[{array_size}]"
                            tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}"
                        else:
                            tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{address}"


                        # elif 'M' in area:
                        #     path_data_type = 'Boolean'

                        # if "." in offset:
                        #     array_size = offset.split('.')[1]
                        #     array_size = array_size.lstrip('0')
                        #     offset = offset.split('.')[0]
                        #     if 'ZR' in area:
                        #         array_size = f"[{array_size}]"
 


                        # tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}"
                        # tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{address}"
                        tags['opcServer'] = 'Ignition OPC UA Server'

                        tags['tagGroup'] = 'default'

def Read_Json_Files(json_files: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Reads a list of JSON files and returns their contents as a dictionary.

    Args:
        json_files (List[str]): A list of file paths to JSON files.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary where the keys are the base names of the JSON files
        (without the file extension) and the values are the contents of the JSON files.

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
    Read a list of CSV files and returns them as a dictionary of DataFrames.

    Parameters:
    csv_files (List[str]): A list of file paths to the CSV files.

    Returns:
    Dict[str, pd.DataFrame]: A dictionary where the keys are the base names of the CSV files
    (without the file extension) and the values are the corresponding DataFrames.

    Example:
    >>> csv_files = ['/path/to/file1.csv', '/path/to/file2.csv']
    >>> data = Read_CSV_Files(csv_files)
    >>> print(data)
    {'file1': DataFrame1, 'file2': DataFrame2}
    """
    csv_df: Dict[str, pd.DataFrame] = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        csv_df[Get_Basename_Without_Extension(csv_file)] = df
    return csv_df

def Write_Json_Files(ignition_json: Dict[str, Any]) -> None:
    """
    Write the give json to the `updated_tags` directory.

    Args:
        ignition_json (Dict[str, Any]): The ignition JSON data to be written.

    Returns:
        None
    """
    if not os.path.exists('updated_tags'):
        os.mkdir('updated_tags')
    for key in ignition_json:
        if not os.path.exists(os.path.join('updated_tags','mitsubishi_devices')):
            os.mkdir(os.path.join('updated_tags','mitsubishi_devices'))
        with open(os.path.join('updated_tags','mitsubishi_devices', f"{ignition_json[key]['name']}.json"), 'w') as f:
            json.dump(ignition_json[key], f, indent=4)

def Write_CSV_Files(address_csv: Dict[str, Any]) -> None:
    if not os.path.exists('address_csv'):
        os.mkdir('address_csv')
    for key, df in address_csv.items():
        if not os.path.exists(os.path.join('address_csv','mitsubishi_devices')):
            os.mkdir(os.path.join('address_csv','mitsubishi_devices'))
        df.to_csv(os.path.join('address_csv','mitsubishi_devices', f'{key}.csv'), index=False)

def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    # write the ignition[key]['tags']['name'] to the first column of address_df
    # find the row in csv_df where the first column is equal to the ignition[key]['tags']['name']
    # write the second column of csv_df to the second column of address_df
    address_csv: Dict[str, pd.DataFrame] = {}

    for key in ignition_json:
        dfs = []
        for tags in ignition_json[key]['tags']:
            tag_name = tags['name']
            # print(csv_df[key])
            row = Find_Row_By_Tag_Name(csv_df[key], tag_name)
            if not row.empty:
                address = row.iloc[0, 1]
                df = pd.DataFrame({'tag_name': [tag_name], 'address': [address]})
                dfs.append(df)
        if dfs:
            address_csv[key] = pd.concat(dfs, ignore_index=True)
    
    # delete the first row of the address_df
    for key, df in address_csv.items():
        df.drop(df.index[0], inplace=True)

    return address_csv

def Write_Address_CSV(address_csv: Dict[str, pd.DataFrame]) -> None:
    if not os.path.exists('address_csv'):
        os.mkdir('address_csv')
    os.chdir('address_csv')
    for key, df in address_csv.items():
        if not os.path.exists('mitsubishi_devices'):
            os.mkdir('mitsubishi_devices')
        df.to_csv(os.path.join('mitsubishi_devices', f'{key}.csv'), index=False)

def main():
    dir_list: List[str] = os.listdir('tags_json')
    for dir in dir_list:
        json_files = Get_ALL_JSON_Paths(dir)
        csv_files = Get_ALL_CSV_Paths(dir)

        ignition_json = Read_Json_Files(json_files)
        csv_df = Read_CSV_Files(csv_files)

        Process_Tags(csv_df, ignition_json)
        Write_Json_Files(ignition_json)

        address_csv = Generate_Address_CSV(csv_df, ignition_json)
        Write_Address_CSV(address_csv)

if __name__ == '__main__':
    main()