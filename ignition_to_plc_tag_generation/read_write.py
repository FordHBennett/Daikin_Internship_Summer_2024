import os
import json
import pandas as pd
from typing import Dict, List, Any
from .helpers import Get_Basename_Without_Extension, Get_All_Keys

def Read_Json_Files(json_files: List[str]) -> Dict[str, Dict[str, Any]]:
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
    csv_df: Dict[str, pd.DataFrame] = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        csv_df[Get_Basename_Without_Extension(csv_file)] = df
    return csv_df

def Write_Json_Files(ignition_json: Dict[str, Any], dir: str) -> None:
    out_dir = os.path.join('output_files', dir, 'ignition_client_tags_json')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key in ignition_json:
        with open(os.path.join(out_dir, f"{ignition_json[key]['name']}.json"), 'w') as f:
            json.dump(ignition_json[key], f, indent=4)

def Write_Address_CSV(address_csv: Dict[str, Any], dir: str) -> None:
    dir = dir.split(os.path.sep)[1]
    out_dir = os.path.join('output_files', dir, 'ignition_gateway_device_address_csv')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for key, df in address_csv.items():
        df.to_csv(os.path.join(out_dir, f'{key}.csv'), index=False)
