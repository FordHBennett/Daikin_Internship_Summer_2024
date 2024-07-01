#!/usr/bin/env python

from collections import defaultdict

from matplotlib.pylab import f
from tag_generator.__main__ import logger 
from pandas import DataFrame as pd_DataFrame


def convert_data_type(data_type):
    from tag_generator.base.constants import DATA_TYPE_MAPPINGS
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))


def update_area_and_path_data_type(area, path_data_type=''):
    if 'SH' in area:
        path_data_type = r'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = r'Bool'
    return (area, path_data_type)

def convert_tag_builder_to_mitsubishi_format(tag_builder) -> None:
    from tag_generator.base.tag_functions import extract_area_and_offset, get_offset_and_array_size
    data_type, path_data_type = convert_data_type(tag_builder['data_type'])
    area, offset = extract_area_and_offset(tag_builder['address'])
    area, path_data_type = update_area_and_path_data_type(area, path_data_type)
    offset, array_size = get_offset_and_array_size(offset)

    if array_size:
        data_type = r'String'
    if r'String' not in path_data_type and array_size:
        array_size = f"[{array_size}]"

    tag_builder.update({
        r'data_type': data_type,
        r'path_data_type': path_data_type,
        r'area': area,
        r'offset': offset,
        r'array_size': array_size,
        
    })
def create_new_connected_tag(current_tag) -> None:
    current_tag.update({
        r"opcItemPath": f'ns=1;s=[{current_tag['opcItemPath'].split('=')[-1].split('.')[0]}][Diagnostics]/Connected',
        r"opcServer": r'Ignition OPC UA Server',
        r"dataType": r'String',
        r'valueSource': r'opc',
        r'tagGroup': r'default' # renove once prodcution
    })

def create_new_tag(current_tag, tag_builder) -> None:
    current_tag.update({
        r"name": current_tag['name'],
        r"opcItemPath": f"ns=1;s=[{current_tag['opcItemPath'].split('=')[-1].split('.')[0]}]{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}",
        r"opcServer": r'Ignition OPC UA Server',
        r"dataType": tag_builder['data_type'],
        r'valueSource': r'opc',
        r'tagGroup': r'default' # renove once prodcution 
    })



def process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, sub_tag):
    if tag_builder['tag_name_path']:
        tag_builder['tag_name_path'] = f'{tag_builder['tag_name_path']}/{tag['name']}'
    else:
        tag_builder['tag_name_path'] = tag['name']
            
    process_tag(ingition_json, tag_builder, key, df, sub_tag, tag_name_and_address_list=tag_name_and_address_list)


def process_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list=[]) -> None:
    from os.path import join as os_path_join
    from tag_generator.base.tag_functions import find_row_by_tag_name, extract_kepware_tag_name, reset_tag_builder
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, sub_tag)
    else:
        if 'opcItemPath' in tag:
            tag_builder.update({
                r'row': find_row_by_tag_name(df, extract_kepware_tag_name(tag['opcItemPath']))
            })
            if tag_builder['row'] is not None:
                update_tag_builder(tag_builder)
                update_tags(tag_builder, tag,  tag_name_and_address_list)
            else:
                create_new_connected_tag(tag)
        else:
            handle_opc_path_not_found(tag, os_path_join)

    reset_tag_builder(tag_builder)

def update_tags(tag_builder, current_tag, tag_name_and_address_list):
    convert_tag_builder_to_mitsubishi_format(tag_builder)
    create_new_tag(current_tag, tag_builder)
    update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag)



def update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag):
    if tag_builder['data_type'] and tag_builder['tag_name_path'] :
        tag_name_and_address_list.append({
            r'tag_name': f'{tag_builder['tag_name_path']}/{current_tag["name"]}',
            r'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
        })
    else:
        tag_name_and_address_list.append({
            r'tag_name': f'{current_tag["name"]}',
            r'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
        })


def finalize_address_csv_dict(device_csv, key, tag_name_and_address_list):
    if tag_name_and_address_list:
        device_csv[key] = pd_DataFrame(tag_name_and_address_list)

def update_tag_builder(tag_builder) -> None:
    tag_builder.update({
            r'kepware_tag_name': tag_builder['row']['Tag Name'],
            r'address': tag_builder['row']['Address'],
            r'data_type': tag_builder['row']['Data Type'],
    })


def get_generated_ignition_json_and_csv_files(kepware_df, ignition_json):
    from tag_generator.base.constants import TAG_BUILDER_TEMPLATE

    address_csv_dict = defaultdict(pd_DataFrame)
    tag_builder = TAG_BUILDER_TEMPLATE.copy()
    for key, df in kepware_df.items():
        if key in ignition_json:
            tag_name_and_address_list = []
            for tag in ignition_json[key]['tags']:
                process_tag(ignition_json, tag_builder, key, df, tag, tag_name_and_address_list=tag_name_and_address_list)
            
            key = ignition_json[key]['name']
            finalize_address_csv_dict(address_csv_dict, key, tag_name_and_address_list)

    return (ignition_json, address_csv_dict)

def log_missing_key_critical(os_path_join, key):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'critical.log'))
    logger.set_level('CRITICAL')
    logger.log_message(f"Could not find {key}.json in ignition JSON so skipping it", 'CRITICAL')


def handle_tag_not_found(tag_builder, key, os_path_join):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f"Could not find tag {tag_builder['kepware_tag_name']} in CSV file {key}.csv so just leaving it as is", 'INFO')

def handle_opc_path_not_found(tag, os_path_join):
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f'Could not find opcItemPath or dataType in tag {tag['name']} so just leaving it as is', 'INFO')


import os 

filePath = "C:"
basePath = "[default]Imported Tags"

# find the dir "files/output" starting from filePath
def import_tags_recursively(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print(os.path.join(root, dir))

import_tags_recursively(filePath)
                    

 
 