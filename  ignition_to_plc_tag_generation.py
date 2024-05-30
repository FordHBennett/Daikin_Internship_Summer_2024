# import csv
# from ctypes import addressof
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
    The function `get_all_keys` recursively extracts all keys from a JSON-like structure and returns
    them in a dictionary.

    @param json_structure The `json_structure` parameter in the `get_all_keys` function is expected to
    be a JSON-like data structure of type `Any`, which can be a dictionary, list, or a combination of
    both. The function recursively extracts all keys present in the JSON structure along with their
    hierarchical paths.

    @return The function `get_all_keys` returns a dictionary containing all the keys found in the JSON
    structure provided as input.
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



def Get_ALL_JSON_Paths() -> List[str]:
    """
    The function `Get_ALL_JSON_Paths` retrieves a list of file paths for all JSON files within the
    current working directory and its subdirectories.

    @return A list of file paths for all JSON files found in the current working directory and its
    subdirectories.
    """
    json_paths:List[str] = []
    for root, _, files in os.walk(os.path.join(os.getcwd(), 'json')):
        for file in files:
            json_paths.append(os.path.join(root, file))
    return json_paths



def Get_ALL_CSV_Paths() -> List[str]:
    """
    The function `Get_ALL_CSV_Paths` retrieves a list of file paths for all CSV files within the
    current working directory and its subdirectories.

    @return A list of file paths for all CSV files found in the current working directory and its
    subdirectories.
    """
    csv_paths:List[str] = []
    for root, _, files in os.walk(os.path.join(os.getcwd(), 'csv')):
        for file in files:
            if file.endswith('.csv'):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

def Get_Basename_Without_Extension(file_path: str) -> str:
    """
    The function `Get_Basename_Without_Extension` takes a file path as input and returns the base name
    of the file without the extension.

    @param file_path The function `Get_Basename_Without_Extension` takes a file path as input and
    returns the base name of the file without the extension.

    @return The function `Get_Basename_Without_Extension` takes a file path as input, extracts the base
    name using `os.path.basename`, removes the extension from the base name using `os.path.splitext`,
    and then returns the base name without the extension.
    """
    base_name:os.path = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return name

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    """
    This function finds rows in a DataFrame based on a specified tag name.

    @param df A pandas DataFrame containing data with rows and columns.
    @param tag_name Tag name is a string that represents the name of a tag.

    @return The function `Find_Row_By_Tag_Name` returns a subset of the input DataFrame `df` where the
    first column matches the `tag_name` or the last part of the string after splitting by '.' matches
    the `tag_name`.
    """
    condition = (df.iloc[:, 0] == tag_name) | (df.iloc[:, 0].apply(lambda x: x.split('.')[-1]) == tag_name)
    return df.loc[condition]

def Process_Tags(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> None:
    """
    The function `Process_Tags` processes tag information from a CSV DataFrame and updates data types
    and OPC item paths based on a provided JSON configuration.
    
    @param csv_df The `csv_df` parameter is a dictionary where the keys are strings and the values are
    pandas DataFrames. This dictionary contains data loaded from CSV files.
    @param ignition_json The `ignition_json` parameter in the `Process_Tags` function is expected to be
    a dictionary containing information related to tags in an Ignition system. This dictionary should
    have keys corresponding to the keys in the `csv_df` dictionary. Each key in `ignition_json` should
    have a
    """
    for key, df in csv_df.items():
        if key in ignition_json:
            for tags in ignition_json[key]['tags']:
                if 'dataType' in tags:
                    if tags['dataType'] == 'Int2':
                        tags['dataType'] = 'Int16'
                    elif tags['dataType'] == 'Int4':
                        tags['dataType'] = 'Int32'

                if 'opcItemPath' in tags:
                    tag_name = tags['opcItemPath'].split('.')[-1]
                    tags['tag_name'] = tag_name

                    row = Find_Row_By_Tag_Name(df, tag_name)
                    if not row.empty:
                        address = row.iloc[0, 1]
                        area = address[:address.find('0')]
                        offset = address[address.find('0'):].lstrip('0') or '0'

                        array_size = ''
                        if 'SH' in area:
                            tags['dataType'] = 'String'
                            area = area.replace('SH', '')
                        elif 'M' in area:
                            tags['dataType'] = 'Boolean'

                        if "." in offset:
                            array_size = offset.split('.')[1]
                            array_size = array_size.lstrip('0')
                            offset = offset.split('.')[0]
                            if 'ZR' in area:
                                array_size = f"[{array_size}]"
 


                        tags['opcItemPath'] = f"ns=1;s=[MitsubishiDriver]{area}<{tags.get('dataType', '')}{array_size}>{offset}"
                        tags['opcServer'] = 'Ignition OPC UA Server'


if __name__ == '__main__':
    json_files: List[str] = Get_ALL_JSON_Paths()

    # Dictionary to hold all keys from all JSON files
    templete_json: Dict[str, Any] = {}
    #Dictionary to hold an unmodified version of the JSON file
    ignition_json: Dict[str, Any] = {}

    # Read each JSON file and extract keys
    for json_file in json_files:
        with open(json_file, 'r') as f:
            json_structure = json.load(f)
            keys = Get_All_Keys(json_structure)
            templete_json.update(keys)
            ignition_json[Get_Basename_Without_Extension(json_file)] = json_structure

    csv_files: List[str] = Get_ALL_CSV_Paths()
    csv_df: Dict[str, pd.DataFrame] = {}
    for csv_file in csv_files:
        df: pd.DataFrame = pd.read_csv(csv_file)
        csv_df[Get_Basename_Without_Extension(csv_file)] = df

    Process_Tags(csv_df, ignition_json)

    #write the ignition json files to the ignition json folder
    for key in ignition_json:
        with open(f'modified_json/{key}.json', 'w') as f:
            json.dump(ignition_json[key], f, indent=4)
