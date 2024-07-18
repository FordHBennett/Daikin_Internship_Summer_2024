#!/usr/bin/env python

import array
from re import M
from tag_generator.base.constants import ADDRESS_PATTERN, DATA_TYPE_MAPPINGS, TAG_BUILDER_TEMPLATE, DEVICE_NAME_MAPPINGS
from collections import defaultdict
import tag_generator.base.tag_functions as tag_functions
import tag_generator.base.file_functions as file_functions
import pandas as pd

# def process_sub_tag(
#                 ingition_json, 
#                 tag_builder,
#                 key, 
#                 df, 
#                 tag, 
#                 tag_name_and_addresses, 
#                 sub_tag, 
#                 logger,
#                 device) -> None:

#             if tag_builder['tag_name_path']:
#                 tag_builder['tag_name_path'] = f"{tag_builder['tag_name_path']}/{tag['name']}"
#             else:
#                 tag_builder['tag_name_path'] = tag['name']
                    
#             process_tag(
#                 ingition_json, 
#                 tag_builder, 
#                 key, 
#                 df, 
#                 sub_tag, 
#                 tag_name_and_addresses, 
#                 logger,
#                 device
#             )
            

# def process_tag(
#         ingition_json, 
#         tag_builder, 
#         key, 
#         df, 
#         tag, 
#         tag_name_and_addresses, 
#         logger,
#         device) -> None:
#     """
#     Process a tag based on the given parameters.

#     Args:
#         ingition_json (dict): The Ignition JSON data.
#         tag_builder (dict): The tag builder dictionary.
#         key (str): The key of the tag.
#         df (pandas.DataFrame): The DataFrame containing the tag data.
#         tag (dict): The tag dictionary.
#         tag_name_and_addresses (list): The list of tag names and addresses.
#         constants (module): The constants module.
#         logger (Logger): The logger object.

#     Returns:
#         None
#     """

#     if 'tags' in tag:

#         tuple(
#             map(
#                 lambda sub_tag: process_sub_tag(
#                     ingition_json, 
#                     tag_builder, 
#                     key, 
#                     df, 
#                     tag, 
#                     tag_name_and_addresses, 
#                     sub_tag, 
#                     logger,
#                     device
#                 ), 
#                 tag['tags']
#             )
#         )
#     else:
#         if tag['valueSource'] != 'expr' or tag['valueSource'] != 'memory':
#             if 'opcItemPath' in tag.keys():
#                 opc_item_path = tag['opcItemPath']
#                 if opc_item_path.startswith('nsu=ThingWorx') or opc_item_path.startswith('ns=2;'):
#                     kepware_path = tag_functions.extract_kepware_tag_name(opc_item_path)
#                     if not opc_item_path.endswith('_NoError') and not kepware_path.endswith('IsConnected'):
#                         tag_builder['row'] = tag_functions.find_row_by_tag_name(df, kepware_path)
#                         if tag_builder['row'] is None:
#                             kepware_path = opc_item_path.split('.', 1)[-1]
#                             tag_builder['row'] = tag_functions.find_row_by_tag_name(df, kepware_path)
#                         if tag_builder['row'] is not None:
#                             tag_functions.update_tag_builder(tag_builder)
#                             if device == 'mitsubishi':
#                                     convert_tag_builder_to_mitsubishi_format(tag_builder)
#                                     create_new_mitsubishi_tag(tag, tag_builder)
#                             elif device == 'cj':
#                                 convert_tag_builder_to_cj_format(tag_builder)
#                                 create_new_cj_tag(tag, tag_builder)
#                             update_tag_builder_wrt_tag_name_and_addresses(tag_builder, tag_name_and_addresses, tag)
#                         else:
#                             logger.log_message(f"Could not find {kepware_path} in coresponding Kepware CSV", device, 'warning')
#                     else:
#                         if device == 'mitsubishi':
#                             tag_functions.create_new_connected_tag(tag)
#                 else:
#                     logger.handle_opc_path_not_found(tag, key, device)
#             else:
#                 logger.handle_opc_path_not_found(tag, key, device)

#     tag_functions.reset_tag_builder(tag_builder, TAG_BUILDER_TEMPLATE)


                

def process_tag(
        ingition_json, 
        tag_builder, 
        key, 
        csv_files, 
        tag, 
        tag_name_and_addresses, 
        logger,
        device) -> None:
    
    if 'tags' in tag:
        for sub_tag in tag['tags']:
            if tag_builder['tag_name_path']:
                tag_builder['tag_name_path'] = f"{tag_builder['tag_name_path']}/{tag['name']}"
            else:
                tag_builder['tag_name_path'] = tag['name']
            process_tag(
                ingition_json, 
                tag_builder, 
                key, 
                csv_files, 
                sub_tag, 
                tag_name_and_addresses, 
                logger,
                device
            )
    else:
        if tag['valueSource'] != 'expr' or tag['valueSource'] != 'memory':
            if 'opcItemPath' in tag.keys():
                opc_item_path = tag['opcItemPath']
                if opc_item_path.startswith('nsu=ThingWorx') or opc_item_path.startswith('ns=2;'):
                    tag_builder['kepware_tag_name'] = tag_functions.extract_kepware_tag_name(opc_item_path)
                    if not opc_item_path.endswith('_NoError') and not tag_builder['kepware_tag_name'].endswith('IsConnected'):
                        for csv_file in csv_files:
                            csv_basename = file_functions.get_basename_without_extension(csv_file)
                            if csv_basename in tag['opcItemPath']:
                                df = pd.read_csv(csv_file)
                                tag_builder['row'] = tag_functions.find_row_by_tag_name(df, tag_builder['kepware_tag_name'])
                                tag_builder['device_name'] = DEVICE_NAME_MAPPINGS.get(csv_basename) or csv_basename
                                break
                        try:
                            if not tag_builder['row']:
                                for csv_file in csv_files:
                                    df = pd.read_csv(csv_file)
                                    tag_names = df['Tag Name'].values
                                    for name in tag_names:
                                        if tag_builder['kepware_tag_name'] in name:
                                            tag_builder['row'] = df[df['Tag Name'] == name].iloc[0]
                                            split_name = tag['opcItemPath'].split('=')
                                            split_name = split_name[-1].split('.')
                                            if len(split_name) > 1:
                                                tag_builder['device_name'] = split_name[1] 
                                            else:
                                                tag_builder['device_name'] = split_name[0]
                                            break
                        except:
                            pass

                        if tag_builder['row'] is not None:
                            tag_functions.update_tag_builder(tag_builder)
                            if device == 'mitsubishi':
                                convert_tag_builder_to_mitsubishi_format(tag_builder)
                                create_new_mitsubishi_tag(tag, tag_builder)
                            elif device == 'cj':
                                convert_tag_builder_to_cj_format(tag_builder)
                                create_new_cj_tag(tag, tag_builder) 
                            update_tag_builder_wrt_tag_name_and_addresses(tag_builder, tag_name_and_addresses, tag)
                        else:
                            logger.log_message(f"Could not find {tag_builder['kepware_tag_name']} in coresponding Kepware CSV", device, 'warning')
                    else:
                        tag_functions.create_new_connected_tag(tag)
                else:
                    logger.handle_opc_path_not_found(tag, key, device)
            else:
                logger.handle_opc_path_not_found(tag, key, device)

    dummy_tag_name_path = None
    if tag_builder['tag_name_path'] and '/' in tag_builder['tag_name_path']:
        dummy_tag_name_path = tag_builder['tag_name_path'][:tag_builder['tag_name_path'].rfind('/')]

    tag_functions.reset_tag_builder(tag_builder, TAG_BUILDER_TEMPLATE)
    tag_builder['tag_name_path'] = dummy_tag_name_path

def create_new_mitsubishi_tag(current_tag, tag_builder) -> None:
    """
    Edits the current tag dictionary to create a new tag based on the tag builder dictionary.

    Args:
        current_tag (dict): The current tag dictionary.
        tag_builder (dict): The tag builder dictionary.

    Returns:
        None
    """


    # Get the device name from the opcItemPath
    device_name = (current_tag['opcItemPath'].split('=')[-1]).split('.')[0]
    
    current_tag.update({
        r"name": current_tag['name'],
        r"opcItemPath": f"ns=1;s=[{device_name}]{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}",
        r"opcServer": r'Ignition OPC UA Server',
        # r"dataType": tag_builder['data_type'],
        r'valueSource': r'opc'
        # r'tagGroup': r'default' # remove once production-ready
    })

def create_new_cj_tag(current_tag, tag_builder) -> None:
        if tag_builder['tag_name_path']:
            device_name = tag_builder['tag_name_path'].split('/')[-1] 
            device_name = DEVICE_NAME_MAPPINGS.get(device_name)
            if device_name:
                tag_builder['device_name'] = device_name
            else:
                tag_builder['device_name'] = 'AAC01_MPLC'
            current_tag.update({
                r"name": current_tag['name'],
                r"opcItemPath": f"ns=1;s=[{device_name}]{tag_builder['area']}<{tag_builder['path_data_type']}>{tag_builder['offset']}",
                r"opcServer": r'Ignition OPC-UA Server',
                # r"dataType": tag_builder['data_type'],
                r'valueSource': r'opc',
                # r'tagGroup': r'default' # remove once production-ready
            })


def update_tag_builder_wrt_tag_name_and_addresses(tag_builder, tag_name_and_addresses, current_tag) -> None:
    """
    Update the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (dict): The tag builder dictionary.

        current_tag (dict): The current tag dictionary.

    Returns:
        None
    """

    tag_name = ''
    if tag_builder['tag_name_path']:
        tag_name = f"{tag_builder['tag_name_path']}/{current_tag['name']}"
    else:
        tag_name = current_tag['name']

    if tag_builder['area'] is not None:
        if tag_builder['device_name'] not in tag_name_and_addresses:
            tag_name_and_addresses[tag_builder['device_name']] = []
        if tag_builder['array_size']:
            tag_name_and_addresses[tag_builder['device_name']].append({
                'tag_name': tag_name,
                'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
            })
        else:
            tag_name_and_addresses[tag_builder['device_name']].append({
                'tag_name': tag_name,
                'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}>{tag_builder['offset']}"
            })
    else:
            if tag_builder['device_name'] not in tag_name_and_addresses:
                tag_name_and_addresses[tag_builder['device_name']] = []
            if tag_builder['array_size']:
                tag_name_and_addresses[tag_builder['device_name']].append({
                    'tag_name': tag_name,
                    'address': f"{tag_builder['address']}"
                })
            else:
                tag_name_and_addresses[tag_builder['device_name']].append({
                    'tag_name': tag_name,
                    'address': f"{tag_builder['address']}"
                })


def update_area_and_path_data_type(area, path_data_type='') -> tuple:
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
    Converts a tag builder dictionary to the Mitsubishi format.

    Args:
        tag_builder (dict): The tag builder dictionary containing the tag information.

    Returns:
        None
    """
    
    data_type, path_data_type = tag_functions.convert_data_type(tag_builder['data_type'], DATA_TYPE_MAPPINGS)
    area, offset = tag_functions.extract_area_and_offset(tag_builder['address'], ADDRESS_PATTERN)
    area, path_data_type = update_area_and_path_data_type(area, path_data_type)

    if 'String' == path_data_type:
        offset, array_size = tag_functions.get_offset_and_array_size(offset)
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



def convert_tag_builder_to_cj_format(tag_builder) -> None:

    data_type, path_data_type = tag_functions.convert_data_type(tag_builder['data_type'], DATA_TYPE_MAPPINGS)
    area = ''
    offset = ''
    if tag_builder['data_type'] == 'Word':
        area = 'W'
        offset = tag_builder['address'].split(':')[-1]
    elif tag_builder['data_type'] == 'String':
        length = tag_builder['address'].split('.')[-1]
        if 'H' in length:
            length = length[:-1]

        path_data_type = path_data_type + length
        area, offset = tag_builder['address'].split(':')
        offset = offset.split('.')[0]
        offset = offset.lstrip('0') or '0'
    elif ':' in tag_builder['address']:
        area, offset = tag_builder['address'].split(':')
        offset = tag_builder['address'].split(':')[-1]
    else:
        area, offset = tag_functions.extract_area_and_offset(tag_builder['address'], ADDRESS_PATTERN)
    
    area, path_data_type = update_area_and_path_data_type(area, path_data_type)

    tag_builder.update({
        r'data_type': data_type,
        r'path_data_type': path_data_type,
        r'area': area,
        r'offset': offset
    })





def get_generated_ignition_json_and_csv_files(
        kepware_df, 
        ignition_json, 
        DataFrame,
        device=None,
        logger=None) -> tuple:
    """
    Generate Ignition JSON and CSV files based on the provided Kepware DataFrame and Ignition JSON.

    Args:
        kepware_df (dict): A dictionary containing Kepware DataFrames.
        ignition_json (dict): The Ignition JSON data.
        DataFrame (class): The DataFrame class to be used.
        device (str, optional): The device name. Defaults to None.
        logger (object, optional): The logger object. Defaults to None.

    Returns:
        tuple: A tuple containing the generated Ignition JSON and a dictionary of CSV files.

    """
    address_csv_dict = defaultdict(DataFrame)
    tag_builder = TAG_BUILDER_TEMPLATE.copy()
    for key, df in kepware_df.items():
        tag_name_and_addresses = []
        if key in ignition_json:
            tuple(
                map(
                    lambda tag: process_tag(
                        ignition_json, 
                        tag_builder, 
                        key, 
                        df, 
                        tag, 
                        tag_name_and_addresses, 
                        logger,
                        device
                    ), 
                    ignition_json[key]['tags']
                )
            )
            
            if tag_name_and_addresses:
                address_csv_dict[next(iter(kepware_df))] = DataFrame(tag_name_and_addresses)
        else:
            logger.log_missing_key_critical(key, device)

    return (ignition_json, address_csv_dict)

def generate_files(
        csv_files:tuple,
        ignition_json:str,
        device:str,
        logger) -> tuple:
    
    address_csv_dict = defaultdict(pd.DataFrame)
    tag_builder = TAG_BUILDER_TEMPLATE.copy()
    tag_name_and_addresses = {}
    for key in ignition_json.keys():

        for tag in ignition_json[key]['tags']:
            process_tag(
                ignition_json, 
                tag_builder, 
                key, 
                csv_files, 
                tag, 
                tag_name_and_addresses, 
                logger,
                device
            )

    for key in tag_name_and_addresses.keys():
        address_csv_dict[key] = pd.DataFrame(tag_name_and_addresses[key])

    return (ignition_json, address_csv_dict)

