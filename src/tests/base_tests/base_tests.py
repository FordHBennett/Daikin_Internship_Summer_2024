from re import T
import unittest 
from base.base_functions import *

class Test_Base_Functions(unittest.TestCase):
    def test_get_basename_without_extension(self):
        self.assertEqual(Get_Basename_Without_Extension('src/base/base_functions.py'), 'base_functions')

    def test_remove_non_alphanumeric_characters(self):
        self.assertEqual(Remove_Non_Alphanumeric_Characters('tag_name!@#<>%$^&*'), 'tag_name')

    def test_get_all_keys(self):
        json_structure = {
            "key1": "value1",
            "key2": {
                "key3": "value3",
                "key4": {
                    "key5": "value5"
                }
            },
            "key6": [
                {
                    "key7": "value7"
                },
                {
                    "key8": "value8"
                }
            ]
        }
        expected_keys = {
            "key1": None,
            "key2": {
                "key3": None,
                "key4": {
                    "key5": None
                }
            },
            "key6": [
                {
                    "key7": None
                },
                {
                    "key8": None
                }
            ]
        }
        self.assertEqual(Get_All_Keys(json_structure), expected_keys)
    
    def test_get_all_keys_empty(self):
        json_structure = {}
        expected_keys = {}
        self.assertEqual(Get_All_Keys(json_structure), expected_keys)
    
    def test_get_all_keys_list(self):
        json_structure = {
            "key1": [
                {
                    "key2": "value2"
                }
            ]
        }
        expected_keys = {
            "key1": [
                {
                    "key2": None
                }
            ]
        }
        self.assertEqual(Get_All_Keys(json_structure), expected_keys)

    def test_Reset_Tag_Builder_Properties(self):
        dict = {
            "is_tag_from_csv_flag": True,
            "key2": {
                "key3": "value3",
                "key4": {
                    "key5": "value5"
                }
            },
            "key6": [
                {
                    "key7": "value7"
                },
                {
                    "key8": "value8"
                }
            ]
        }
        expected_dict = {
            "is_tag_from_csv_flag": False,
            "key2": {
                "key3": '',
                "key4": {
                    "key5": ''
                }
            },
            "key6": [
                {
                    "key7": ''
                },
                {
                    "key8": ''
                }
            ]
        }
        Reset_Tag_Builder_Properties(dict)
        self.assertEqual(dict, expected_dict)

    def test_extract_tag_name(self):
        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.PLC_PHS_Heartbeat'
        expected_tag_name = 'PLC_PHS_Heartbeat'
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

    def test_extract_tag_name_with_no_tag_name(self):
        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.'
        expected_tag_name = ''
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

    def test_extract_tag_name_with_no_tag_name_and_no_period(self):
        tag_name = 'A_KanseiConveyorMA_KanseiConveyor'
        expected_tag_name = 'A_KanseiConveyorMA_KanseiConveyor'
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)
        
    def test_extract_area_and_offset(self):
        address = 'RTY000023456.000000987456789'
        expected_area = 'RTY'
        expected_offset = '23456.000000987456789'

        self.assertEqual(Extract_Area_And_Offset(address), (expected_area, expected_offset))
    
    def test_extract_offset_and_array_size(self):
        offset = '23456.000000987456789'
        expected_offset = '23456'
        expected_array_size = '987456789'

        self.assertEqual(Extract_Offset_And_Array_Size(offset), (expected_offset, expected_array_size))

if __name__ == '__main__':
    unittest.main()