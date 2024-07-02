import unittest 
import os
from tag_generator import *
import tag_generator.base.file_functions as file_functions
from tag_generator.base.tag_functions import *
import tag_generator.mitsubishi_tag_generator as mitsubishi_tag_generator
import pandas as pd
import json
from deepdiff import DeepDiff



class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_get_generated_ignition_json_and_csv_files(self):
        file_functions.remove_output_dir(os.path)
        file_functions.remove_log_dir(os.path)
        
        input_dir: str = os.path.join('src','tests','files','input', 'mitsubishi')
        output_dir: str = os.path.join('src','tests','files','output', 'mitsubishi')
        expected_output_dir: str = os.path.join('src','tests','files','expected_output', 'mitsubishi')
    
        json_files = file_functions.get_all_files(input_dir, '.json', os)
        csv_files = file_functions.get_all_files(input_dir, '.csv', os)

        logger = Logger()

        def generate_output(output_dir, csv_files, json_file) -> None:

            ignition_json = file_functions.get_dict_from_json_files(tuple([json_file]), os.path, json, logger=logger)
            for csv_file in csv_files:
                if file_functions.get_basename_without_extension(csv_file, os.path) in ignition_json.keys():
                    ignition_json, address_csv = mitsubishi_tag_generator.get_generated_ignition_json_and_csv_files(file_functions.get_dict_of_dfs_from_csv_files(tuple([csv_file]), os, pd) , ignition_json, pd, os.path, logger=logger)
                    file_functions.write_json_files(ignition_json, output_dir, os, json)
                    file_functions.write_csv_files(address_csv, output_dir, os)
                    break
                
        for json_file in json_files:
            generate_output(output_dir, csv_files, json_file)

        json_files = file_functions.get_all_files(output_dir, '.json', os)
        ignition_json = file_functions.get_dict_from_json_files(json_files, os.path,  json, is_test=True, logger=logger)

        address_csv = file_functions.get_all_files(output_dir, '.csv', os)
        address_csv = file_functions.get_dict_of_dfs_from_csv_files(address_csv, os, pd)

        expected_output_json_files = file_functions.get_all_files(expected_output_dir, '.json', os)
        expected_ignition_json = file_functions.get_dict_from_json_files(expected_output_json_files, os.path,  json, is_test=True, logger=logger)

        expected_output_csv_files = file_functions.get_all_files(expected_output_dir, '.csv', os)
        expected_address_csv = file_functions.get_dict_of_dfs_from_csv_files(expected_output_csv_files, os, pd)

        diff = DeepDiff(expected_ignition_json, ignition_json, ignore_order=True, verbose_level=2)
        if diff:
            self.fail(f"JSON files do not match: {diff}")

        # Loop through every element of both dataframes and compare them
        for key, df in address_csv.items():
            if key in expected_address_csv:
                pd.testing.assert_frame_equal(df, expected_address_csv[key])
            else:
                self.fail(f"Missing expected CSV for key: {key}")

        


        
        
        


if __name__ == '__main__':
    unittest.main()