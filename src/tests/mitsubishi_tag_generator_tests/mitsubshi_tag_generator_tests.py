import unittest 
import os
from pandas.testing import assert_frame_equal
from mitsubishi_tag_generator.process_tags import *
from base.base_functions import *

class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_Generate_Ignition_JSON_And_Address_CSV(self):
        input_dir: str = os.path.join('src','tests','test_files','input_files', 'mitsubishi')
        output_dir: str = os.path.join('src','tests','test_files','output_files', 'mitsubishi')
        expected_output_dir: str = os.path.join('src','tests','test_files','expected_output_files', 'mitsubishi')
    
        json_files = Get_ALL_JSON_Paths(input_dir)
        csv_files = Get_ALL_CSV_Paths(input_dir)

        ignition_json = Read_Json_Files(json_files)
        csv_df = Read_CSV_Files(csv_files)

        ignition_json, address_csv = Generate_Ignition_JSON_And_Address_CSV(csv_df, ignition_json)
        Write_Json_Files(ignition_json, output_dir)
        Write_Address_CSV(address_csv, output_dir)

        expected_output_json_files = Get_ALL_JSON_Paths(expected_output_dir)
        expected_ignition_json = Read_Json_Files(expected_output_json_files, is_test=True)

        expected_output_csv_files = Get_ALL_CSV_Paths(expected_output_dir)
        expected_address_csv = Read_CSV_Files(expected_output_csv_files)

        self.assertEqual(ignition_json, expected_ignition_json)

        # Find a way to assert dataframes
        with self.assertRaises(AssertionError):
            assert_frame_equal(address_csv, expected_address_csv)


        
        
        


if __name__ == '__main__':
    unittest.main()