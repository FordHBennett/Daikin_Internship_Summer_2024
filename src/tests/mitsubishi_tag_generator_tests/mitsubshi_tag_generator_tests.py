import unittest 
import os
from mitsubishi_tag_generator.process_tags import *
from base.tag_functions import *
from base.file_functions import *
import pandas as pd
from shutil import rmtree
from base.logging_class import Logger
from deepdiff import DeepDiff



class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_get_generated_ignition_json_and_csv_files(self):
        input_dir: str = os.path.join('src','tests','files','input', 'mitsubishi')
        output_dir: str = os.path.join('src','tests','files','output', 'mitsubishi')
        expected_output_dir: str = os.path.join('src','tests','files','expected_output', 'mitsubishi')
    
        json_files = get_all_json_files(input_dir)
        csv_files = get_all_csv_files(input_dir)

        logger = Logger()

        for json_file in json_files:
            ignition_json = get_dict_from_json_files([json_file], logger=logger)
            for csv_file in csv_files:
                dummy_csv_file = get_basename_without_extension(csv_file)
                if dummy_csv_file in ignition_json.keys():
                    csv_df = get_dict_of_dfs_from_csv_files([csv_file])
                    ignition_json, address_csv = get_generated_ignition_json_and_csv_files(csv_df, ignition_json)
                    write_json_files(ignition_json, output_dir)
                    write_csv_files(address_csv, output_dir)

        json_files = get_all_json_files(output_dir)

        ignition_json = get_dict_from_json_files(json_files, is_test=True, logger=logger)

        expected_output_json_files = get_all_json_files(expected_output_dir)
        expected_ignition_json = get_dict_from_json_files(expected_output_json_files, is_test=True, logger=logger)

        expected_output_csv_files = get_all_csv_files(expected_output_dir)
        expected_address_csv = get_dict_of_dfs_from_csv_files(expected_output_csv_files)

        diff = DeepDiff(expected_ignition_json, ignition_json, ignore_order=True)
        if diff:
            self.fail(f"JSON files do not match: {diff}")

        # Loop through every element of both dataframes and compare them
        for key, df in address_csv.items():
            if key in expected_address_csv:
                pd.testing.assert_frame_equal(df, expected_address_csv[key])
            else:
                self.fail(f"Missing expected CSV for key: {key}")


        # rmtree(output_dir)



        
        
        


if __name__ == '__main__':
    unittest.main()