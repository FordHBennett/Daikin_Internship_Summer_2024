from os import path
from numpy import add
import pandas as pd
from typing import Dict, Any
from .helpers import Find_Row_By_Tag_Name

def Modify_Tags_For_Direct_Driver_Communication(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> None:
    """
    Modifies tags for direct driver communication based on the provided CSV data and Ignition JSON.

    Args:
        csv_df (Dict[str, pd.DataFrame]): A dictionary containing CSV data as pandas DataFrames.
        ignition_json (Dict[str, Any]): A dictionary containing Ignition JSON data.

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

                    row = Find_Row_By_Tag_Name(df, tag_name)
                    if not row.empty:
                        tags["name"] = tag_name
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
                            if 'SH' in area:
                                array_size = f"[{array_size}]"
                                if tags['dataType'] == 'Int2':
                                    tags['dataType'] = 'Short Array'
                                elif tags['dataType'] == 'Int4':
                                    tags['dataType'] = 'Integer Array'
                            
                        tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}"

                        tags['opcServer'] = 'Ignition OPC UA Server'
                        tags['tagGroup'] = 'default'
                    else:
                        print(f"Tag {tag_name} not found in {key}.csv")

def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Generate the address CSV file based on the provided CSV DataFrame and Ignition JSON data.

    Args:
        csv_df (Dict[str, pd.DataFrame]): A dictionary containing CSV DataFrames for each key.
        ignition_json (Dict[str, Any]): A dictionary containing Ignition JSON data.

    Returns:
        Dict[str, pd.DataFrame]: A dictionary containing the generated address CSV DataFrames for each key.
    """
    address_csv: Dict[str, pd.DataFrame] = {}
    for key in ignition_json:
        dfs = []
        for tags in ignition_json[key]['tags']:
            if 'dataType' in tags:
                if tags['dataType'] == 'Int2':
                    path_data_type = 'Int16'
                elif tags['dataType'] == 'Int4':
                    path_data_type = 'Int32'
                tag_name = tags['name']
                row = Find_Row_By_Tag_Name(csv_df[key], tag_name)
                if not row.empty:
                    address = row.iloc[0, 1]
                    area = address[:address.find('0')]
                    offset = address[address.find('0'):].lstrip('0') or '0'


                    array_size = ''
                    if 'SH' in area:
                        area = area.replace('SH', '')
                        path_data_type = 'String'
                    if "." in offset:
                        array_size = offset.split('.')[1]
                        array_size = array_size.lstrip('0')
                        offset = offset.split('.')[0]
                        if 'String'not in path_data_type:
                            array_size = f"[{array_size}]"

                    address = f"{area}<{path_data_type}{array_size}>{offset}"
                    

                    df = pd.DataFrame({'tag_name': [tag_name], 'address': [address]})
                    dfs.append(df)
        if dfs:
            address_csv[key] = pd.concat(dfs, ignore_index=True)

    # sort the rows by tag_name
    for key in address_csv:
        address_csv[key] = address_csv[key].sort_values(by='tag_name', ignore_index=True)

    return address_csv
