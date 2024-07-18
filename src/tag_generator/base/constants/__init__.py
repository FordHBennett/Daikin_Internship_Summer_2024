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
    r'Boolean': ('Boolean', 'Bool'),
    r'String': ('String', 'String'),
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
    r'device_name': None
}

DEVICE_NAME_MAPPINGS:dict = {
    '1ST_CHARGE_1': 'AAC01_1stCharge01',
    '1ST_CHARGE_2': 'AAC01_1stCharge02',
    '1ST_CHARGE_3': '1ST_CHARGE_3',
    '1ST_CHARGE_4': '1ST_CHARGE_4',
    '1ST_LEAKTEST_1': 'AAC01_1stLC01',
    '1ST_LEAKTEST_2': 'AAC01_1stLC02',
    '1ST_LEAKTEST_3': 'AAC01_1stLC03',
    '1ST_LEAKTEST_4': 'AAC01_1stLC04',
    '1ST_LEAKTEST_5': 'AAC01_1stLC05',
    '2ND_CHARGE_1': 'AAC01_2ndCharge01',
    '2ND_CHARGE_2': 'AAC01_2ndCharge02',
    '2ND_LEAKTEST_1': '2ND_LEAKTEST_1',
    'DIAGNOSTICS': 'DIAGNOSTICS',
    'EVAC_1': 'AAC01_EVAC01',
    'EVAC_2': 'AAC01_EVAC02',
    'EVAC_3': 'AAC01_EVAC03',
    'EVAC_4': 'AAC01_EVAC04',
    'EVAC_5': 'AAC01_EVAC05',
    'EVAC_6': 'AAC01_EVAC06',
    'EVAC_7': 'AAC01_EVAC07',
    'EVAC_8': 'AAC01_EVAC08',
    'EVAC_9': 'AAC01_EVAC09',
    'EVAC_10': 'AAC01_EVAC10',
    'EVAC_11': 'AAC01_EVAC11',
    'EVAC_12': 'AAC01_EVAC12',
    'HIPOT' : 'AAC01_HIPOT',
    'KAISHI_CONV' : 'Kaishi_Conv',
    'KANSEI_CONV' : 'Kansei_Conv',
    'MPLC' : 'AAC01_MPLC',
    'MPLCV' : 'AAC01_MPLC',
    'N2_1' : 'AAC01_N2_1',
    'N2_2' : 'AAC01_N2_2',
    'N2_3' : 'AAC01_N2_3',
    'N2_4' : 'AAC01_N2_4',
    'N2_5' : 'AAC01_N2_5',
    'N2_6' : 'AAC01_N2_6',
    'N2_7' : 'AAC01_N2_7',
    'N2_8' : 'AAC01_N2_8',
    'N2_9' : 'AAC01_N2_9',
    'N2_10' : 'AAC01_N2_10',
    'RUNTEST_1' : 'RUNTEST_1',
    'RUNTEST_2' : 'RUNTEST_2',
    'RUNTEST_3' : 'RUNTEST_3',
    'MA_RE1' : 'RFID_LT1',
    'MA_HiPot' : 'RFID_HIPOT',
    'MA_KaishiConveyor' : 'Kaishi_Conv',
    'MA_KanseiConveyor' : 'Kansei_Conv',
    'MA_PD1' : 'RFID_PD1',
    'MA_LC1' : 'RFID_LT1',
    'MA_RE1' : 'RFID_RC1'
}

