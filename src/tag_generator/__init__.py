#!/usr/bin/env python

from tag_generator.base.logging_class import Logger

logger = Logger()

def main():
    from tag_generator.base.file_functions import remove_output_dir, remove_log_dir, get_all_files
    from os.path import join as os_path_join

    remove_output_dir()
    remove_log_dir()

    input_dir = os_path_join('files', 'input', 'mitsubishi')
    output_dir = os_path_join('files', 'output', 'mitsubishi')
   
    json_files = get_all_files(input_dir, '.json')
    csv_files = get_all_files(input_dir, '.csv')

    for json_file in json_files:
        generate_output(output_dir, csv_files, json_file)


def process_files(output_dir, json_files, csv_df):
    """
    Process the JSON and CSV files to generate ignition JSON and CSV files.

    Args:
        output_dir (str): The directory where the generated files will be saved.
        json_files (list): A list of JSON file paths.
        csv_df (pandas.DataFrame): The CSV data.

    Returns:
        None
    """
    from tag_generator.base import file_functions
    from tag_generator.mitsubishi_tag_generator import get_generated_ignition_json_and_csv_files

    ignition_json = file_functions.get_dict_from_json_files(json_files, logger=logger)
    ignition_json, address_csv = get_generated_ignition_json_and_csv_files(csv_df, ignition_json)

    file_functions.write_json_files(ignition_json, output_dir)
    file_functions.write_csv_files(address_csv, output_dir)


def generate_output(output_dir, csv_files, json_file):
    """
    Process the JSON and CSV files to generate ignition JSON and CSV files.

    Args:
        output_dir (str): The directory where the output files will be saved.
        csv_files (list): A list of CSV file paths.
        json_file (str): The path to the JSON file.

    Returns:
        None
    """
    from tag_generator.base.file_functions import get_dict_from_json_files, get_basename_without_extension
    ignition_json = get_dict_from_json_files(tuple([json_file]), logger=logger)
    for csv_file in csv_files:
        if get_basename_without_extension(csv_file) in ignition_json.keys():
            from tag_generator.base.file_functions import get_dict_of_dfs_from_csv_files, write_json_files, write_csv_files
            from tag_generator.mitsubishi_tag_generator import get_generated_ignition_json_and_csv_files
            
            ignition_json, address_csv = get_generated_ignition_json_and_csv_files(get_dict_of_dfs_from_csv_files(tuple([csv_file])) , ignition_json)
            write_json_files(ignition_json, output_dir)
            write_csv_files(address_csv, output_dir)
            break


    

# main()