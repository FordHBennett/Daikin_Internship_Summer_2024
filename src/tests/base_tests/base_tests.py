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

        
    
    

if __name__ == '__main__':
    unittest.main()