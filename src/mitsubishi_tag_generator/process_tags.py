#!/usr/bin/env python

# from os import path
# import re
from re import S
# from pandas import DataFrame as pd_DataFrame
# from pandas import concat as pd_concat
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
# from copy import deepcopy as copy_deepcopy


from base.base_functions import log_message, Find_Row_By_Tag_Name, Extract_Tag_Name, Reset_Tag_Builder_Properties, Extract_Area_And_Offset, Extract_Offset_And_Array_Size, Remove_Invalid_Tag_Name_Characters, Set_Tag_Properties, Generate_Full_Path_From_Name_Parts, Convert_Data_Type, Build_Tag_Hierarchy, Create_Tag_Builder_Properties

def Update_Area_And_Path_Data_Type(area: str, path_data_type: str='') -> Tuple[str, str]:
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = 'Bool'
    return area, path_data_type

def Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties: Dict[str, Any]) -> None:
    data_type, path_data_type = Convert_Data_Type(tag_builder_properties['data_type'])
    area, offset = Extract_Area_And_Offset(tag_builder_properties['address'])
    area, path_data_type = Update_Area_And_Path_Data_Type(area, path_data_type)
    offset, array_size = Extract_Offset_And_Array_Size(offset)


    tag_builder_properties.update({
        'data_type': data_type,
        'path_data_type': path_data_type,
        'area': area,
        'offset': offset,
        'array_size': array_size
    })




def Create_New_Tag(name_parts: List[str], tags: Dict[str, Any], current_tag, tag_builder_properties) -> None:
    if tag_builder_properties['array_size'] != '':
        tag_builder_properties['data_type'] = 'String'
    if 'String' not in tag_builder_properties['path_data_type'] and '' != tag_builder_properties['array_size']:
        tag_builder_properties['array_size'] = f"[{tag_builder_properties['array_size']}]"

    tag_builder_properties['tag_name'] = name_parts[-1]
    tag_builder_properties['device_name'] = name_parts[0]

    new_tag = {
        "name": tag_builder_properties['tag_name'],
        "opcItemPath": f"ns=1;s=[{tag_builder_properties['device_name']}]{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}",
        "opcServer": 'Ignition OPC UA Server',
        "dataType": tag_builder_properties['data_type'],
        'valueSource': 'opc'
    }

    if tag_builder_properties['is_tag_from_csv_flag']:
        Set_Tag_Properties(tags=tags, new_tag=new_tag)
        current_tag.update(new_tag)
        tag_builder_properties['tag_name_path'] = Generate_Full_Path_From_Name_Parts(name_parts)
    else:
        Set_Tag_Properties(new_tag=new_tag, current_tag=current_tag)
        current_tag.update(new_tag)
        if tag_builder_properties['tag_name_path'] != '':
            tag_builder_properties['tag_name_path'] = f'{name_parts[0]}/{tag_builder_properties["tag_name_path"]}'
        else:
            tag_builder_properties['tag_name_path'] = name_parts[0]




def Process_Tag_Name(device_name, tags, current_tag, tag_builder_properties) -> None:
    if tag_builder_properties['is_tag_from_csv_flag']:
        name_parts = [Remove_Invalid_Tag_Name_Characters(part) for part in tag_builder_properties['tag_name'].split('.')]
        name_parts.insert(0, 'kepware')
        dummy_tags = Build_Tag_Hierarchy(tags, name_parts)
        name_parts.insert(0, device_name)
        Create_New_Tag(name_parts, tags, current_tag, tag_builder_properties)
        dummy_tags.append(current_tag)
    else:
        name_parts = [tag_builder_properties['tag_name'].split('.')][-1]
        name_parts.insert(0, device_name)
        Create_New_Tag(name_parts, tags, current_tag, tag_builder_properties)



def Populate_Tag_Builder_Properties(tag_builder_properties, device_name, row=None, is_tag_from_csv_flag=True) -> None:
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
            'data_type': row['Data Type'].iloc[0],
            'address': tag_builder_properties['row'].iloc[0, 1]
        })


def Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, collected_data=[], existing_tag_names=[]) -> None:
    if 'tags' in tag:
        for sub_tag in tag['tags']:

            if tag_builder_properties['tag_name_path'] != '':
                tag_builder_properties['tag_name_path'] = f'{tag_builder_properties['tag_name_path']}/{tag['name']}'
            else:
                tag_builder_properties['tag_name_path'] = tag['name']
            
            Process_Tag(generated_ingition_json, tag_builder_properties, key, df, sub_tag, collected_data=collected_data, existing_tag_names=existing_tag_names)
    else:
        if 'opcItemPath' in tag :
            # tag_builder_properties['tag_name'] = Extract_Tag_Name(tag['opcItemPath'])
            # tag_builder_properties['row'] = Find_Row_By_Tag_Name(df, tag_builder_properties['tag_name'])
            tag_builder_properties.update({
                'tag_name': Extract_Tag_Name(tag['opcItemPath']),
                'row': Find_Row_By_Tag_Name(df, Extract_Tag_Name(tag['opcItemPath']))
            })

            if not tag_builder_properties['row'].empty:
                existing_tag_names.append(tag_builder_properties['tag_name'])
                Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], is_tag_from_csv_flag=False, row=tag_builder_properties['row'])
                Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)
                Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], tag, tag_builder_properties)
                Update_Device_CSV(tag_builder_properties, collected_data)
            else:
                log_message(f"Could not find tag {tag_builder_properties['tag_name']} in CSV file {key}.csv so just leaving it as is", 'warning')

        else:
            log_message(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is', 'warning')
    Reset_Tag_Builder_Properties(tag_builder_properties)

def Update_Device_CSV(tag_builder_properties, collected_data):
    tag_name = ''
    if tag_builder_properties['data_type'] != '':

        if '/' in tag_builder_properties['tag_name_path']:
            tag_name = tag_builder_properties['tag_name_path'][tag_builder_properties['tag_name_path'].find('/') + 1:]
            tag_name = f'{tag_name}/{tag_builder_properties["tag_name"]}'
        else:
            tag_name = tag_builder_properties['tag_name']
            
        collected_data.append({
            'tag_name': tag_name,
            'address': f"{tag_builder_properties['area']}<{tag_builder_properties['path_data_type']}{tag_builder_properties['array_size']}>{tag_builder_properties['offset']}"
        })

def Finalize_Device_CSV(device_csv, key, collected_data):
    from pandas import DataFrame as pd_DataFrame
    from pandas import concat as pd_concat
    if collected_data:
        device_csv[key] = pd_concat([device_csv[key], pd_DataFrame(collected_data)], ignore_index=True)

def Process_CSV_Row(generated_ingition_json, tag_builder_properties, key, row, collected_data=[], existing_tag_names=[]) -> None:
    tag_builder_properties['tag_name'] = row['Tag Name']

    if tag_builder_properties['tag_name'] not in existing_tag_names:
        Populate_Tag_Builder_Properties(tag_builder_properties, generated_ingition_json[key]['name'], row)
        Convert_Tag_Builder_Properties_To_Mitsubishi_Format(tag_builder_properties)
        Process_Tag_Name(tag_builder_properties['device_name'], generated_ingition_json[key]['tags'], {}, tag_builder_properties)
        Update_Device_CSV(tag_builder_properties, collected_data)
        Reset_Tag_Builder_Properties(tag_builder_properties)


def Generate_Ignition_JSON_And_Address_CSV(csv_df, ignition_json) -> Dict[str, Any]:
    from pandas import DataFrame as pd_DataFrame
    generated_ingition_json = ignition_json
    device_csv = {key: pd_DataFrame() for key in csv_df}
    tag_builder_properties = Create_Tag_Builder_Properties()
    for key, df in csv_df.items():
        if key in ignition_json:
            collected_data = []
            existing_tag_names = []
            for tag in ignition_json[key]['tags']:
                Process_Tag(generated_ingition_json, tag_builder_properties, key, df, tag, collected_data=collected_data, existing_tag_names=existing_tag_names)
                
            for _, row in df.iterrows():
                Process_CSV_Row(generated_ingition_json, tag_builder_properties, key, row, collected_data, existing_tag_names)

            Finalize_Device_CSV(device_csv, key, collected_data)
        else:
            log_message(f"Could not find {key}.json in ignition JSON so skipping it", 'warning')
        del df

    return generated_ingition_json, device_csv
