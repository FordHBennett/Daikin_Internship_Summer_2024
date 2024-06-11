#!/usr/bin/env python

from ast import Tuple
import json
import sys
import pandas as pd
from typing import Dict, Any, List, Union, Tuple
import re
import copy
from base.base_functions import Remove_Non_Alphanumeric_Characters, Reset_Tag_Builder_Properties

def Find_Row_By_Tag_Name(df: pd.DataFrame, tag_name: str) -> pd.DataFrame:
    return df[df['Tag Name'] == tag_name]

def Extract_Tag_Name(opc_item_path: str) -> str:
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]


def Convert_Data_Type(data_type: str) -> Tuple[str, str]:
    path_data_type = ''
    if data_type in {'Short', 'Int2', 'Word'}:
        data_type = 'Int2'
        path_data_type = 'Int16'
    elif data_type in {'Integer', 'Int4', 'BCD'}:
        data_type = 'Int4'
        path_data_type = 'Int32'
    elif data_type == 'Boolean':
        data_type = 'Boolean'
        path_data_type = 'Bool'
    return data_type, path_data_type



def Extract_Area_And_Offset(address: str) -> Tuple[str, str]:
    match = re.search(r'\d+', address)
    if match:
        if 'X' in address:
            area, hex_address = address.split('X')[0], address.split('X')[1]
            # Convert hex to decimal
            offset = str(int(hex_address.lstrip('0') or '0', 16))
            return area, offset
        else:
            first_number_index = match.start()
            area = address[:first_number_index]
            offset = address[first_number_index:].lstrip('0') or '0'
            return area, offset
    else:
        exit(f"Invalid address format: {address}")

def Update_Area_And_Path_Data_Type(area: str, path_data_type: str='') -> Tuple[str, str]:
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
        return area, path_data_type
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = 'Bool'
        area = area.replace('M', '')
        return area, path_data_type
    return area, path_data_type

def Extract_Offset_And_Array_Size(offset: str) -> Tuple[str, str]:
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]
        return offset, array_size
    return offset, ''


def Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties: Dict[str, Any]) -> None:

    tag_builder_properties['data_type'], tag_builder_properties['path_data_type'] = Convert_Data_Type(tag_builder_properties['data_type'])
    tag_builder_properties['area'], tag_builder_properties['offset'] = Extract_Area_And_Offset(tag_builder_properties['address'])

    try:
        tag_builder_properties['area'], tag_builder_properties['path_data_type'] = Update_Area_And_Path_Data_Type(tag_builder_properties['area'], tag_builder_properties['path_data_type'])
    except KeyError:
        tag_builder_properties['area'], tag_builder_properties['path_data_type'] = Update_Area_And_Path_Data_Type(tag_builder_properties['area'])

    tag_builder_properties['offset'], tag_builder_properties['array_size'] = Extract_Offset_And_Array_Size(tag_builder_properties['offset'])



def Find_Missing_Tag_Properties(tags, new_tag) -> None:
    if isinstance(tags, list):
        for dummy_tag in tags:
            for key in ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']:
                if key not in new_tag and key in dummy_tag:
                    new_tag[key] = dummy_tag[key]
            if all(key in new_tag for key in ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']):
                break

def Set_New_Tag_Properties(tags: Union[Dict[str, Any], List[Dict[str, Any]]], new_tag: Dict[str, Any]) -> None:

    Find_Missing_Tag_Properties(tags, new_tag)
    new_tag.update({
        'enabled': False,
        'valueSource': 'opc',
        'tagGroup': 'default'
    })

def Set_Existing_Tag_Properties(current_tag, new_tag):
    new_tag['tagGroup'] = 'default' # Remove once this in production
    new_tag['tagType'] = current_tag['tagType']
    for key in ['historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']:
        if key in current_tag:
            new_tag[key] = current_tag[key]
    new_tag['enabled'] = True


def Generate_Full_Path_From_Name_Parts(name_parts):
    full_path = ''
    for i in range(len(name_parts) - 1):
        part = name_parts[i]
        part = Remove_Non_Alphanumeric_Characters(part)
        full_path += f"{part}/" 
    
    return full_path.rstrip('/')
    
    


def Create_New_Tag(name_parts: List[str], tags: Dict[str, Any], current_tag, tag_builder_properties) -> Dict[str, Any]:
    if tag_builder_properties['array_size'] != '':
        tag_builder_properties['data_type'] = 'String'
    if 'String' not in tag_builder_properties['path_data_type'] and '' != tag_builder_properties['array_size']:
            tag_builder_properties['array_size'] = f"[{tag_builder_properties['array_size']}]"

    new_tag = {
        "name": name_parts[-1],
        "opcItemPath": f"ns=1;s=[{Generate_Full_Path_From_Name_Parts(name_parts)}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        "opcServer": 'Ignition OPC UA Server',
        "dataType": tag_builder_properties['data_type'],
    }

    if tag_builder_properties['is_tag_from_csv_flag']:
        Set_New_Tag_Properties(tags, new_tag)
    else:
        Set_Existing_Tag_Properties(current_tag, new_tag)
    return new_tag

# this shit is broken 
def Process_Tag_Name(device_name, tags, current_tag, tag_builder_properties) -> None:
    if '.' in tag_builder_properties['tag_name']:
        name_parts = [tag_builder_properties['tag_name'].split('.')[0]]
        for part in tag_builder_properties['tag_name'].split('.')[1:]:
            if '.' in part:
                name_parts.extend(part.split('.'))
            else:
                name_parts.append(part)
        
        dummy_tags = copy.deepcopy(tags)

        for part in name_parts[:-1]:
            found = False
            for tag in dummy_tags:
                if tag['name'] == part:
                    if 'tags' not in tag:
                        tag['tags'] = []
                    dummy_tags = tag['tags']
                    found = True
                    break
            if not found:
                new_folder_tag = {
                    "name": Remove_Non_Alphanumeric_Characters(part),
                    "tagType": "Folder",
                    "tags": []
                }
                tags.append(new_folder_tag)
    else:
        name_parts = [tag_builder_properties['tag_name']]
        dummy_tags = tags

    name_parts.insert(0, device_name)
    new_tag = Create_New_Tag(name_parts, tags, current_tag, tag_builder_properties)
    dummy_tags.append(new_tag)


def Get_Tag_Name_And_Address(tags_list: List[Dict[str, Any]], collected_tags: List[Dict[str, str]]) -> List[Dict[str, str]]:
    for tag in tags_list:
        if 'opcItemPath' in tag and 'Kepware' not in tag['opcItemPath']:
            if '/' not in tag['opcItemPath']:
                tag_name = tag['name']
            else:
                tag_name = f"{tag['opcItemPath'][tag['opcItemPath'].find('/')+1:tag['opcItemPath'].find(']')]}/{tag['name']}"

            address = tag['opcItemPath'][tag['opcItemPath'].find(']')+1:]
            collected_tags.append({'tag_name': tag_name, 'address': address})
        if 'tags' in tag:
            Get_Tag_Name_And_Address(tag['tags'], collected_tags)
    return collected_tags


def Set_Unnested_Tag_Properties(tag_builder_properties, tag):

    tag.update({
        'name': tag_builder_properties['tag_name'],
        'opcItemPath': f"ns=1;s=[{tag_builder_properties['device_name']}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        'opcServer': 'Ignition OPC UA Server',
        'dataType': tag_builder_properties['data_type'],
        'tagGroup': 'default',
        'enabled': True
    })

def Populate_Tag_Builder_Properties(tag_builder_properties, device_name, row=None, is_tag_from_csv_flag=True, data_type=None) -> None:
    if is_tag_from_csv_flag:
        tag_builder_properties.update({
            'is_tag_from_csv_flag': True,
            'device_name': device_name,
            'data_type': row['Data Type'],
            'address': row['Address']
        })

    else:
        tag_builder_properties.update({
            'device_name': device_name,
            'data_type': data_type,
            'address': tag_builder_properties['row'].iloc[0, 1]
        })

def Modify_Tags_For_Direct_Driver_Communication(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, Any]:

    tag_builder_properties = {
        "path_data_type": '',
        "data_type": '',
        "tag_name": '',
        "address": '',
        "area": '',
        "offset": '',
        "array_size": '',
        "row": '',
        "device_name": '',
        "is_tag_from_csv_flag": False
    }

    generated_ingition_json = copy.deepcopy(ignition_json)
    for key, df in csv_df.items():
        if key in ignition_json:
            existing_tag_names = set()
            tags_to_remove = []
            for tag in ignition_json[key]['tags']:
                Process_Tag(generated_ingition_json, tag_builder_properties, key, df, existing_tag_names, tags_to_remove, tag)
                Reset_Tag_Builder_Properties(tag_builder_properties)       

            for tag_to_remove in tags_to_remove:
                generated_ingition_json[key]['tags'].remove(tag_to_remove)

            for _, row in df.iterrows():
                tag_builder_properties['tag_name'] = row['Tag Name']

                if tag_builder_properties['tag_name'] not in existing_tag_names:
                    Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], row)
                    existing_tag_names.add(tag_builder_properties['tag_name'])
                    Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)
                    Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], {}, tag_builder_properties)
                
                Reset_Tag_Builder_Properties(tag_builder_properties)
        else:
            print(f"Could not find CSV file {key}.csv in ignition JSON")
    
    return generated_ingition_json

# Add way so that if there are folder tags it'll work
def Process_Tag(generated_ingition_json, tag_builder_properties, key, df, existing_tag_names, tags_to_remove, tag):
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            Process_Tag(generated_ingition_json, tag_builder_properties, key, df, existing_tag_names, tags_to_remove, sub_tag)
    else:
        if 'opcItemPath' in tag and 'dataType' in tag:
            tag_builder_properties['tag_name'] = Extract_Tag_Name(tag['opcItemPath'])
            existing_tag_names.add(tag_builder_properties['tag_name'])
            tag_builder_properties['row'] = Find_Row_By_Tag_Name(df, tag_builder_properties['tag_name'])

            if not tag_builder_properties['row'].empty:
                Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], is_tag_from_csv_flag=False, data_type=tag['dataType'])
                Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)

                if '.' in tag_builder_properties['tag_name']:
                    Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], tag, tag_builder_properties)
                    tags_to_remove.append(tag)
                else:
                    Set_Unnested_Tag_Properties(tag_builder_properties, tag)
            else: 
                print(f"Could not find tag {tag_builder_properties['tag_name']} in CSV file {key}.csv")
        else:
            print(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is')
            


def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    for key in ignition_json:
        #clear csv_df
        csv_df[key] = pd.DataFrame()
        collected_tags = []
        collected_tags = Get_Tag_Name_And_Address(ignition_json[key]['tags'],collected_tags)
        df = pd.DataFrame(collected_tags)
        
        if key in csv_df:
            csv_df[key] = pd.concat([csv_df[key], df], ignore_index=True)
        else:
            csv_df[key] = df

    return csv_df

