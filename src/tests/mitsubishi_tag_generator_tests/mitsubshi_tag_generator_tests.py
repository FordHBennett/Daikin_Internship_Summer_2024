import unittest 
import os
from mitsubishi_tag_generator.process_tags import *
from base.tag_functions import *
from base.file_functions import *
import pandas as pd
from shutil import rmtree
from base.logging_class import Logger



class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_get_generated_ignition_json_and_csv_files(self):
        input_dir: str = os.path.join('src','tests','files','input', 'mitsubishi')
        output_dir: str = os.path.join('src','tests','files','output', 'mitsubishi')
        expected_output_dir: str = os.path.join('src','tests','files','expected_output', 'mitsubishi')
    
        json_files = get_all_json_files(input_dir)
        csv_files = get_all_csv_files(input_dir)

        logger = Logger()

        ignition_json = get_dict_from_json_files(json_files, logger=logger)
        csv_df = get_dict_of_dfs_from_csv_files(csv_files)

        ignition_json, address_csv = get_generated_ignition_json_and_csv_files(csv_df, ignition_json)
        write_json_files(ignition_json, output_dir)
        write_csv_files(address_csv, output_dir)

        expected_output_json_files = get_all_json_files(expected_output_dir)
        expected_ignition_json = get_dict_from_json_files(expected_output_json_files, is_test=True, logger=logger)

        expected_output_csv_files = get_all_csv_files(expected_output_dir)
        expected_address_csv = get_dict_of_dfs_from_csv_files(expected_output_csv_files)

        self.assertEqual(ignition_json, expected_ignition_json)

        # Loop through every element of both dataframes and compare them
        for key, df in address_csv.items():
            if key in expected_address_csv:
                pd.testing.assert_frame_equal(df, expected_address_csv[key])
            else:
                self.fail(f"Missing expected CSV for key: {key}")

        # Check for any extra keys in expected_address_csv that were not processed
        for key in expected_address_csv.keys():
            if key not in address_csv:
                self.fail(f"Expected CSV for key {key} was not processed")


        rmtree(output_dir)



        
        
        


if __name__ == '__main__':
    unittest.main()