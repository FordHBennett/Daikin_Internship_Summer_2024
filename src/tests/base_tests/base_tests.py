from re import T
import unittest 
from base.base_functions import *
from base.base_file_functions import *
class Test_Base_Functions(unittest.TestCase):
    def test_get_basename_without_extension(self):
        self.assertEqual(Get_Basename_Without_Extension('src/base/base_functions.py'), 'base_functions')

    def test_Remove_Invalid_Tag_Name_Characters(self):
        #Remove special characters
        tag_name = "Hello, World!"
        expected_result = "Hello World"
        self.assertEqual(Remove_Invalid_Tag_Name_Characters(tag_name), expected_result)

        #Retain alphanumeric characters
        tag_name = "abc123"
        expected_result = "abc123"
        self.assertEqual(Remove_Invalid_Tag_Name_Characters(tag_name), expected_result)

        #Retain hyphen and underscore
        tag_name = "my-tag_name"
        expected_result = "my-tag_name"
        self.assertEqual(Remove_Invalid_Tag_Name_Characters(tag_name), expected_result)

        #Remove all characters except hyphen, underscore, space and dot
        tag_name = "!@#$%^&*()_+-=[]{}|; ':,.<>/?"
        expected_result = "_- ."
        self.assertEqual(Remove_Invalid_Tag_Name_Characters(tag_name), expected_result)


    def test_get_all_keys(self):
        #Test with nested dictionary and list
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

        #Test with empty dictionary
        json_structure = {}
        expected_keys = {}
        self.assertEqual(Get_All_Keys(json_structure), expected_keys)

        #Test with nested dictionary
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


    def test_extract_tag_name(self):
        #Test with tag name containing multiple periods
        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.PLC_PHS_Heartbeat'
        expected_tag_name = 'PLC_PHS_Heartbeat'
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

        #Test with tag name containing one period
        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.'
        expected_tag_name = ''
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

        #Test with tag name containing no periods
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