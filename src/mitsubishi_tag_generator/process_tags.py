#!/usr/bin/env python

import pandas as pd
from typing import Dict, Any, List
import re

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    return df[df['Tag Name'] == tag_name]

def Convert_To_Path_Data_Type(data_type: str) -> str:
    if data_type == 'Short' or data_type == 'Int2':
        return 'Int16'
    elif data_type == 'Integer' or data_type == 'Int4':
        return 'Int32'
    elif data_type == 'Boolean':
        return 'Bool'
    elif data_type == 'BCD':
        return 'Float'
    return data_type

def Extract_Area_Offset(address: str) -> tuple[str, str]:
    match = re.search(r'\d+', address)
    if match:
        first_number_index = match.start()
        area = address[:first_number_index]
        offset = address[first_number_index:].lstrip('0') or '0'
    else:
        exit(f"Invalid address format: {address}")

    return area, offset

def Convert_Area_To_Mitsubishi_Format(area: str, path_data_type: str):
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    return area, path_data_type

def Convert_Array_Size_To_Mitsubishi_Format(offset:str, path_data_type: str):
    array_size = ''
    data_type = ''
    if "." in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]
        if 'String' not in path_data_type:
            array_size = f"[{array_size}]"
            data_type = "String"
    return array_size, data_type, offset

def Create_New_Tag(tag_name: str, parent_tag_name: str, ignition_name: str, area: str, path_data_type: str, array_size: str, offset: str, data_type: str, tags: Dict[str, Any]) -> Dict[str, Any]:
    new_tag = {
        "name": tag_name[tag_name.find('.')+1:],
        "opcItemPath": f"ns=1;s=[{ignition_name}/{parent_tag_name}]{area}<{path_data_type}{array_size}>{offset}",
        "opcServer": 'Ignition OPC UA Server',
        "tagGroup": 'default'  # Remove once this in production
    }
    if 'dataType' in tags:
        new_tag['dataType'] = data_type
    if 'tagType' in tags:
        new_tag['tagType'] = tags['tagType']
    if 'historyProvider' in tags:
        new_tag['historyProvider'] = tags['historyProvider']
    if 'historicalDeadband' in tags:
        new_tag['historicalDeadband'] = tags['historicalDeadband']
    if 'historicalDeadbandStyle' in tags:
        new_tag['historicalDeadbandStyle'] = tags['historicalDeadbandStyle']
    return new_tag

def Add_To_Existing_Tag(tag_list: List[Dict[str, Any]], parent_tag_name: str, new_tag: Dict[str, Any]) -> None:
    for tag in tag_list:
        if tag['name'] == parent_tag_name:
            if 'tags' not in tag:
                tag['tags'] = []
            tag['tags'].append(new_tag)
            return
    # If the parent tag does not exist, create it
    parent_tag = {
        "name": parent_tag_name,
        "tag_type": "Folder",
        "tags": [new_tag]
    }
    tag_list.append(parent_tag)

def Process_Tag_Name(ignition_json: Dict[str, Any], key: str, tag_name: str, area: str, path_data_type: str, data_type: str, tags: Dict[str, Any], array_size: str, offset: str) -> None:
    name_parts = tag_name.split('.')
    current_tags = ignition_json[key]['tags']
    
    for i in range(len(name_parts) - 1):
        part = name_parts[i]
        found = False
        for tag in current_tags:
            if tag['name'] == part:
                if 'tags' not in tag:
                    tag['tags'] = []
                current_tags = tag['tags']
                found = True
                break
        if not found:
            new_folder_tag = {
                "name": part,
                "tag_type": "Folder",
                "tags": []
            }
            current_tags.append(new_folder_tag)
            current_tags = new_folder_tag['tags']
    
    final_tag_name = name_parts[-1]
    parent_tag_name = name_parts[-2]
    new_tag = Create_New_Tag(final_tag_name,parent_tag_name, ignition_json[key]['name'], area, path_data_type, array_size, offset, data_type, tags)
    current_tags.append(new_tag)


def Modify_Tags_For_Direct_Driver_Communication(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, Any]:
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
            existing_tag_names = set()
            tags_to_remove = []
            for tags in ignition_json[key]['tags']:
                if 'opcItemPath' in tags:
                    path_data_type = ''
                    if 'dataType' in tags:
                        data_type = tags['dataType']
                        path_data_type = Convert_To_Path_Data_Type(data_type)
                        dummy_name = tags['opcItemPath'][tags['opcItemPath'].find('.')+1:]
                        tag_name = dummy_name[dummy_name.find('.')+1:]
                        existing_tag_names.add(tag_name)

                        row = Find_Row_By_Tag_Name(df, tag_name)
                        if not row.empty:
                            address = row.iloc[0, 1]
                            area, offset = Extract_Area_Offset(address)
                            area, path_data_type = Convert_Area_To_Mitsubishi_Format(area, path_data_type)
                            array_size, data_type, offset = Convert_Array_Size_To_Mitsubishi_Format(offset, path_data_type)
                            if data_type == "":
                                data_type = tags['dataType']
                            if '.' in tag_name:
                                Process_Tag_Name(ignition_json, key, tag_name, area, path_data_type, data_type, tags, array_size, offset)
                                tags_to_remove.append(tags)
                            else:
                                tags["name"] = tag_name
                                tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}"
                                tags['opcServer'] = 'Ignition OPC UA Server'
                                tags['dataType'] = data_type
                                tags['tagGroup'] = 'default' # Remove once this in production
                        else: 
                            print(f"Could not find tag {tag_name} in CSV file {key}.csv")
            for tag_to_remove in tags_to_remove:
                ignition_json[key]['tags'].remove(tag_to_remove)
            # Process new tags from CSV
            # for index, row in df.iterrows():
            #     tag_name = row['Tag Name']
            #     if tag_name not in existing_tag_names:
            #         existing_tag_names.add(tag_name)
            #         path_data_type = Convert_To_Path_Data_Type(row['Data Type'])
            #         address = row['Address']
            #         area, offset = Extract_Area_Offset(address)
            #         area, path_data_type = Convert_Area_To_Mitsubishi_Format(area, path_data_type)
            #         array_size, row['Data Type'], offset = Convert_Array_Size_To_Mitsubishi_Format(offset, path_data_type, row['Data Type'])
                    
            #         tag_type = ''
            #         tagGroup = ''
            #         historyProvider = ''
            #         historicalDeadband = ''
            #         historicalDeadbandStyle = ''
                    
            #         for dummy_tags in ignition_json[key]['tags']:
            #             if 'tagType' in dummy_tags:
            #                 tag_type = dummy_tags['tagType']
            #                 break
            #         for dummy_tags in ignition_json[key]['tags']:
            #             if 'tagGroup' in dummy_tags:
            #                 tagGroup = dummy_tags['tagGroup']
            #                 break
            #         for dummy_tags in ignition_json[key]['tags']:
            #             if 'historyProvider' in dummy_tags:
            #                 historyProvider = dummy_tags['historyProvider']
            #                 break
            #         for dummy_tags in ignition_json[key]['tags']:
            #             if 'historicalDeadband' in dummy_tags:
            #                 historicalDeadband = dummy_tags['historicalDeadband']
            #                 break   
            #         for dummy_tags in ignition_json[key]['tags']:
            #             if 'historicalDeadbandStyle' in dummy_tags:
            #                 historicalDeadbandStyle = dummy_tags['historicalDeadbandStyle']
            #                 break
                    
            #         new_tag = {
            #             "valueSource": "opc",
            #             "opcItemPath": f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}",
            #             "dataType": row['Data Type'],
            #             "historyProvider": historyProvider,
            #             "historicalDeadband": historicalDeadband,
            #             "historicalDeadbandStyle": historicalDeadbandStyle,
            #             "name": tag_name,
            #             "historyEnabled": False,
            #             "tagGroup": 'default', # Change to tagGroup once in production
            #             "tagType": tag_type,
            #             "opcServer": 'Ignition OPC UA Server',
            #             "enabled": False,
            #         }
            #         ignition_json[key]['tags'].append(new_tag)
    
    return ignition_json
            



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
                path_data_type = tags['dataType']
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
