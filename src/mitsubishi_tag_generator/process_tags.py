#!/usr/bin/env python

import pandas as pd
from typing import Dict, Any, List, Union, Tuple, Final
import copy
from base.base_functions import *

def Convert_Data_Type(data_type: str) -> Tuple[str, str]:
    data_type_mappings = {
        'Short': ('Int2', 'Int16'),
        'Int2': ('Int2', 'Int16'),
        'Word': ('Int2', 'Int16'),
        'Integer': ('Int4', 'Int32'),
        'Int4': ('Int4', 'Int32'),
        'BCD': ('Int4', 'Int32'),
        'Boolean': ('Boolean', 'Bool')
    }
    return data_type_mappings.get(data_type, (data_type, ''))

def Update_Area_And_Path_Data_Type(area: str, path_data_type: str='') -> Tuple[str, str]:
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = 'Bool'
        area = area.replace('M', '')
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

def Set_Unnested_Tag_Properties(tag_builder_properties, tag):
    tag.update({
        'name': tag_builder_properties['tag_name'],
        'opcItemPath': f"ns=1;s=[{tag_builder_properties['device_name']}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        'opcServer': 'Ignition OPC UA Server',
        'dataType': tag_builder_properties['data_type'],
        'tagGroup': 'default',
        'enabled': True
    })

def Process_Tag_Name(device_name, tags, current_tag, tag_builder_properties) -> None:
    name_parts = [Remove_Non_Alphanumeric_Characters(part) for part in tag_builder_properties['tag_name'].split('.')]
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

def Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, existing_tag_names):
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            Process_Tag(generated_ingition_json, tag_builder_properties, key, df, sub_tag, existing_tag_names)
    else:
        if 'opcItemPath' in tag and 'dataType' in tag:
            tag_builder_properties['tag_name'] = Extract_Tag_Name(tag['opcItemPath'])
            if tag_builder_properties['tag_name'] not in existing_tag_names:
                existing_tag_names.append(tag_builder_properties['tag_name'])
                tag_builder_properties['row'] = Find_Row_By_Tag_Name(df, tag_builder_properties['tag_name'])

                if not tag_builder_properties['row'].empty:
                    Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], is_tag_from_csv_flag=False, data_type=tag['dataType'])
                    Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)

                    if '.' in tag_builder_properties['tag_name']:
                        tag_to_remove = tag
                        Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], tag, tag_builder_properties)

                    else:
                        tag_to_remove = copy.deepcopy(tag)
                        Set_Unnested_Tag_Properties(tag_builder_properties, tag)
                        generated_ingition_json[key]['tags'].append(tag)

                    generated_ingition_json[key]['tags'].remove(tag_to_remove)
            else:
                    print(f"Duplicate tag found in ignition JSON {key}.json")
                    print(f"Duplicate tag name: {tag_builder_properties['tag_name']}")
                    print("So Deleting the duplicate tag")
                    generated_ingition_json[key]['tags'].remove(tag)
        else:
            print(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is')
            
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
    device_csv = copy.deepcopy(csv_df)
    for key, df in csv_df.items():
        if key in ignition_json:
            existing_tag_names = []
            for tag in ignition_json[key]['tags']:
                Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, existing_tag_names)
                Reset_Tag_Builder_Properties(tag_builder_properties) 

            for _, row in df.iterrows():
                tag_builder_properties['tag_name'] = row['Tag Name']

                if tag_builder_properties['tag_name'] not in existing_tag_names:
                    Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], row)
                    existing_tag_names.append(tag_builder_properties['tag_name'])
                    Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)
                    Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], {}, tag_builder_properties)
    
                    Reset_Tag_Builder_Properties(tag_builder_properties)
        else:
            print(f"Could not find CSV file {key}.csv in ignition JSON")

        del ignition_json[key]
        del df
            
    return generated_ingition_json

def Get_Tag_Name_And_Address(tags_list: List[Dict[str, Any]], collected_tags: List[Dict[str, str]]) -> List[Dict[str, str]]:
    for tag in tags_list:
        if 'opcItemPath' in tag and 'Kepware' not in tag['opcItemPath']:
            tag_name = tag['name'] if '/' not in tag['opcItemPath'] else f"{tag['opcItemPath'].split('/')[1].split(']')[0]}/{tag['name']}"
            address = tag['opcItemPath'].split(']')[1]
            collected_tags.append({'tag_name': tag_name, 'address': address})
        if 'tags' in tag:
            Get_Tag_Name_And_Address(tag['tags'], collected_tags)
    return collected_tags

def Generate_Address_CSV(csv_df: Dict[str, pd.DataFrame], ignition_json: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    for key in ignition_json:
        #clear csv_df
        csv_df[key] = pd.DataFrame()
        collected_tags = []
        collected_tags = Get_Tag_Name_And_Address(ignition_json[key]['tags'], collected_tags)
        df = pd.DataFrame(collected_tags)
        
        if key in csv_df:
            csv_df[key] = pd.concat([csv_df[key], df], ignore_index=True)
        else:
            csv_df[key] = df

    return csv_df

