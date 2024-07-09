import unittest 
import os
from tag_generator import *
import tag_generator.base.file_functions as file_functions
from tag_generator.base.tag_functions import *
import tag_generator.ignition_tag_generator as ignition_tag_generator
import pandas as pd
from deepdiff import DeepDiff



class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_get_generated_ignition_json_and_csv_files(self):
        file_functions.clean_files_dir()

        
        input_dir: str = os.path.join('src','tests','files','input', 'mitsubishi')
        output_dir: str = os.path.join('src','tests','files','output', 'mitsubishi')
        expected_output_dir: str = os.path.join('src','tests','files','expected_output', 'mitsubishi')
    
        json_files = file_functions.get_all_files(input_dir, '.json')
        csv_files = file_functions.get_all_files(input_dir, '.csv')

        logger = Logger()

            
        def generate_output(output_dir, csv_files, json_file, device) -> None:
            """
            Process the JSON and CSV files to generate ignition JSON and CSV files.

            Args:
                output_dir (str): The directory where the output files will be saved.
                csv_files (list): A list of CSV file paths.
                json_file (str): The path to the JSON file.

            Returns:
                None
            """
        
            ignition_json:dict = file_functions.get_dict_from_json_files(tuple([json_file]))

            for csv_file in csv_files:
                csv_basename = file_functions.get_basename_without_extension(csv_file)
                found_device_name_flag = False
                def get_device_name(tags, csv_basename, csv_file, ignition_json, device, logger):
                    nonlocal found_device_name_flag
                    if found_device_name_flag:
                        return
                    for tag in tags:
                        if 'opcItemPath' in tag:
                            opc_path = tag['opcItemPath']
                            if csv_basename in opc_path:
                                device_name = opc_path.split('.')[1]

                                csv_dict = file_functions.get_dict_of_dfs_from_csv_files((csv_file,), pd.read_csv)
                                ignition_old_key = next(iter(ignition_json))
                                ignition_json[device_name] = ignition_json.pop(ignition_old_key)

                                ignition_json, address_csv = ignition_tag_generator.get_generated_ignition_json_and_csv_files(
                                    csv_dict,
                                    ignition_json,
                                    pd.DataFrame,
                                    device=device,
                                    logger=logger
                                )

                                ignition_json[ignition_old_key] = ignition_json.pop(device_name)
                                file_functions.write_json_files(ignition_json, output_dir)
                                file_functions.write_csv_files(address_csv, output_dir)
                                found_device_name_flag = True
                                return
                        elif 'tags' in tag:
                            if found_device_name_flag:
                                return
                            get_device_name(tag['tags'], csv_basename, csv_file, ignition_json, device, logger)
                
                dummy_json = next(iter(ignition_json.values()))
                get_device_name(dummy_json['tags'], csv_basename, csv_file, ignition_json, device, logger)
                if found_device_name_flag:
                    return



        list(map(lambda json_file: generate_output(output_dir, csv_files, json_file, 'mitsubishi'), json_files))


                
        # for json_file in json_files:
        #     generate_output(output_dir, csv_files, json_file, 'mitsubishi')

        json_files = file_functions.get_all_files(output_dir, '.json')
        ignition_json = file_functions.get_dict_from_json_files(json_files)

        address_csv = file_functions.get_all_files(output_dir, '.csv')
        address_csv = file_functions.get_dict_of_dfs_from_csv_files(address_csv, pd.read_csv)

        expected_output_json_files = file_functions.get_all_files(expected_output_dir, '.json')
        expected_ignition_json = file_functions.get_dict_from_json_files(expected_output_json_files)

        expected_output_csv_files = file_functions.get_all_files(expected_output_dir, '.csv')
        expected_address_csv = file_functions.get_dict_of_dfs_from_csv_files(expected_output_csv_files, pd.read_csv)

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