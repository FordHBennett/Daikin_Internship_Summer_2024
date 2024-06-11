from math import e
import unittest 
from mitsubishi_tag_generator.process_tags import *
from base.base_functions import *
import os

class Test_Mitsubishi_Tag_Generator(unittest.TestCase):


    


    def test_modify_tags_for_direct_driver_communication(self):

        input_dir: str = os.path.join('src','tests','test_files','input_files', 'mitsubishi_devices')
        output_dir: str = os.path.join('src','tests','test_files','output_files', 'mitsubishi_devices')
        expected_output_dir: str = os.path.join('src','tests','test_files','expected_output_files', 'mitsubishi_devices')
    
        json_files = Get_ALL_JSON_Paths(input_dir)
        csv_files = Get_ALL_CSV_Paths(input_dir)

        ignition_json = Read_Json_Files(json_files)
        csv_df = Read_CSV_Files(csv_files)

        ignition_json = Modify_Tags_For_Direct_Driver_Communication(csv_df, ignition_json)
        Write_Json_Files(ignition_json, output_dir)

        # check if the contents of the output_files are the same as the expected_output_files
        output_files = Get_ALL_JSON_Paths(output_dir)
        expected_output_files = Get_ALL_JSON_Paths(expected_output_dir)

        output_json = Read_Json_Files(output_files)
        expected_output_json = Read_Json_Files(expected_output_files)

        self.assertEqual(output_json, expected_output_json)
        
        
        


if __name__ == '__main__':
    unittest.main()