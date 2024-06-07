#!/usr/bin/env python

from curses.ascii import isalpha
from numpy import add
import pandas as pd
from typing import Dict, Any, List, Union
import re
from base.base_functions import Remove_Non_Alphanumeric_Characters

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    return df[df['Tag Name'] == tag_name]

def Convert_To_Path_Data_Type(data_type: str) -> str:
    if data_type == 'Short' or data_type == 'Int2' or data_type == 'Word':
        return 'Int16'
    elif data_type == 'Integer' or data_type == 'Int4' or data_type == 'BCD':
        return 'Int32'
    elif data_type == 'Boolean':
        return 'Bool'
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
        if 'String' not in path_data_type and '' != array_size:
            array_size = f"[{array_size}]"
            data_type = "String"
    return array_size, data_type, offset

def Set_New_Tag_Properties(tags: Union[Dict[str, Any], List[Dict[str, Any]]], new_tag: Dict[str, Any], data_type: str, is_tag_from_csv_flag: bool) -> None:
    # Initialize new_tag with properties if present in tags
    if isinstance(tags, dict):
        new_tag['tagGroup'] = tags.get('tagGroup', '')
        new_tag['dataType'] = tags.get('dataType', data_type)
        new_tag['tagType'] = tags.get('tagType', '')
        new_tag['historyProvider'] = tags.get('historyProvider', '')
        new_tag['historicalDeadband'] = tags.get('historicalDeadband', '')
        new_tag['historicalDeadbandStyle'] = tags.get('historicalDeadbandStyle', '')

    # If tags is a list, we need to search through it for the properties
    for dummy_tags in tags if isinstance(tags, list) else []:
        if 'tagGroup' not in new_tag and 'tagGroup' in dummy_tags:
            new_tag['tagGroup'] = dummy_tags['tagGroup']
        if 'dataType' not in new_tag and 'dataType' in dummy_tags:
            new_tag['dataType'] = dummy_tags['dataType']
        if 'tagType' not in new_tag and 'tagType' in dummy_tags:
            new_tag['tagType'] = dummy_tags['tagType']
        if 'historyProvider' not in new_tag and 'historyProvider' in dummy_tags:
            new_tag['historyProvider'] = dummy_tags['historyProvider']
        if 'historicalDeadband' not in new_tag and 'historicalDeadband' in dummy_tags:
            new_tag['historicalDeadband'] = dummy_tags['historicalDeadband']
        if 'historicalDeadbandStyle' not in new_tag and 'historicalDeadbandStyle' in dummy_tags:
            new_tag['historicalDeadbandStyle'] = dummy_tags['historicalDeadbandStyle']

        # Break the loop if all properties are found
        try:
            if (new_tag['tagGroup'] and new_tag['dataType'] and new_tag['tagType'] and 
                new_tag['historyProvider'] and new_tag['historicalDeadband'] and new_tag['historicalDeadbandStyle']):
                break
        except KeyError:
            pass

    if 'HistoricalDeadband' not in new_tag:
        new_tag.pop('historicalDeadband', None)
    if 'HistoricalDeadbandStyle' not in new_tag:
        new_tag.pop('historicalDeadbandStyle', None)
    if 'HistoryProvider' not in new_tag:
        new_tag.pop('historyProvider', None)

    if is_tag_from_csv_flag:
        new_tag['enabled'] = False
    else:
        new_tag['enabled'] = True
    
    new_tag['valueSource'] = 'opc'
    new_tag['tagGroup']= 'default' # Remove once this in production


def Create_New_Tag(name_parts: List[str], device_name:str, orignal_tag_name:str, area: str, path_data_type: str, array_size: str, offset: str, data_type: str, tags: Dict[str, Any], is_tag_from_csv_flag: bool) -> Dict[str, Any]:
    full_path = ''
    for part in name_parts:
        part = Remove_Non_Alphanumeric_Characters(part)
        full_path += f"{part}/"
    full_path = full_path[:-1]
    full_path = full_path[:full_path.rfind('/')]
    new_tag = {
        "name": orignal_tag_name,
        "opcItemPath": f"ns=1;s=[{device_name}/{full_path}]{area}<{path_data_type}{array_size}>{offset}",
        "opcServer": 'Ignition OPC UA Server',
    }

    Set_New_Tag_Properties(tags, new_tag, data_type, is_tag_from_csv_flag)
    return new_tag

def Process_Tag_Name(ignition_json: Dict[str, Any], key: str, tag_name: str, area: str, path_data_type: str, data_type: str, tags: Dict[str, Any], array_size: str, offset: str, is_tag_from_csv_flag=False) -> None:
    orignal_tag_name = tag_name.split('.')[-1]
    name_parts = [tag_name.split('.')[0]]
    for part in tag_name.split('.')[1:]:
        # max_len = max(len(part) - 3, 4)
        # pattern = re.compile(rf"^(?P<part1>(?=.*[0-9])(?=.*[A-Z])[A-Z0-9]{{2,{max_len}}})_(?P<part2>.*)$")
        # match = pattern.match(part)
        # if match:
        #     part = match.group('part1') + '-' + match.group('part2')
        # #if a lowercase letter is followed by an uppercase letter, add '-' between them
        # elif 'Convayor' in part:
        #     part = re.sub(r'([a-z])([A-C][A-Z])', r'\1\2-', part, count=1)
        # elif re.search(r'[a-z][A-Z]', part):
        #     part = re.sub(r'([a-z])([A-Z])', r'\1-\2', part, count=1)

        # part = part.replace('-', '')
        # part = part.replace('_', '')
        part = re.sub(r'([a-z])([A-Z])', r'\1_\2', part)
        # part = re.sub(r'([a-z])([0-9]+)', r'\1\2_', part)
        part = re.sub(r'([A-Za-z0-9]+)(To)', r'\1_\2_', part)
        part = re.sub(r'(_)([a-z])([A-Za-z]+)', (r'\1\2').upper() + (r'\3').lower(), part)
        part = re.sub(r'([0-9]+)(_)(st)', r'\1\3', part)
        part = re.sub(r'(6)(_)(PM)(_)', r'\1\3.', part)
        part = re.sub(r'(Conveyor)(_)([A-Z])', r'\1\3.', part)
        part = re.sub(r'(__)', r'_', part)
        # part = re.sub(r'([A-Z])([A-Z])', r'\1_\2', part)
        # part = re.sub(r'(_)([A-Z]|[0-9]+)([A-Z])', r'\2-\3', part)
        # part = re.sub(r'(_)([A-Z]|[0-9]+)([_])', r'\2-', part)
        # part = re.sub(r'(-)([0-9]+)([A-Z])', r'-\2_\3', part)
        orignal_tag_name = part

            
        if '.' in part:
            name_parts.extend(part.split('.'))
        else:
            name_parts.append(part)
        
    current_tags = ignition_json[key]['tags']


    for i in range(len(name_parts) - 1):
        part = name_parts[i]
        part = Remove_Non_Alphanumeric_Characters(part)
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
                "tagType": "Folder",
                "tags": []
            }
            current_tags.append(new_folder_tag)
            current_tags = new_folder_tag['tags']
    
    
    new_tag = Create_New_Tag(name_parts, ignition_json[key]['name'], orignal_tag_name, area, path_data_type, array_size, offset, data_type, tags, is_tag_from_csv_flag)
    current_tags.append(new_tag)



def Get_Tag_Name_Address(tags_list: List[Dict[str, Any]], collected_tags: List[Dict[str, str]], parent_tag='') -> None:
    for tag in tags_list:
        if 'dataType' in tag and 'opcItemPath' in tag and 'Kepware' not in tag['opcItemPath']:
            tag_name = tag['name']
            if parent_tag:
                tag_name = f"{parent_tag}/{tag_name}"
            address = tag['opcItemPath'][tag['opcItemPath'].find(']')+1:]
            collected_tags.append({'tag_name': tag_name, 'address': address})
        if 'tags' in tag:
            Get_Tag_Name_Address(tag['tags'], collected_tags, parent_tag=tag['name'])


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
                                if 'enabled' not in tags:
                                    tags['enabled'] = True
                        else: 
                            print(f"Could not find tag {tag_name} in CSV file {key}.csv")
            for tag_to_remove in tags_to_remove:
                ignition_json[key]['tags'].remove(tag_to_remove)
            # Process new tags from CSV
            for index, row in df.iterrows():
                tag_name = row['Tag Name']
                if tag_name not in existing_tag_names:
                    existing_tag_names.add(tag_name)
                    path_data_type = Convert_To_Path_Data_Type(row['Data Type'])
                    address = row['Address']
                    area, offset = Extract_Area_Offset(address)
                    area, path_data_type = Convert_Area_To_Mitsubishi_Format(area, path_data_type)
                    array_size, row['Data Type'], offset = Convert_Array_Size_To_Mitsubishi_Format(offset, path_data_type)
                    if '.' in tag_name:
                        Process_Tag_Name(ignition_json, key, tag_name, area, path_data_type, row['Data Type'], ignition_json[key]["tags"], array_size, offset, is_tag_from_csv_flag=True)
    
    return ignition_json
            



def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:

    # address_csv: Dict[str, pd.DataFrame] = {}
    # for key in ignition_json:
    #     dfs = []
    #     for tags in ignition_json[key]['tags']:
    #         if 'dataType' in tags:
    #             tag_name = tags['name']
    #             row = Find_Row_By_Tag_Name(csv_df[key], tag_name)
    #             if not row.empty:
    #                 address = row.iloc[0, 1]
    #                 area = address[:address.find('0')]
    #                 offset = address[address.find('0'):].lstrip('0') or '0'


    #                 array_size = ''
    #                 if 'SH' in area:
    #                     area = area.replace('SH', '')
    #                     path_data_type = 'String'
    #                 if "." in offset:
    #                     array_size = offset.split('.')[1]
    #                     array_size = array_size.lstrip('0')
    #                     offset = offset.split('.')[0]
    #                     if 'String'not in path_data_type:
    #                         array_size = f"[{array_size}]"

    #                 address = f"{area}<{path_data_type}{array_size}>{offset}"
                    

    #                 df = pd.DataFrame({'tag_name': [tag_name], 'address': [address]})
    #                 dfs.append(df)
    #     if dfs:
    #         address_csv[key] = pd.concat(dfs, ignore_index=True)

    # # sort the rows by tag_name
    # for key in address_csv:
    #     address_csv[key] = address_csv[key].sort_values(by='tag_name', ignore_index=True)

    # return address_csv
    for key in ignition_json:
        #clear csv_df
        csv_df[key] = pd.DataFrame()
        collected_tags = []
        Get_Tag_Name_Address(ignition_json[key]['tags'], collected_tags)
        df = pd.DataFrame(collected_tags)
        
        if key in csv_df:
            csv_df[key] = pd.concat([csv_df[key], df], ignore_index=True)
        else:
            csv_df[key] = df
    return csv_df

