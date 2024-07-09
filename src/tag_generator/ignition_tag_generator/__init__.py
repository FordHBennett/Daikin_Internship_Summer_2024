#!/usr/bin/env python

import tag_generator.base.constants as constants
from collections import defaultdict
import tag_generator.base.tag_functions as tag_functions


def process_tag(
        ingition_json, 
        tag_builder, 
        key, 
        df, 
        tag, 
        tag_name_and_address_list, 
        constants, 
        logger,
        device) -> None:
    """
    Process a tag based on the given parameters.

    Args:
        ingition_json (dict): The Ignition JSON data.
        tag_builder (dict): The tag builder dictionary.
        key (str): The key of the tag.
        df (pandas.DataFrame): The DataFrame containing the tag data.
        tag (dict): The tag dictionary.
        tag_name_and_address_list (list): The list of tag names and addresses.
        constants (module): The constants module.
        logger (Logger): The logger object.

    Returns:
        None
    """

    if 'tags' in tag:
        def process_sub_tag(
                ingition_json, 
                tag_builder,
                key, 
                df, 
                tag, 
                tag_name_and_address_list, 
                sub_tag, 
                constants, 
                logger,
                device) -> None:
            """
            Process a sub tag by updating the tag name path and calling the process_tag function recursively.

            Args:
                ingition_json (dict): The Ignition JSON object.
                tag_builder (dict): The tag builder dictionary.
                key (str): The key for the current sub tag.
                df (pandas.DataFrame): The DataFrame containing the tag data.
                tag (dict): The tag dictionary.
                tag_name_and_address_list (list): The list of tag names and addresses.
                sub_tag (dict): The sub tag dictionary.
                constants (module): The constants module.
                logger (Logger): The logger object.
                path (module): The path module.

            Returns:
                None
            """
            if tag_builder['tag_name_path']:
                tag_builder['tag_name_path'] = f"{tag_builder['tag_name_path']}/{tag['name']}"
            else:
                tag_builder['tag_name_path'] = tag['name']
                    
            process_tag(
                ingition_json, 
                tag_builder, 
                key, 
                df, 
                sub_tag, 
                tag_name_and_address_list, 
                constants, 
                logger,
                device)
            
        list(
            map(
                lambda sub_tag: process_sub_tag(
                    ingition_json, 
                    tag_builder, 
                    key, 
                    df, 
                    tag, 
                    tag_name_and_address_list, 
                    sub_tag, 
                    constants, 
                    logger,
                    device
                ), 
                tag['tags']
            )
        )
    else:
        if tag['valueSource'] != 'expr':
            if 'opcItemPath' in tag.keys():
                opc_item_path = tag['opcItemPath']
                if opc_item_path.startswith('nsu=ThingWorx') or opc_item_path.startswith('ns=2;'):
                    kepware_path = tag_functions.extract_kepware_path(opc_item_path)
                    if not opc_item_path.endswith('_NoError') and not kepware_path.endswith('IsConnected'):
                        tag_builder['row'] = tag_functions.find_row_by_tag_name(df, kepware_path)
                        if tag_builder['row'] is None:
                            kepware_path = opc_item_path.split('.', 1)[-1]
                            tag_builder['row'] = tag_functions.find_row_by_tag_name(df, kepware_path)
                        if tag_builder['row'] is not None:
                            tag_functions.update_tag_builder(tag_builder)
                            if device == 'mitsubishi':
                                update_mitsubishi_tags(tag_builder, tag, tag_name_and_address_list, tag_functions, constants.ADDRESS_PATTERN, constants.DATA_TYPE_MAPPINGS)
                            elif device == 'cj':
                                tag_builder['address'] = tag_builder['address'].replace(':', '')
                                data_type, path_data_type = tag_functions.convert_data_type(tag_builder['data_type'], constants.DATA_TYPE_MAPPINGS)
                                tag_builder.update({
                                    r'data_type': data_type,
                                    r'path_data_type': path_data_type
                                })
                                create_new_tag(tag, tag_builder, device)
                                update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, tag)
                        else:
                            logger.log_message(f"Could not find {kepware_path} in coresponding Kepware CSV", device, 'warning')
                    else:
                        tag_functions.create_new_connected_tag(tag)
                else:
                    logger.handle_opc_path_not_found(tag, key, device)
            else:
                logger.handle_opc_path_not_found(tag, key, device)

    tag_functions.reset_tag_builder(tag_builder, constants.TAG_BUILDER_TEMPLATE)

def create_new_tag(current_tag, tag_builder, device) -> None:
    """
    Edits the current tag dictionary to create a new tag based on the tag builder dictionary.

    Args:
        current_tag (dict): The current tag dictionary.
        tag_builder (dict): The tag builder dictionary.

    Returns:
        None
    """
    device_name = (current_tag['opcItemPath'].split('=')[-1]).split('.')[0]

    if device == 'mitsubishi':
        current_tag.update({
            r"name": current_tag['name'],
            r"opcItemPath": f"ns=1;s=[{device_name}]{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}",
            r"opcServer": r'Ignition OPC UA Server',
            # r"dataType": tag_builder['data_type'],
            r'valueSource': r'opc'
            # r'tagGroup': r'default' # remove once production-ready
        })
    elif device == 'cj':
        current_tag.update({
            r"name": current_tag['name'],
            r"opcItemPath": f"ns=1;s=[{device_name}]{tag_builder['address']}",
            r"opcServer": r'Ignition OPC UA Server',
            # r"dataType": tag_builder['data_type'],
            r'valueSource': r'opc',
            # r'tagGroup': r'default' # remove once production-ready
        })


def update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag) -> None:
    """
    Update the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (dict): The tag builder dictionary.
        tag_name_and_address_list (list): The list of tag names and addresses.
        current_tag (dict): The current tag dictionary.

    Returns:
        None
    """
    if tag_builder['data_type'] and tag_builder['tag_name_path'] and tag_builder['area'] is not None:
        tag_name_and_address_list.append({
            r'tag_name': f'{tag_builder['tag_name_path']}/{current_tag["name"]}',
            r'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
        })
    elif tag_builder['area'] is None:
        if tag_builder['kepware_tag_name'].find('.') != -1:
            name_parts = tag_builder['kepware_tag_name'].split('.')
            name = name_parts[0]
            for i in range(1, len(name_parts)):
                if i<(len(name_parts[i]) -1):
                    name = f"{name}/{name_parts[i]}" 

                
            tag_name_and_address_list.append({
                r'tag_name': f'{name}/{current_tag["name"]}',
                r'address': f"{tag_builder['address']}"
            })
        # tag_name_and_address_list.append({
        #     r'tag_name': f'{current_tag["name"]}',
        #     r'address': f"{tag_builder['address']}"
        # })
    else:
        tag_name_and_address_list.append({
            r'tag_name': f'{current_tag["name"]}',
            r'address': f"{tag_builder['area']}<{tag_builder['path_data_type']}{tag_builder['array_size']}>{tag_builder['offset']}"
        })

def update_mitsubishi_tags(
        tag_builder, 
        current_tag, 
        tag_name_and_address_list, 
        tag_functions, 
        ADDRESS_PATTERN,
        DATA_TYPE_MAPPINGS) -> None:
    """
    Updates the tags by converting the tag builder to Mitsubishi format,
    creating a new tag based on the current tag and tag builder,
    and updating the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (TagBuilder): The tag builder object.
        current_tag (Tag): The current tag object.
        tag_name_and_address_list (list): A list of tag names and addresses.
        tag_functions (module): The tag functions module.
        ADDRESS_PATTERN (re.Pattern): A regular expression pattern used to match numerical addresses.
        DATA_TYPE_MAPPINGS (dict): A dictionary mapping data types to their corresponding OPC UA data types.

    Returns:
        None
    """
    def convert_tag_builder_to_mitsubishi_format(tag_builder, tag_functions, ADDRESS_PATTERN, DATA_TYPE_MAPPINGS) -> None:
        """
        Converts a tag builder dictionary to the Mitsubishi format.

        Args:
            tag_builder (dict): The tag builder dictionary containing the tag information.
            tag_functions (module): The tag functions module.
            ADDRESS_PATTERN (re.Pattern): A regular expression pattern used to match numerical addresses.
            DATA_TYPE_MAPPINGS (dict): A dictionary mapping data types to their corresponding OPC UA data types.

        Returns:
            None
        """
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


    convert_tag_builder_to_mitsubishi_format(tag_builder, tag_functions, ADDRESS_PATTERN, DATA_TYPE_MAPPINGS)
    create_new_tag(current_tag, tag_builder, 'mitsubishi')
    update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag)

def get_generated_ignition_json_and_csv_files(
        kepware_df, 
        ignition_json, 
        DataFrame,
        device=None,
        logger=None) -> tuple:
    """
    Generates Ignition JSON and CSV files based on the provided Kepware DataFrame and Ignition JSON.

    Args:
        kepware_df (dict): A dictionary containing Kepware DataFrames.
        ignition_json (dict): A dictionary containing Ignition JSON data.
        pd(module): The pandas module.
        logger (object): (optional) A logger object for logging messages.

    Returns:
        tuple: A tuple containing the generated Ignition JSON and a dictionary of generated CSV files.
    """

    address_csv_dict = defaultdict(DataFrame)
    tag_builder = constants.TAG_BUILDER_TEMPLATE.copy()
    for key, df in kepware_df.items():
        tag_name_and_address_list = []
        if key in ignition_json:
            list(
                map(
                    lambda tag: process_tag(
                        ignition_json, 
                        tag_builder, 
                        key, 
                        df, 
                        tag, 
                        tag_name_and_address_list, 
                        constants, 
                        logger,
                        device
                    ), 
                    ignition_json[key]['tags']
                )
            )
            
            if tag_name_and_address_list:
                address_csv_dict[ignition_json[key]['name']] = DataFrame(tag_name_and_address_list)
        else:
            logger.log_missing_key_critical(key, device)

    return (ignition_json, address_csv_dict)

