#!/usr/bin/env python

# import gc
# import profile
# from typing import Dict, Any, Tuple
from collections import defaultdict


from tag_generator.__main__ import logger 
from functools import lru_cache
from pandas import DataFrame as pd_DataFrame
# from memory_profiler import profile

@lru_cache(maxsize=None)
def convert_data_type(data_type: str):
    # from base.constants import DATA_TYPE_MAPPINGS
    from tag_generator.base.constants import DATA_TYPE_MAPPINGS
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))


def update_area_and_path_data_type(area: str, path_data_type: str=''):
    if 'SH' in area:
        path_data_type = 'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = 'Bool'
    return area, path_data_type

def convert_tag_builder_to_mitsubishi_format(tag_builder) -> None:
    # from base.tag_functions import extract_area_and_offset, get_offset_and_array_size
    from tag_generator.base.tag_functions import extract_area_and_offset, get_offset_and_array_size
    data_type, path_data_type = convert_data_type(tag_builder['data_type'])
    area, offset = extract_area_and_offset(tag_builder['address'])
    area, path_data_type = update_area_and_path_data_type(area, path_data_type)
    offset, array_size = get_offset_and_array_size(offset)

    if array_size:
        data_type = 'String'
    if 'String' not in path_data_type and array_size:
        array_size = f"[{array_size}]"

    tag_builder.update({
        'data_type': data_type,
        'path_data_type': path_data_type,
        'area': area,
        'offset': offset,
        'array_size': array_size
    })


def create_new_tag(name_parts, tags, current_tag, tag_builder) -> None:
    # from base.tag_functions import generate_full_path_from_name_parts, set_tag_properties
    from tag_generator.base.tag_functions import generate_full_path_from_name_parts, set_tag_properties
    tag_builder.update({
        'tag_name': name_parts[-1],
        'tag_name_path': generate_full_path_from_name_parts(name_parts)
    })

    new_tag = {
        "name": tag_builder['tag_name'],
        "opcItemPath": f"ns=1;s=[{tag_builder['device_name']}]{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}",
        "opcServer": 'Ignition OPC UA Server',
        "dataType": tag_builder['data_type'],
        'valueSource': 'opc'
    }

    if tag_builder['is_tag_from_csv_flag']:
        set_tag_properties(tags=tags, new_tag=new_tag)
    else:
        set_tag_properties(new_tag=new_tag, current_tag=current_tag)
    
    current_tag.update(new_tag)


def process_tag_name(tags, tag_builder, current_tag=None) -> None:
    # from base.tag_functions import build_tag_hierarchy, remove_invalid_tag_name_characters
    from tag_generator.base.tag_functions import build_tag_hierarchy, remove_invalid_tag_name_characters
    if current_tag is None:
        current_tag = {}

    if tag_builder['is_tag_from_csv_flag']:
        name_parts = [remove_invalid_tag_name_characters(part) for part in tag_builder['kepware_tag_name'].split('.')]

        name_parts.insert(0, 'kepware')
        dummy_tags = build_tag_hierarchy(tags, name_parts)

        create_new_tag(name_parts, tags, current_tag, tag_builder)
        dummy_tags.append(current_tag)
    else:
        name_parts = [tag_builder['kepware_tag_name'].split('.')[-1]] or [tag_builder['kepware_tag_name']]
        if tag_builder['tag_name_path']:
            name_parts.insert(0, tag_builder['tag_name_path'])
        create_new_tag(name_parts, tags, current_tag, tag_builder)

def handle_tag_not_found(tag_builder, key, os_path_join):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f"Could not find tag {tag_builder['kepware_tag_name']} in CSV file {key}.csv so just leaving it as is", 'INFO')

def handle_opc_path_not_found(tag, os_path_join):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is', 'INFO')

def process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, processed_tags, sub_tag):
    if tag_builder['tag_name_path']:
        tag_builder['tag_name_path'] = f'{tag_builder['tag_name_path']}/{tag['name']}'
    else:
        tag_builder['tag_name_path'] = tag['name']
            
    process_tag(ingition_json, tag_builder, key, df, sub_tag, tag_name_and_address_list=tag_name_and_address_list, processed_tags=processed_tags)


def process_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list=[], processed_tags=[]) -> None:
    from os.path import join as os_path_join
    from tag_generator.base.tag_functions import find_row_by_tag_name, extract_kepware_tag_name, reset_tag_builder
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, processed_tags, sub_tag)
    else:
        if 'opcItemPath' in tag:
                tag_builder.update({
                    'row': find_row_by_tag_name(df, extract_kepware_tag_name(tag['opcItemPath']))
                })

                
                if tag_builder['row'] is not None:
                    update_tag_builder(ingition_json, tag_builder, key)
                    processed_tags.append(tag_builder['kepware_tag_name'])
                    update_tags(tag_builder, tag, ingition_json[key]['tags'], tag_name_and_address_list)

                else:
                    handle_tag_not_found(tag_builder, key, os_path_join)
        else:
            handle_opc_path_not_found(tag, os_path_join)

    reset_tag_builder(tag_builder)

def update_tags(tag_builder, current_tag, tags, tag_name_and_address_list):
    convert_tag_builder_to_mitsubishi_format(tag_builder)
    process_tag_name(tags, tag_builder, current_tag=current_tag)
    update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list)



def update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list):
    if tag_builder['data_type']:
        tag_name_and_address_list.append({
            'tag_name': tag_builder['tag_name_path'],
            'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
        })

def finalize_address_csv_dict(device_csv, key, tag_name_and_address_list):
    from pandas import concat as pd_concat
    if tag_name_and_address_list:
        device_csv[key] = pd_concat([device_csv[key], pd_DataFrame(tag_name_and_address_list)], ignore_index=True)

def generate_df_from_kepware(ignition_json, tag_builder, key, tag_name_and_address_list, row) -> None:
    # from base.tag_functions import reset_tag_builder
    from tag_generator.base.tag_functions import reset_tag_builder
    tag_builder.update({'row': row})
    update_tag_builder(ignition_json, tag_builder, key, is_tag_from_csv_flag=True)
    update_tags(tag_builder, {}, ignition_json[key]['tags'], tag_name_and_address_list)
    reset_tag_builder(tag_builder)

def update_tag_builder(ignition_json, tag_builder, key, is_tag_from_csv_flag=False) -> None:
    tag_builder.update({
            'kepware_tag_name': tag_builder['row']['Tag Name'],
            'is_tag_from_csv_flag': is_tag_from_csv_flag,
            'device_name': ignition_json[key]['name'],
            'address': tag_builder['row']['Address'],
            'data_type': tag_builder['row']['Data Type']
        })

# @profile
def get_generated_ignition_json_and_csv_files(kepware_df, ignition_json):
    # from base.tag_functions import get_tag_builder
    from tag_generator.base.tag_functions import get_tag_builder
    address_csv_dict = defaultdict(pd_DataFrame)
    tag_builder = get_tag_builder()
    for key, df in kepware_df.items():
        if key in ignition_json:
            tag_name_and_address_list = []
            processed_tags = []
            for tag in ignition_json[key]['tags']:
                process_tag(ignition_json, tag_builder, key, df, tag, tag_name_and_address_list=tag_name_and_address_list, processed_tags=processed_tags)

            # drop all rows that have been processed
            df = df[~df['Tag Name'].isin(processed_tags)]
                
            for _, row in df.iterrows():
                generate_df_from_kepware(ignition_json, tag_builder, key, tag_name_and_address_list, row)

            finalize_address_csv_dict(address_csv_dict, key, tag_name_and_address_list)
        # else:
        #     log_missing_key_critical(os_path_join, key)



    return (ignition_json, address_csv_dict)

def log_missing_key_critical(os_path_join, key):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'critical.log'))
    logger.set_level('CRITICAL')
    logger.log_message(f"Could not find {key}.json in ignition JSON so skipping it", 'CRITICAL')
