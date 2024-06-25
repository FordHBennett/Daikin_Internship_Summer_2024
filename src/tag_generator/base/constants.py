#!/usr/bin/env python

from re import compile as re_compile

ADDRESS_PATTERN = re_compile(r'\d+')
TAG_NAME_PATTERN = re_compile(r'[^a-zA-Z0-9-_ .]')

DATA_TYPE_MAPPINGS = {
    'Short': ('Int2', 'Int16'),
    'Int2': ('Int2', 'Int16'),
    'Word': ('Int2', 'Int16'),
    'Integer': ('Int4', 'Int32'),
    'Int4': ('Int4', 'Int32'),
    'BCD': ('Int4', 'Int32'),
    'Boolean': ('Boolean', 'Bool')
}

REQUIRED_KEYS = ['tagGroup', 'dataType', 'tagType', 'historyProvider', 'historicalDeadband', 'historicalDeadbandStyle']

TAG_BUILDER_TEMPLATE = {
    "path_data_type": None,
    "data_type": None,
    "tag_name": None,
    "tag_name_path": None,
    "address": None,
    "area": None,
    "offset": None,
    "array_size": None,
    "row": None,
    "device_name": None,
    "kepware_tag_name": None,
    "is_tag_from_csv_flag": False
}

