#!/usr/bin/env python
import tag_generator.ignition_tag_generator as ignition_tag_generator
import tag_generator.base.file_functions as file_functions
import pandas as pd
from tag_generator.base.logging_class import Logger
logger = Logger()

def generate_output(output_dir:str, csv_files:tuple, json_file:str, device:str) -> None:
    """
    Generate output files based on the provided inputs.

    Args:
        output_dir (str): The directory where the output files will be saved.
        csv_files (tuple): A tuple of CSV file paths.
        json_file (str): The path to the JSON file.
        device (str): The device name.

    Returns:
        None
    """
    ignition_json:dict = file_functions.get_dict_from_json_files((json_file,))

    for csv_file in csv_files:
        csv_basename = file_functions.get_basename_without_extension(csv_file)
        found_device_name_flag = False
        def get_device_name(tags, csv_basename, csv_file, ignition_json, device, logger):
            nonlocal found_device_name_flag
            if found_device_name_flag:
                return
            for tag in tags:
                if 'opcItemPath' in tag:
                    if csv_basename in tag['opcItemPath']:
                        device_name = tag['opcItemPath'].split('.')[1]

                        csv_dict = file_functions.get_dict_of_dfs_from_csv_files((csv_file,), pd.read_csv)
                        ignition_old_key, = ignition_json.keys()
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
        
        dummy_json = tuple(ignition_json.values())[0]
        get_device_name(dummy_json['tags'], csv_basename, csv_file, ignition_json, device, logger)
        if found_device_name_flag:
            return


def generate_output_using_all_csv_files(output_dir:str, csv_files:tuple, json_file:str, device:str) -> None:
    """
    Generate output files based on the provided inputs.

    Args:
        output_dir (str): The directory where the output files will be saved.
        csv_files (tuple): A tuple of CSV file paths.
        json_file (str): The path to the JSON file.
        device (str): The device name.

    Returns:
        None
    """
    ignition_json:dict = file_functions.get_dict_from_json_files((json_file,))

    ignition_json, address_csv = ignition_tag_generator.generate_files(
        csv_files,
        ignition_json,
        device=device,
        logger=logger
    )

    file_functions.write_json_files(ignition_json, output_dir)
    file_functions.write_csv_files(address_csv, output_dir)


    # file_functions.write_csv_files(address_csv, output_dir)
