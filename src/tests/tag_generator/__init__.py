import unittest 
import os
from tag_generator import  generate_output_using_all_csv_files
import tag_generator.base.file_functions as file_functions
from tag_generator.base.tag_functions import *

from deepdiff import DeepDiff



class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_get_generated_ignition_json_and_csv_files(self):
        os.chdir('src')
        os.chdir('tests')

        file_functions.clean_files_dir()

        
        input_dir: str = os.path.join('files','input', 'mitsubishi')
        output_dir: str = os.path.join('files','output', 'mitsubishi')
        expected_output_dir: str = os.path.join('files','expected_output', 'mitsubishi')
    
        json_files = file_functions.get_all_files(input_dir, '.json')
        csv_files = file_functions.get_all_files(input_dir, '.csv')


        # list(map(lambda json_file: generate_output(output_dir, csv_files, json_file, 'mitsubishi'), json_files))
        for json_file in json_files:
            generate_output_using_all_csv_files(output_dir, csv_files, json_file, 'mitsubishi')


        json_files = file_functions.get_all_files(output_dir, '.json')
        ignition_json = file_functions.get_dict_from_json_files(json_files)

        # address_csv = file_functions.get_all_files(output_dir, '.csv')
        # address_csv = file_functions.get_dict_of_dfs_from_csv_files(address_csv, pd.read_csv)

        expected_output_json_files = file_functions.get_all_files(expected_output_dir, '.json')
        expected_ignition_json = file_functions.get_dict_from_json_files(expected_output_json_files)

        # expected_output_csv_files = file_functions.get_all_files(expected_output_dir, '.csv')
        # expected_address_csv = file_functions.get_dict_of_dfs_from_csv_files(expected_output_csv_files, pd.read_csv)

        diff = DeepDiff(expected_ignition_json, ignition_json, ignore_order=True, verbose_level=2)
        if diff:
            self.fail(f"JSON files do not match: {diff}")

        # for key, df in address_csv.items():
        #     if key in expected_address_csv:
        #         pd.testing.assert_frame_equal(df, expected_address_csv[key])
        #     else:
        #         self.fail(f"Missing expected CSV for key: {key}")

        