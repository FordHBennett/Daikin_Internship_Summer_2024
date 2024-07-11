#!/usr/bin/env python
"""
This module contains constants used in the tag generator.

- `ADDRESS_PATTERN`: Regular expression pattern to match numeric addresses.
- `TAG_NAME_PATTERN`: Regular expression pattern to match invalid characters in tag names.
- `DATA_TYPE_MAPPINGS`: Mapping of data types to their corresponding OPC UA data types.
- `READ_WRITE_MAPPINGS`: Mapping of read-only and read-write properties.
- `REQUIRED_KEYS`: List of keys required in the tag builder template.
- `TAG_BUILDER_TEMPLATE`: Template for building tags with placeholder values.
"""

import re

ADDRESS_PATTERN:re.Pattern = re.compile(r'\d+')
TAG_NAME_PATTERN:re.Pattern = re.compile(r'[^a-zA-Z0-9-_ .]')

DATA_TYPE_MAPPINGS:dict = {
    r'Short': ('Int2', 'Int16'),
    r'Int2': ('Int2', 'Int16'),
    r'Word': ('Int4', 'Int16'),
    r'Integer': ('Int4', 'Int32'),
    r'Int4': ('Int4', 'Int32'),
    r'BCD': ('Int4', 'Int16'),
    r'Boolean': ('Boolean', 'Bool')
}

# READ_WRITE_MAPPINGS:dict = {
#     r'RO' :  True,
#     r'R/W' : False
# }

# REQUIRED_KEYS:tuple = (r'tagGroup', r'dataType', r'tagType', r'historyProvider', r'historicalDeadband', r'historicalDeadbandStyle')

TAG_BUILDER_TEMPLATE = {
    r"path_data_type": None,
    r"data_type": None,
    r"tag_name": None,
    r"tag_name_path": None,
    r"address": None,
    r"area": None,
    r"offset": None,
    r"array_size": None,
    r"row": None,
    r"kepware_tag_name": None,
    r"readOnly": None
}