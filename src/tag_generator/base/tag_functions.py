#!/usr/bin/env python

def remove_invalid_tag_name_characters(tag_name):
    """
    Removes invalid characters from a tag name.

    Args:
        tag_name (str): The tag name to remove invalid characters from.

    Returns:
        str: The tag name with invalid characters removed.
    """
    from tag_generator.base.constants import TAG_NAME_PATTERN
    return TAG_NAME_PATTERN.sub('', tag_name)

def get_tag_builder():
    """
    Returns a copy of the TAG_BUILDER_TEMPLATE.

    This function retrieves the TAG_BUILDER_TEMPLATE from the tag_generator.base.constants module
    and returns a copy of it.

    Returns:
        dict: A copy of the TAG_BUILDER_TEMPLATE.

    """
    from tag_generator.base.constants import TAG_BUILDER_TEMPLATE
    return TAG_BUILDER_TEMPLATE.copy()

def reset_tag_builder(tag_builder= {}) -> None:
    """
    Resets the tag builder dictionary to its initial state.

    Parameters:
    - tag_builder (dict): The tag builder dictionary to be reset. Defaults to an empty dictionary.

    Returns:
    - None
    """
    from tag_generator.base.constants import TAG_BUILDER_TEMPLATE
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


def extract_kepware_path(opc_item_path):
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

def extract_area_and_offset(address):
    """
    Extracts the area and offset from the given address.

    Args:
        address (str): The address from which to extract the area and offset.

    Returns:
        tuple: A tuple containing the extracted area and offset.

    Raises:
        SystemExit: If no numbers are found in the address.

    """
    from tag_generator.base.constants import ADDRESS_PATTERN
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
        return area, offset
    else:
        exit(f"Could not find any numbers in address {address}")

def get_offset_and_array_size(offset):
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

