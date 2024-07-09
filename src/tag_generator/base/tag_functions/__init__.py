#!/usr/bin/env python


def reset_tag_builder(tag_builder, TAG_BUILDER_TEMPLATE) -> None:
    tag_builder.update(TAG_BUILDER_TEMPLATE)
    
def find_row_by_tag_name(df, tag_name):
    """
    Finds the first row in a DataFrame that matches the given tag name.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to search in.
    - tag_name (str): The tag name to search for.

    Returns:
    - pandas.Series or None: The first row that matches the tag name, or None if no match is found.
    """
    row = df[df[r'Tag Name'] == tag_name]
    return row.iloc[0] if not row.empty else None


def extract_kepware_path(opc_item_path) -> str:
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

def extract_area_and_offset(address, ADDRESS_PATTERN) -> tuple:
    """
    Extracts the area and offset from the given address.

    Args:
        address (str): The address from which to extract the area and offset.

    Returns:
        tuple: A tuple containing the extracted area and offset.

    Raises:
        SystemExit: If no numbers are found in the address.

    """

    match = ADDRESS_PATTERN.search(address)
    if match:
        first_number_index = match.start()
        area = address[:first_number_index]
        if 'X' in address:
            offset = str(int(address[first_number_index:].lstrip('0') or '0', 16))
        else:
            offset = address[first_number_index:].lstrip('0') or '0'
            if offset.find('.') == 0:
                offset = '0' + offset
        return (area, offset)
    else:
        exit(f"Could not find any numbers in address {address}")

def get_offset_and_array_size(offset) -> tuple:
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
        array_size = array_size.lstrip('0')
        offset = offset.split('.')[0]

    return (offset, array_size)

def convert_data_type(data_type, DATA_TYPE_MAPPINGS) -> tuple:
    """
    Converts the given data type to its corresponding mapping in the DATA_TYPE_MAPPINGS dictionary.

    Args:
        data_type (str): The data type to be converted.
        DATA_TYPE_MAPPINGS (dict): A dictionary mapping data types to their corresponding OPC UA data types.

    Returns:
        tuple: A tuple containing the converted data type and an empty string if no mapping is found.

    """
    return DATA_TYPE_MAPPINGS.get(data_type, (data_type, ''))

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
        r'data_type': tag_builder['row']['Data Type']
    })
