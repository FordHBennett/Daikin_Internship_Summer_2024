#!/usr/bin/env python
 
from tag_generator.base.constants import ADDRESS_PATTERN, DATA_TYPE_MAPPINGS, TAG_BUILDER_TEMPLATE, DEVICE_NAME_MAPPINGS
from collections import defaultdict
import tag_generator.base.tag_functions as tag_functions
import tag_generator.base.file_functions as file_functions
import pandas as pd

def process_tag(
        ingition_json, 
        tag_builder, 
        key, 
        csv_files, 
        tag, 
        tag_name_and_addresses, 
        logger,
        manufacturer) -> None:
    
    # Check if the tag has sub-tags
    if 'tags' in tag:

        # Iterate over all the sub-tags
        for sub_tag in tag['tags']:

            # If the tag has a tag name path, update it with the sub-tag name to keep track of the tag hierarchy
            if tag_builder['tag_name_path']:
                tag_builder['tag_name_path'] = f"{tag_builder['tag_name_path']}/{tag['name']}"
            # Otherwise, set the tag name path to the sub-tag name
            else:
                tag_builder['tag_name_path'] = tag['name']
            
            # Process the sub-tag
            process_tag(
                ingition_json, 
                tag_builder, 
                key, 
                csv_files, 
                sub_tag, 
                tag_name_and_addresses, 
                logger,
                manufacturer
            )
    # If the tag does not have sub-tags
    else:
        # Check if the tag is not a memory or expression tag
        if tag['valueSource'] != 'expr' or tag['valueSource'] != 'memory':

            # Check if the tag has an opcItemPath
            if 'opcItemPath' in tag.keys():
                opc_item_path = tag['opcItemPath']

                # Check if the opcItemPath starts with 'nsu=ThingWorx' or 'ns=2;'
                if opc_item_path.startswith('nsu=ThingWorx') or opc_item_path.startswith('ns=2;'):

                    # Extract the Kepware tag name from the opcItemPath and update the tag builder
                    tag_builder['kepware_tag_name'] = tag_functions.extract_kepware_tag_name(opc_item_path)

                    # Check if the Kepware tag name is not None and does not end with '_NoError' or 'IsConnected'
                    if not opc_item_path.endswith('_NoError') and not tag_builder['kepware_tag_name'].endswith('IsConnected'):

                        # Iterate over all the CSV files
                        for csv_file in csv_files:
                            csv_basename = file_functions.get_basename_without_extension(csv_file)

                            # Check if the Kepware tag name is in the CSV file name and the CSV file name does not contain 'MPLC'
                            if csv_basename in tag['opcItemPath']and 'MPLC' not in csv_basename:

                                # Read the CSV file and find the row by the Kepware tag name
                                df = pd.read_csv(csv_file)


                                # if '.' not in tag_builder['kepware_tag_name']:
                                #     tag_builder['row'] = tag_functions.find_row_by_tag_name(df, tag_builder['kepware_tag_name'])
                                # else:
                                tag_builder['row'] = tag_functions.find_row_by_tag_name(df, tag_builder['kepware_tag_name'])
                                while(tag_builder['row'] is None or tag_builder['kepware_tag_name'].find('.') != -1):
                                    tag_builder['row'] = tag_functions.find_row_by_tag_name(df, tag_builder['kepware_tag_name'])
                                    tag_builder['kepware_tag_name'] = tag_builder['kepware_tag_name'][tag_builder['kepware_tag_name'].find('.') + 1:]
                                        

                                # Update the tag builder with the device name from the CSV file name 
                                # If the device name is not found in the mappings, use the first part of the Kepware tag name
                                tag_builder['device_name'] = DEVICE_NAME_MAPPINGS.get(csv_basename) or csv_basename
                                
                                # Break the loop because kepware row is found
                                if tag_builder['row']  is not None:
                                    break
                        try:
                            # If the tag builder row is still None, iterate over all the CSV files again
                            if tag_builder['row'] is not None:
                                for csv_file in csv_files:

                                    # Read the CSV file
                                    df = pd.read_csv(csv_file)
                                    tag_names = df['Tag Name'].values

                                    # Iterate over all the tag names in the CSV file
                                    for name in tag_names:

                                        # Check if the Kepware tag name is in the tag name
                                        if tag_builder['kepware_tag_name'] in name:

                                            # Find the row by the tag name and update the tag builder
                                            tag_builder['row'] = df[df['Tag Name'] == name].iloc[0]

                                            # Update the tag builder with the device name from the CSV file name
                                            split_name = tag['opcItemPath'].split('=')
                                            kepware_path = split_name[-1]
                                            kepware_path = '.'.join(kepware_path.split('.')[:3])
                                            tag_builder['device_name'] = DEVICE_NAME_MAPPINGS.get(kepware_path) or kepware_path.split('.')[1] or kepware_path.split('.')[0]

                                            # Break the loop because kepware row is found
                                            break
                        except:
                            pass
                        
                        # Check if the tag builder row was found
                        if tag_builder['row'] is not None:

                            # Update the tag builder with the tag information
                            tag_functions.update_tag_builder(tag_builder)

                            # Check the manufacturer of the device
                            if manufacturer == 'mitsubishi':

                                # Update the tag builder with the Mitsubishi format
                                convert_tag_builder_to_mitsubishi_format(tag_builder)

                                # Create a new Mitsubishi tag
                                create_new_mitsubishi_tag(tag, tag_builder)
                            elif manufacturer == 'cj':

                                # Update the tag builder with the CJ format
                                convert_tag_builder_to_cj_format(tag_builder)

                                # Create a new CJ tag
                                create_new_cj_tag(tag, tag_builder) 
                            
                            # Update the tag builder with respect to the tag name and addresses
                            update_tag_builder_wrt_tag_name_and_addresses(tag_builder, tag_name_and_addresses, tag)

                        # If the tag builder row was not found, log a message
                        else:
                            logger.log_message(f"Could not find {tag_builder['kepware_tag_name']} in coresponding Kepware CSV", manufacturer, 'warning')
                    
                    # If the Kepware tag name ends with '_NoError' or 'IsConnected' create a new connected tag
                    else:
                        tag_functions.create_new_connected_tag(tag)
                # If the opcItemPath does not start with 'nsu=ThingWorx' or 'ns=2;' log a message
                else:
                    logger.handle_opc_path_not_found(tag, key, manufacturer)
            else:
                logger.handle_opc_path_not_found(tag, key, manufacturer)

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
        # if tag_builder['tag_name_path']:
            # device_name = tag_builder['tag_name_path'].split('/')[-1] 
            # device_name = DEVICE_NAME_MAPPINGS.get(device_name)
            # if device_name:
            #     tag_builder['device_name'] = device_name
            # else:
            #     tag_builder['device_name'] = 'AAC01_MPLC'
        current_tag.update({
            r"name": current_tag['name'],
            r"opcItemPath": f"ns=1;s=[{tag_builder['device_name']}]{tag_builder['area']}<{tag_builder['path_data_type']}>{tag_builder['offset']}",
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
        manufacturer:str,
        logger) -> tuple:
    """
    Generate address CSV files and update the Ignition JSON file with tag information.

    Args:
        csv_files (tuple): A tuple of CSV files.
        ignition_json (str): The path to the Ignition JSON file.
        manufacturer (str): The manufacturer name.
        logger: The logger object for logging messages.

    Returns:
        tuple: A tuple containing the updated Ignition JSON and a dictionary of address CSV files.
    """

    # Create a dictionary of DataFrames from the CSV files
    address_csv_dict = defaultdict(pd.DataFrame)

    # Create a copy of the tag builder template
    tag_builder = TAG_BUILDER_TEMPLATE.copy()

    # Create a dictionary to store the tag names and addresses
    tag_name_and_addresses = {}

    # Iterate over all the tags in the Ignition JSON
    for key in ignition_json.keys():

        # Iterate over all the tags in the Ignition JSON
        for tag in ignition_json[key]['tags']:
            # Process the tag
            process_tag(
                ignition_json, 
                tag_builder, 
                key, 
                csv_files, 
                tag, 
                tag_name_and_addresses, 
                logger,
                manufacturer
            )

    for key in tag_name_and_addresses.keys():
        address_csv_dict[key] = pd.DataFrame(tag_name_and_addresses[key])

    return (ignition_json, address_csv_dict)

