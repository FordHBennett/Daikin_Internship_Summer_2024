#!bin/python3

import os
import pandas as pd
from typing import Dict, Any

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
