#!/usr/bin/env python

from re import compile as re_compile


ADDRESS_PATTERN = re_compile(r'\d+')
TAG_NAME_PATTERN = re_compile(r'[^a-zA-Z0-9-_ .]')

DATA_TYPE_MAPPINGS = {
    r'Short': ('Int2', 'Int16'),
    r'Int2': ('Int2', 'Int16'),
    r'Word': ('Int2', 'Int16'),
    r'Integer': ('Int4', 'Int32'),
    r'Int4': ('Int4', 'Int32'),
    r'BCD': ('Int4', 'Int32'),
    r'Boolean': ('Boolean', 'Bool')
}

REQUIRED_KEYS = [r'tagGroup', r'dataType', r'tagType', r'historyProvider', r'historicalDeadband', r'historicalDeadbandStyle']

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
    r"is_tag_from_csv_flag": False
}

