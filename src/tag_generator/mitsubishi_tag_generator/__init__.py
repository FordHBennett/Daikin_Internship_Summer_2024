#!/usr/bin/env python


def process_tag(
        ingition_json, 
        tag_builder, 
        key, 
        df, 
        tag, 
        tag_name_and_address_list, 
        constants, 
        logger, 
        path) -> None:
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

    
    import tag_generator.base.tag_functions as tag_functions

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
                path) -> None:
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
                path)
            
        for sub_tag in tag['tags']:
            process_sub_tag(
                ingition_json, 
                tag_builder, 
                key, 
                df, 
                tag, 
                tag_name_and_address_list, 
                sub_tag, 
                constants, 
                logger, 
                path)
    else:
        if 'opcItemPath' in tag:
            if('nsu=ThingWorx Kepware Server' in tag['opcItemPath'] or 'nsu=2' in tag['opcItemPath']):
                tag_builder.update({
                    r'row': tag_functions.find_row_by_tag_name(df, tag_functions.extract_kepware_path(tag['opcItemPath']))
                })
                if tag_builder['row'] is not None:
                    tag_functions.update_tag_builder(tag_builder)
                    update_tags(
                        tag_builder, 
                        tag,  
                        tag_name_and_address_list, 
                        tag_functions, 
                        constants)
                    
                elif '_NoError' in tag['opcItemPath']:
                    tag_functions.create_new_connected_tag(tag)
                else:
                    logger.handle_tag_not_found(tag_builder, key, path.join)
        elif tag['valueSource'] == 'expr':
            pass
        else:
            logger.handle_opc_path_not_found(tag, key, path.join)

    tag_functions.reset_tag_builder(tag_builder, constants)

def update_tags(
        tag_builder, 
        current_tag, 
        tag_name_and_address_list, 
        tag_functions, 
        constants) -> None:
    """
    Updates the tags by converting the tag builder to Mitsubishi format,
    creating a new tag based on the current tag and tag builder,
    and updating the tag builder with respect to the tag name and address list.

    Args:
        tag_builder (TagBuilder): The tag builder object.
        current_tag (Tag): The current tag object.
        tag_name_and_address_list (list): A list of tag names and addresses.
        tag_functions (module): The tag functions module.
        constants (module): The constants module.

    Returns:
        None
    """
    def convert_tag_builder_to_mitsubishi_format(tag_builder, tag_functions, constants) -> None:
        """
        Converts a tag builder dictionary to the Mitsubishi format.

        Args:
            tag_builder (dict): The tag builder dictionary containing the tag information.
            tag_functions (module): The tag functions module.
            constants(module): The constants module.

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
        
        data_type, path_data_type = tag_functions.convert_data_type(tag_builder['data_type'], constants)
        area, offset = tag_functions.extract_area_and_offset(tag_builder['address'], constants)
        area, path_data_type = update_area_and_path_data_type(area, path_data_type)

        if r'String' in path_data_type:
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

    convert_tag_builder_to_mitsubishi_format(tag_builder, tag_functions, constants)
    create_new_tag(current_tag, tag_builder)
    update_tag_builder_wrt_tag_name_and_address_list(tag_builder, tag_name_and_address_list, current_tag)


def get_generated_ignition_json_and_csv_files(
        kepware_df, 
        ignition_json, 
        pd, 
        path, 
        logger=None) -> tuple:
    """
    Generates Ignition JSON and CSV files based on the provided Kepware DataFrame and Ignition JSON.

    Args:
        kepware_df (dict): A dictionary containing Kepware DataFrames.
        ignition_json (dict): A dictionary containing Ignition JSON data.
        pd(module): The pandas module.
        path (module): The path module.
        logger (object): (optional) A logger object for logging messages.

    Returns:
        tuple: A tuple containing the generated Ignition JSON and a dictionary of generated CSV files.
    """

    import tag_generator.base.constants as constants
    from collections import defaultdict

    address_csv_dict = defaultdict(pd.DataFrame)
    tag_builder = constants.TAG_BUILDER_TEMPLATE.copy()
    for key, df in kepware_df.items():
        if key in ignition_json:
            tag_name_and_address_list = []
            for tag in ignition_json[key]['tags']:
                process_tag(
                    ignition_json, 
                    tag_builder, 
                    key, 
                    df, 
                    tag, 
                    tag_name_and_address_list, 
                    constants, 
                    logger, 
                    path)
            
            key = ignition_json[key]['name']

            if tag_name_and_address_list:
                address_csv_dict[key] = pd.DataFrame(tag_name_and_address_list)
        else:

            logger.log_missing_key_critical(key)

    return (ignition_json, address_csv_dict)

