#!/usr/bin/env python

from pandas import DataFrame as pd_DataFrame
from pandas import concat as pd_concat
from typing import Dict, Any, List, Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy as copy_deepcopy
from functools import lru_cache

from base.base_functions import log_message, Find_Row_By_Tag_Name, Extract_Tag_Name, Reset_Tag_Builder_Properties, Extract_Area_And_Offset, Extract_Offset_And_Array_Size, Remove_Invalid_Tag_Name_Characters


DATA_TYPE_MAPPINGS = {
    'Short': ('Int2', 'Int16'),
    'Int2': ('Int2', 'Int16'),
    'Word': ('Int2', 'Int16'),
    'Integer': ('Int4', 'Int32'),
    'Int4': ('Int4', 'Int32'),
    'BCD': ('Int4', 'Int32'),
    'Boolean': ('Boolean', 'Bool')
}

REQUIRED_KEYS = ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']

# Caching frequently called functions
@lru_cache(maxsize=None)
def Convert_Data_Type(data_type: str) -> Tuple[str, str]:
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))

def Update_Area_And_Path_Data_Type(area: str, path_data_type: str='') -> Tuple[str, str]:
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    return area, path_data_type

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
        required_keys = ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']
        for dummy_tag in tags:
            for key in required_keys:
                if key not in new_tag and key in dummy_tag:
                    new_tag[key] = dummy_tag[key]
            if all(key in new_tag for key in required_keys):
                break

def Generate_Full_Path_From_Name_Parts(name_parts):
    return ('/'.join(name_parts[:-1])).rstrip('/')

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

def Create_New_Tag(name_parts: List[str], tags: Dict[str, Any], current_tag, tag_builder_properties) -> Dict[str, Any]:
    if tag_builder_properties['array_size'] != '':
        tag_builder_properties['data_type'] = 'String'
    if 'String' not in tag_builder_properties['path_data_type'] and '' != tag_builder_properties['array_size']:
            tag_builder_properties['array_size'] = f"[{tag_builder_properties['array_size']}]"

    tag_builder_properties['tag_name_path'] = Generate_Full_Path_From_Name_Parts(name_parts)
    tag_builder_properties['tag_name'] = name_parts[-1]

    new_tag = {
        "name": tag_builder_properties['tag_name'],
        "opcItemPath": f"ns=1;s=[{name_parts[0]}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        "opcServer": 'Ignition OPC UA Server',
        "dataType": tag_builder_properties['data_type'],
        'valueSource': 'opc'
    }

    if tag_builder_properties['is_tag_from_csv_flag']:
        Set_New_Tag_Properties(tags, new_tag)
    else:
        Set_Existing_Tag_Properties(current_tag, new_tag)
    return new_tag

def Set_Unnested_Tag_Properties(tag_builder_properties, tag):
    tag.update({
        'name': tag_builder_properties['tag_name'],
        'opcItemPath': f"ns=1;s=[{tag_builder_properties['device_name']}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        'opcServer': 'Ignition OPC UA Server',
        'dataType': tag_builder_properties['data_type'],
        'tagGroup': 'default',
        'enabled': True,
        'valueSource': 'opc'
    })

def Build_Tag_Hierarchy(tags, name_parts):
    dummy_tags = tags
    for part in name_parts[:-1]:
        found = False
        for tag in dummy_tags:
            if tag['name'] == part:
                dummy_tags = tag['tags']
                found = True
                break
        if not found:
            new_folder_tag = {
                "name": part,
                "tagType": "Folder",
                "tags": []
            }
            dummy_tags.append(new_folder_tag)
            dummy_tags = new_folder_tag['tags']
    return dummy_tags

def Process_Tag_Name(device_name, tags, current_tag, tag_builder_properties) -> None:
    name_parts = [Remove_Invalid_Tag_Name_Characters(part) for part in tag_builder_properties['tag_name'].split('.')]
    dummy_tags = Build_Tag_Hierarchy(tags, name_parts)

    name_parts.insert(0, device_name)
    new_tag = Create_New_Tag(name_parts, tags, current_tag, tag_builder_properties)
    dummy_tags.append(new_tag)


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

def Handle_Duplicate_Tag(key, tag_builder_properties, generated_ingition_json, tag):
    log_message(f"Duplicate tag found in ignition JSON {key}.json", 'warning')
    log_message(f"Duplicate tag name: {tag_builder_properties['tag_name']}", 'warning')
    log_message("So Deleting the duplicate tag", 'warning')
    generated_ingition_json[key]['tags'].remove(tag)

def remove_tag(tags, tag_to_remove):
    for tag in tags:
        if 'opcItemPath' in tag:
            if tag['opcItemPath'] == tag_to_remove['opcItemPath']:
                tags.remove(tag)
                return
            if 'tags' in tag:
                remove_tag(tag['tags'], tag_to_remove)

def Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, existing_tag_names):
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            Process_Tag(generated_ingition_json, tag_builder_properties, key, df, sub_tag, existing_tag_names)
    else:
        if 'opcItemPath' in tag and 'dataType' in tag:
            tag_builder_properties['tag_name'] = Extract_Tag_Name(tag['opcItemPath'])

            if tag_builder_properties['tag_name'] not in existing_tag_names:
                tag_builder_properties['row'] = Find_Row_By_Tag_Name(df, tag_builder_properties['tag_name'])

                if not tag_builder_properties['row'].empty:
                    existing_tag_names.append(tag_builder_properties['tag_name'])
                    df.drop(tag_builder_properties['row'].index, inplace=True)
                    Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], is_tag_from_csv_flag=False, data_type=tag['dataType'])
                    Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)

                    if '.' in tag_builder_properties['tag_name']:
                        Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], tag, tag_builder_properties)
                    else:
                        new_tag = copy_deepcopy(tag)
                        Set_Unnested_Tag_Properties(tag_builder_properties, new_tag)
                        generated_ingition_json[key]['tags'].append(new_tag)
                    
                    remove_tag(generated_ingition_json[key]['tags'], tag)
                    

                else:
                    log_message(f"Could not find tag {tag_builder_properties['tag_name']} in CSV file {key}.csv so just leaving it as is", 'warning')
            else:
                Handle_Duplicate_Tag(key, tag_builder_properties, generated_ingition_json, tag)
        else:
            log_message(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is', 'warning')


def Create_Tag_Builder_Properties():
    return {
        "path_data_type": '',
        "data_type": '',
        "tag_name": '',
        "tag_name_path": '',
        "address": '',
        "area": '',
        "offset": '',
        "array_size": '',
        "row": '',
        "device_name": '',
        "is_tag_from_csv_flag": False
    }


def Update_Device_CSV(tag_builder_properties, collected_data):
    tag_name = ''
    if tag_builder_properties['data_type'] != '':
        if '/' not in tag_builder_properties['tag_name_path']:
            tag_name = tag_builder_properties['tag_name']
        else:
            tag_name = f'{tag_builder_properties["tag_name_path"][tag_builder_properties["tag_name_path"].find("/") + 1:]}/{tag_builder_properties["tag_name"]}'
            
        collected_data.append({
            'tag_name': tag_name,
            'address': f"{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}"
        })

def Finalize_Device_CSV(device_csv, key, collected_data):
    if collected_data:
        device_csv[key] = pd_concat([device_csv[key], pd_DataFrame(collected_data)], ignore_index=True)

def Process_CSV_Row(generated_ingition_json, tag_builder_properties, key, row, collected_data=[]):
    tag_builder_properties['tag_name'] = row['Tag Name']
    Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], row)
    Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)
    Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], {}, tag_builder_properties)
    Update_Device_CSV(tag_builder_properties, collected_data)
    tag_builder_properties = copy_deepcopy(Create_Tag_Builder_Properties())
            
def Generate_Ignition_JSON_And_Address_CSV_Helper(key, df, ignition_json, csv_df):
    tag_builder_properties = Create_Tag_Builder_Properties()
    generated_ingition_json = copy_deepcopy(ignition_json)
    collected_data = []
    existing_tag_names = []

    for tag in ignition_json[key]['tags']:
        Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, existing_tag_names)
        Update_Device_CSV(tag_builder_properties, collected_data)
        Reset_Tag_Builder_Properties(tag_builder_properties)

    for _, row in df.iterrows():
        Process_CSV_Row(generated_ingition_json, tag_builder_properties, key, row, collected_data)

    Finalize_Device_CSV(csv_df, key, collected_data)

    return key, generated_ingition_json[key], csv_df[key]

def Generate_Ignition_JSON_And_Address_CSV(csv_df: Dict[str, pd_DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, Any]:
    generated_ingition_json = copy_deepcopy(ignition_json)
    device_csv = {key: pd_DataFrame() for key in csv_df}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(Generate_Ignition_JSON_And_Address_CSV_Helper, key, df, generated_ingition_json, device_csv): key for key, df in csv_df.items()}

        for future in as_completed(futures):
            key = futures[future]
            try:
                key, updated_json, updated_csv = future.result()
                generated_ingition_json[key] = updated_json
                device_csv[key] = updated_csv
            except Exception as exc:
                log_message(f"Error processing {key}: {exc}", 'error')

    return generated_ingition_json, device_csv