#!/usr/bin/env python

from ast import Tuple
from calendar import c
from curses.ascii import isalpha
from numpy import add
import pandas as pd
from typing import Dict, Any, List, Union, Tuple
import re
from base.base_functions import Remove_Non_Alphanumeric_Characters

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    return df[df['Tag Name'] == tag_name]

def Convert_Data_Type(data_type: str) -> tuple[str, str]:
    """
    Converts the given data type to the corresponding data type used in the system.

    Args:
        data_type (str): The data type to be converted.

    Returns:
        tuple[str, str]: data_type, path_data_type
    """
    if data_type == 'Short' or data_type == 'Int2' or data_type == 'Word':
        return 'Int16', 'Int2'
    elif data_type == 'Integer' or data_type == 'Int4' or data_type == 'BCD':
        return 'Int32', 'Int4'
    elif data_type == 'Boolean':
        return 'Bool', 'Boolean'

    return data_type, data_type


def Extract_Area_Offset(address: str) -> tuple[str, str]:
    """
    Extracts the area and offset from the given address.

    Args:
        address (str): The address to extract the area and offset from.

    Returns:
        tuple[str, str]: area, offset

    Raises:
        SystemExit: If the address contains no numbers or letters.
    """
    match = re.search(r'\d+', address)
    if match:
        first_number_index = match.start()
        area = address[:first_number_index]
        offset = address[first_number_index:].lstrip('0') or '0'
    else:
        exit(f"Invalid address format: {address}")

    return area, offset

def Convert_Area_To_Mitsubishi_Format(area: str, path_data_type: str) -> Tuple[str, str]:
    """
    Converts the given area to Mitsubishi format by removing 'SH' and updating the path data type if necessary.

    Args:
        area (str): The area to be converted.
        path_data_type (str): The path data type.

    Returns:
        tuple: area, path_data_type
    """
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    return area, path_data_type

def Convert_Array_Size_To_Mitsubishi_Format(offset: str):
    """
    Converts the array size to the Mitsubishi format.

    Args:
        offset (str): The offset value.

    Returns:
        tuple: array_size, offset
    """
    array_size = ''
    if "." in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]
    return array_size, offset

def Set_New_Tag_Properties(tags: Union[Dict[str, Any], List[Dict[str, Any]]], new_tag: Dict[str, Any], is_tag_from_csv_flag: bool) -> None:
    # Initialize new_tag with properties if present in tags
    if isinstance(tags, dict):
        new_tag['tagGroup'] = tags.get('tagGroup', '')
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

    if is_tag_from_csv_flag:
        new_tag['enabled'] = False
    else:
        new_tag['enabled'] = True
    
    new_tag['valueSource'] = 'opc'
    new_tag['tagGroup']= 'default' # Remove once this in production


def Create_New_Tag(name_parts: List[str], orignal_tag_name:str,device_name:str, tags: Dict[str, Any], current_tag, tag_builder_properties) -> Dict[str, Any]:
    if tag_builder_properties['array_size'] != '':
        data_type = 'String'
    if 'String' not in tag_builder_properties['path_data_type'] and '' != tag_builder_properties['array_size']:
            tag_builder_properties['array_size'] = f"[{tag_builder_properties['array_size']}]"
    full_path = ''
    for part in name_parts:
        part = Remove_Non_Alphanumeric_Characters(part)
        full_path += f"{part}/"
    full_path = full_path[:full_path.rfind('/')]
    new_tag = {
        "name": orignal_tag_name,
        "opcItemPath": f"ns=1;s=[{device_name}/{full_path}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        "opcServer": 'Ignition OPC UA Server',
        "dataType": tag_builder_properties['data_type'],
    }

    if tag_builder_properties['is_tag_from_csv_flag']:
        Set_New_Tag_Properties(tags, new_tag, tag_builder_properties['is_tag_from_csv_flag'])
    else:
        new_tag['tagGroup'] = 'default' # Remove once this in production
        new_tag['tagType'] = current_tag['tagType']
        if 'historyProvider' in current_tag:
            new_tag['historyProvider'] = current_tag['historyProvider']
        if 'historicalDeadband' in current_tag:
            new_tag['historicalDeadband'] = current_tag['historicalDeadband']
        if 'historicalDeadbandStyle' in current_tag:
            new_tag['historicalDeadbandStyle'] = current_tag['historicalDeadbandStyle']
        new_tag['enabled'] = True
    return new_tag

def Process_Tag_Name(device_name, tags, current_tag, tag_builder_properties) -> None:
    if '.' in tag_builder_properties['tag_name']:
        orignal_tag_name = tag_builder_properties['tag_name'].split('.')[-1]
        name_parts = [tag_builder_properties['tag_name'].split('.')[0]]
        for part in tag_builder_properties['tag_name'].split('.')[1:]:
            orignal_tag_name = part
            if '.' in part:
                name_parts.extend(part.split('.'))
            else:
                name_parts.append(part)
        
        current_tags = tags

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
    else:
        orignal_tag_name = tag_builder_properties['tag_name']
        name_parts = [tag_builder_properties['tag_name']]
        current_tags = tags
    
    
    # new_tag = Create_New_Tag(name_parts, orignal_tag_name, ignition_json[key]['name'],ignition_json[key]['tags'], tags, tag_builder_properties)
    new_tag = Create_New_Tag(name_parts, orignal_tag_name, device_name, tags, current_tag, tag_builder_properties)
    current_tags.append(new_tag)



def Get_Tag_Name_Address(tags_list: List[Dict[str, Any]], collected_tags: List[Dict[str, str]]) -> List[Dict[str, str]]:
    for tag in tags_list:
        if 'opcItemPath' in tag and 'Kepware' not in tag['opcItemPath']:
            if '/' not in tag['opcItemPath']:
                tag_name = tag['name']
            else:
                tag_name = f"{tag['opcItemPath'][tag['opcItemPath'].find('/')+1:tag['opcItemPath'].find(']')]}/{tag['name']}"

            address = tag['opcItemPath'][tag['opcItemPath'].find(']')+1:]
            collected_tags.append({'tag_name': tag_name, 'address': address})
        if 'tags' in tag:
            Get_Tag_Name_Address(tag['tags'], collected_tags)
    return collected_tags


def Modify_Tags_For_Direct_Driver_Communication(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifies tags for direct driver communication based on the provided CSV data and Ignition JSON.

    Args:
        csv_df (Dict[str, pd.DataFrame]): A dictionary containing CSV data as pandas DataFrames.
        ignition_json (Dict[str, Any]): A dictionary containing Ignition JSON data.

    Returns:
        None
    """
    tag_builder_properties = {
        "path_data_type": '',
        "data_type": '',
        "tag_name": '',
        "address": '',
        "area": '',
        "offset": '',
        "array_size": '',
        "row": '',
        "is_tag_from_csv_flag": False
    }

    for key, df in csv_df.items():
        if key in ignition_json:
            existing_tag_names = set()
            tags_to_remove = []
            for tag in ignition_json[key]['tags']:
                if 'opcItemPath' in tag:
                    # path_data_type = ''
                    if 'dataType' in tag:
                        # data_type = tag['dataType']
                        tag_builder_properties['data_type'] = tag['dataType']
                        # path_data_type, data_type = Convert_Data_Type(data_type)
                        tag_builder_properties['path_data_type'], tag_builder_properties['data_type'] = Convert_Data_Type(tag_builder_properties['data_type'])
                        dummy_name = tag['opcItemPath'][tag['opcItemPath'].find('.')+1:]
                        # tag_name = dummy_name[dummy_name.find('.')+1:]
                        tag_builder_properties['tag_name'] = dummy_name[dummy_name.find('.')+1:]
                        existing_tag_names.add(tag_builder_properties['tag_name'])

                        # row = Find_Row_By_Tag_Name(df, tag_name)
                        tag_builder_properties['row'] = Find_Row_By_Tag_Name(df, tag_builder_properties['tag_name'])
                        # if not row.empty:
                        if not tag_builder_properties['row'].empty:
                            # address = row.iloc[0, 1]
                            tag_builder_properties['address'] = tag_builder_properties['row'].iloc[0, 1]
                            # area, offset = Extract_Area_Offset(address)
                            tag_builder_properties['area'], tag_builder_properties['offset'] = Extract_Area_Offset(tag_builder_properties['address'])
                            # area, path_data_type = Convert_Area_To_Mitsubishi_Format(area, path_data_type)
                            tag_builder_properties['area'], tag_builder_properties['path_data_type'] = Convert_Area_To_Mitsubishi_Format(tag_builder_properties['area'], tag_builder_properties['path_data_type'])
                            # array_size, offset = Convert_Array_Size_To_Mitsubishi_Format(offset)
                            tag_builder_properties['array_size'], tag_builder_properties['offset'] = Convert_Array_Size_To_Mitsubishi_Format(tag_builder_properties['offset'])
                            # if data_type == "":
                            if tag_builder_properties['data_type'] == "":
                                # data_type = tags['dataType']
                                tag_builder_properties['data_type'] = tag['dataType']
                            # if '.' in tag_name:
                            if '.' in tag_builder_properties['tag_name']:
                                Process_Tag_Name(ignition_json[key]['name'], ignition_json[key]['tags'], tag, tag_builder_properties)
                                tags_to_remove.append(tag)
                            else:
                                # tags["name"] = tag_name
                                tag['name'] = tag_builder_properties['tag_name']
                                # tags['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{area}<{path_data_type}{array_size}>{offset}"
                                tag['opcItemPath'] = f"ns=1;s=[{ignition_json[key]['name']}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}"
                                tag['opcServer'] = 'Ignition OPC UA Server'
                                # tags['dataType'] = data_type
                                tag['dataType'] = tag_builder_properties['data_type']
                                tag['tagGroup'] = 'default' # Remove once this in production
                                if 'enabled' not in tag:
                                    tag['enabled'] = True
                        else: 
                            # print(f"Could not find tag {tag_name} in CSV file {key}.csv")
                            print(f"Could not find tag {tag_builder_properties['tag_name']} in CSV file {key}.csv")
                
                # reset tag_builder_properties
                for property in tag_builder_properties:
                    tag_builder_properties[property] = ''
                        
                        
            for tag_to_remove in tags_to_remove:
                ignition_json[key]['tags'].remove(tag_to_remove)
            # Process new tags from CSV
            for index, row in df.iterrows():
                tag_builder_properties['is_tag_from_csv_flag'] = True
                # tag_name = row['Tag Name']
                tag_builder_properties['tag_name'] = row['Tag Name']
                # data_type = row['Data Type']
                tag_builder_properties['data_type'] = row['Data Type']
                # if tag_name not in existing_tag_names:
                if tag_builder_properties['tag_name'] not in existing_tag_names:
                    # existing_tag_names.add(tag_name)
                    existing_tag_names.add(tag_builder_properties['tag_name'])
                    # path_data_type, data_type = Convert_Data_Type(data_type)
                    tag_builder_properties['path_data_type'], tag_builder_properties['data_type'] = Convert_Data_Type(tag_builder_properties['data_type'])
                    # address = row['Address']
                    tag_builder_properties['address'] = row['Address']
                    # area, offset = Extract_Area_Offset(address)
                    tag_builder_properties['area'], tag_builder_properties['offset'] = Extract_Area_Offset(tag_builder_properties['address'])
                    # area, path_data_type = Convert_Area_To_Mitsubishi_Format(area, path_data_type)
                    tag_builder_properties['area'], tag_builder_properties['path_data_type'] = Convert_Area_To_Mitsubishi_Format(tag_builder_properties['area'], tag_builder_properties['path_data_type'])
                    # array_size, offset = Convert_Array_Size_To_Mitsubishi_Format(offset)
                    tag_builder_properties['array_size'], tag_builder_properties['offset'] = Convert_Array_Size_To_Mitsubishi_Format(tag_builder_properties['offset'])
                    # Process_Tag_Name(ignition_json, key, tag_name, area, path_data_type, data_type, ignition_json[key]["tags"], array_size, offset, is_tag_from_csv_flag=True)
                    # Process_Tag_Name(ignition_json, key, row, tag_builder_properties)
                    Process_Tag_Name(ignition_json[key]['name'], ignition_json[key]['tags'], {}, tag_builder_properties)
                
                # reset tag_builder_properties
                for property in tag_builder_properties:
                    tag_builder_properties[property] = ''
    
    return ignition_json
            



def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    for key in ignition_json:
        #clear csv_df
        csv_df[key] = pd.DataFrame()
        collected_tags = []
        collected_tags = Get_Tag_Name_Address(ignition_json[key]['tags'],collected_tags)
        df = pd.DataFrame(collected_tags)
        
        if key in csv_df:
            csv_df[key] = pd.concat([csv_df[key], df], ignore_index=True)
        else:
            csv_df[key] = df
    return csv_df

