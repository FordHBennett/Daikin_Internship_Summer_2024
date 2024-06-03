import os
import pandas as pd
from typing import Dict, Any

def Get_Basename_Without_Extension(file_path: str) -> str:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return name

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    condition = (df.iloc[:, 0] == tag_name) | (df.iloc[:, 0].apply(lambda x: x.split('.')[-1]) == tag_name)
    return df.loc[condition]

def Get_All_Keys(json_structure: Any) -> Dict[str, Any]:
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
