#!/usr/bin/env python

from collections import defaultdict

from matplotlib.pylab import f
from tag_generator.__main__ import logger 
from pandas import DataFrame as pd_DataFrame


def convert_data_type(data_type):
    """
    Converts the given data type to its corresponding data type mapping.

    Args:
        data_type (str): The data type to be converted.

    Returns:
        tuple: A tuple containing the converted data type and an empty string if no mapping is found.

    """
    from tag_generator.base.constants import DATA_TYPE_MAPPINGS
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))


def update_area_and_path_data_type(area, path_data_type=''):
    """
    Updates the area and path data type based on the given area.

    Args:
        area (str): The area string.
        path_data_type (str, optional): The path data type. Defaults to ''.

    Returns:
        tuple: A tuple containing the updated area and path data type.
    """
    if 'SH' in area:
        path_data_type = r'String'
        area = area.replace('SH', '')
    if 'Z' in area:
        area = area.replace('Z', '')
    if 'M' in area:
        path_data_type = r'Bool'
    return (area, path_data_type)

def convert_tag_builder_to_mitsubishi_format(tag_builder) -> None:
    """
    Converts the data_type, path_data_type, area, and offset in the tag builder dictionary to Mitsubishi format.

    Args:
        tag_builder (dict): The tag builder dictionary containing the tag information.

    Returns:
        None
    """
    from tag_generator.base.tag_functions import extract_area_and_offset, get_offset_and_array_size
    data_type, path_data_type = convert_data_type(tag_builder['data_type'])
    area, offset = extract_area_and_offset(tag_builder['address'])
    area, path_data_type = update_area_and_path_data_type(area, path_data_type)

    if r'String' in path_data_type:
        offset, array_size = get_offset_and_array_size(offset)
        tag_builder.update({
            r'data_type': data_type,
            r'path_data_type': path_data_type,
            r'area': area,
            r'offset': offset,
            r'array_size': array_size,    
        })
    else:
        tag_builder.update({
            r'data_type': data_type,
            r'path_data_type': path_data_type,
            r'area': area,
            r'offset': offset,
            r'array_size': ''
        })


def create_new_connected_tag(current_tag) -> None:
    """
    Creates a new connected tag based on the current tag.

    Args:
        current_tag: The current tag to create a connected tag from.

    Returns:
        None
    """
    current_tag.update({
        r"opcItemPath": f'ns=1;s=[{current_tag['opcItemPath'].split('=')[-1].split('.')[0]}][Diagnostics]/Connected',
        r"opcServer": r'Ignition OPC UA Server',
        r"dataType": r'String',
        r'valueSource': r'opc',
        # r'tagGroup': r'default' # remove once production
    })

def create_new_tag(current_tag, tag_builder) -> None:
    """
    Edits the current tag dictionary to create a new tag based on the tag builder dictionary.

    Args:
        current_tag (dict): The current tag dictionary.
        tag_builder (dict): The tag builder dictionary.

    Returns:
        None
    """
    current_tag.update({
        r"name": current_tag['name'],
        r"opcItemPath": f"ns=1;s=[{current_tag['opcItemPath'].split('=')[-1].split('.')[0]}]{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}",
        r"opcServer": r'Ignition OPC UA Server',
        r"dataType": tag_builder['data_type'],
        r'valueSource': r'opc',
        # r'tagGroup': r'default' # remove once production-ready
    })



def process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, sub_tag):
    """
    Process a sub-tag by updating the tag name path and calling the process_tag function recursively.

    Args:
        ingition_json (dict): The Ignition JSON object.
        tag_builder (dict): The tag builder dictionary.
        key (str): The key for the current tag.
        df (pandas.DataFrame): The DataFrame containing the tag data.
        tag (dict): The tag dictionary.
        tag_name_and_address_list (list): The list of tag names and addresses.
        sub_tag (dict): The sub-tag dictionary.

    Returns:
        None
    """
    if tag_builder['tag_name_path']:
        tag_builder['tag_name_path'] = f"{tag_builder['tag_name_path']}/{tag['name']}"
    else:
        tag_builder['tag_name_path'] = tag['name']
            
    process_tag(ingition_json, tag_builder, key, df, sub_tag, tag_name_and_address_list=tag_name_and_address_list)


def process_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list=[]) -> None:
    """
    Process a tag and update the tag builder and tag list.

    Args:
        ingition_json (dict): The Ignition JSON data.
        tag_builder (dict): The tag builder dictionary.
        key (str): The key of the tag.
        df (pandas.DataFrame): The DataFrame containing the tag data.
        tag (dict): The tag dictionary to process.
        tag_name_and_address_list (list, optional): The list of tag names and addresses. Defaults to [].

    Returns:
        None
    """
    from os.path import join as os_path_join
    from tag_generator.base.tag_functions import find_row_by_tag_name, extract_kepware_path, reset_tag_builder

    if 'tags' in tag:
        for sub_tag in tag['tags']:
            process_sub_tag(ingition_json, tag_builder, key, df, tag, tag_name_and_address_list, sub_tag)
    else:
        if 'opcItemPath' in tag:
            tag_builder.update({
                r'row': find_row_by_tag_name(df, extract_kepware_path(tag['opcItemPath']))
            })
            if tag_builder['row'] is not None:
                update_tag_builder(tag_builder)
                update_tags(tag_builder, tag,  tag_name_and_address_list)
            else:
                create_new_connected_tag(tag)
        elif tag['valueSource'] == 'expr':
            pass
        else:
            handle_opc_path_not_found(tag, key, os_path_join)

    reset_tag_builder(tag_builder)

def update_tags(tag_builder, current_tag, tag_name_and_address_list):
    """
    Updates the tags by converting the tag builder to Mitsubishi format,
    creating a new tag based on the current tag and tag builder,
    and updating the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (TagBuilder): The tag builder object.
        current_tag (Tag): The current tag object.
        tag_name_and_address_list (list): A list of tag names and addresses.

    Returns:
        None
    """
    convert_tag_builder_to_mitsubishi_format(tag_builder)
    create_new_tag(current_tag, tag_builder)
    update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag)



def update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag):
    """
    Update the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (dict): The tag builder dictionary.
        tag_name_and_address_list (list): The list of tag names and addresses.
        current_tag (dict): The current tag dictionary.

    Returns:
        None
    """
    if tag_builder['data_type'] and tag_builder['tag_name_path']:
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
    """
    Finalizes the address CSV dictionary by adding the tag name and address list.

    Args:
        device_csv (dict): The device CSV dictionary.
        key (str): The key to be used in the device CSV dictionary.
        tag_name_and_address_list (list): The list of tag names and addresses.

    Returns:
        None
    """
    if tag_name_and_address_list:
        device_csv[key] = pd_DataFrame(tag_name_and_address_list)

def update_tag_builder(tag_builder) -> None:
    """
    Updates the tag_builder dictionary with the values from the 'row' dictionary.

    Args:
        tag_builder (dict): The tag_builder dictionary to be updated.

    Returns:
        None
    """
    tag_builder.update({
        r'kepware_tag_name': tag_builder['row']['Tag Name'],
        r'address': tag_builder['row']['Address'],
        r'data_type': tag_builder['row']['Data Type'],
    })


def get_generated_ignition_json_and_csv_files(kepware_df, ignition_json):
    """
    Generates Ignition JSON and CSV files based on the provided Kepware DataFrame and Ignition JSON.

    Args:
        kepware_df (dict): A dictionary containing Kepware DataFrames.
        ignition_json (dict): The Ignition JSON data.

    Returns:
        tuple: A tuple containing the generated Ignition JSON and a dictionary of address CSV files.
    """
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
    """
    Logs a critical message when a key is missing in the ignition JSON.

    Args:
        os_path_join (function): A function to join multiple path components.
        key (str): The key that is missing in the ignition JSON.

    Returns:
        None
    """
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'critical.log'))
    logger.set_level('CRITICAL')
    logger.log_message(f"Could not find {key}.json in ignition JSON so skipping it", 'CRITICAL')


def handle_tag_not_found(tag_builder, key, os_path_join):
    """
    Handles the case when a tag is not found in the CSV file.

    Args:
        tag_builder (dict): The tag builder object.
        key (str): The key of the CSV file.
        os_path_join (function): The function used to join file paths.

    Returns:
        None
    """
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f"Could not find tag {tag_builder['kepware_tag_name']} in CSV file {key}.csv so just leaving it as is", 'INFO')

def handle_opc_path_not_found(tag, device_name, os_path_join):
    """
    Handles the case when the opcItemPath or dataType is not found in the given tag.

    Args:
        tag (dict): The tag dictionary containing the tag information.
        os_path_join (function): The function used to join file paths.

    Returns:
        None

    Raises:
        None
    """
    logger.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
    logger.set_level('INFO')
    logger.log_message(f"Could not find opcItemPath or dataType in tag {tag['name']} in the file {device_name}.json so just leaving it as is", 'INFO')
