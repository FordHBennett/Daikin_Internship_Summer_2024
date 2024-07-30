#!/usr/bin/env python

def reset_tag_builder(tag_builder: dict, TAG_BUILDER_TEMPLATE: dict) -> None:
    """
    Reset the tag builder dictionary with the provided template.

    Args:
        tag_builder (dict): The tag builder dictionary to be reset.
        TAG_BUILDER_TEMPLATE (dict): The template dictionary to reset the tag builder.

    Returns:
        None
    """
    tag_builder.update(TAG_BUILDER_TEMPLATE)
    
def find_row_by_tag_name(df, tag_name:str):
    """
    Finds the first row in a DataFrame that matches the given tag name.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to search in.
    - tag_name (str): The tag name to search for.

    Returns:
    - pandas.Series or None: The first row that matches the tag name, or None if no match is found.
    """
    if tag_name in df['Tag Name'].values:
        try:
            return df.loc[df['Tag Name'] == tag_name].iloc[0]
        except Exception as e:
            print(f"Error finding row by tag name: {tag_name}")
            raise e
    else:
        return None



def extract_kepware_tag_name(opc_item_path:str) -> str:
    """
    Extracts the Kepware path from the given OPC item path.

    Args:
        opc_item_path (str): The OPC item path.

    Returns:
        str: The extracted Kepware path.
    """
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.', 2)[-1]

def extract_kepware_device_name(opc_item_path: str) -> str:
    """
    Extracts the device name from the OPC item path.

    Args:
        opc_item_path (str): The OPC item path.

    Returns:
        str: The extracted device name.
    """
    if '.' not in opc_item_path:
        return opc_item_path
    return opc_item_path.split('.')[1]

def extract_area_and_offset(address:str, ADDRESS_PATTERN) -> tuple:
    """
    Extracts the area and offset from the given address.

    Args:
        address (str): The address from which to extract the area and offset.
        ADDRESS_PATTERN (pattern): The regular expression pattern used to match the address.

    Returns:
        tuple: A tuple containing the extracted area and offset.

    Raises:
        SystemExit: If no numbers are found in the address.

    """

    match = ADDRESS_PATTERN.search(address)
    if match:
        if ':' in address:
            area, offset = address.split(':')
            return (area, offset)
        else:
            first_number_index = match.start()
            area = address[:first_number_index]
            if 'X' in address:
                try:
                    offset = str(int(address[first_number_index:].lstrip('0') or '0', 16))
                except ValueError:
                    offset = address[first_number_index:].lstrip('0') or '0'
            else:
                offset = address[first_number_index:].lstrip('0') or '0'
                if offset.find('.') == 0:
                    offset = '0' + offset
            return (area, offset)
    else:
        raise(f"Could not find any numbers in address {address}")

def get_offset_and_array_size(offset:str) -> tuple:
    """
    Splits the given offset into offset and array size.

    Args:
        offset (str): The offset value.

    Returns:
        tuple: A tuple containing the offset and array size.
    """
    array_size = ''
    if '.' in offset:
        array_size = offset.split('.')[1]
        array_size = array_size.lstrip('0') or '0'
        offset = offset.split('.')[0]
        offset = offset.lstrip('0')

    return (offset, array_size)

def convert_data_type(data_type:str, DATA_TYPE_MAPPINGS:dict) -> tuple:
    """
    Converts the given data type to its corresponding mapping in the DATA_TYPE_MAPPINGS dictionary.

    Args:
        data_type (str): The data type to be converted.
        DATA_TYPE_MAPPINGS (dict): A dictionary mapping data types to their corresponding OPC UA data types.

    Returns:
        tuple: A tuple containing the converted data type and an empty string if no mapping is found.

    """
    try:
        return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))
    except Exception as e:
        print(f"{data_type} is not currently supported. Please add it to the DATA_TYPE_MAPPINGS dictionary.")
        raise e 

def create_new_connected_tag(current_tag: dict) -> None:
    """
    Creates a new connected tag based on the current tag.

    Args:
        current_tag (dict): The current tag to create a connected tag from.

    Returns:
        None
    """
    current_tag.update({
        r"opcItemPath": f'ns=1;s=[{current_tag['opcItemPath'].split('=')[-1].split('.')[0]}][Diagnostics]/Connected',
        r"opcServer": r'Ignition OPC UA Server',
        r"dataType": r'String',
        r"valueSource": r'opc',
        # r'tagGroup': r'default' # remove once production
    })

def update_tag_builder(tag_builder:dict) -> None:
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
        r'data_type': tag_builder['row']['Data Type']
    })

def check_if_system_tag(opc_item_path:str) -> bool:
    """
    Check if the given OPC item path corresponds to a system tag.

    Args:
        opc_item_path (str): The OPC item path to check.

    Returns:
        bool: True if the OPC item path corresponds to a system tag, False otherwise.
    """
    invalid_kepware_tags = ['_NoError', '_Error', 'IsConnected', '_Enabled', '_SystemStatus']
    for tag in invalid_kepware_tags:
        if opc_item_path.endswith(tag):
            return True
    
    invalid_strings = ['._System.', 'DPMPHS4VM']
    for string in invalid_strings:
        if string in opc_item_path:
            return True
    
    return False