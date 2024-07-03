# from . import main

if __name__ == '__main__':
    import tag_generator.base.file_functions as file_functions
    import os


    file_functions.remove_output_dir(os.path)
    file_functions.remove_log_dir(os.path)

    input_dir = os.path.join('files', 'input', 'mitsubishi')
    output_dir = os.path.join('files', 'output', 'mitsubishi')
   
    json_files = file_functions.get_all_files(input_dir, '.json', os)
    csv_files = file_functions.get_all_files(input_dir, '.csv', os)

    def generate_output(output_dir, csv_files, json_file) -> None:
        """
        Process the JSON and CSV files to generate ignition JSON and CSV files.

        Args:
            output_dir (str): The directory where the output files will be saved.
            csv_files (list): A list of CSV file paths.
            json_file (str): The path to the JSON file.

        Returns:
            None
        """
        import tag_generator.mitsubishi_tag_generator as mitsubishi_tag_generator
        import pandas as pd
        from tag_generator import logger
        import json

        ignition_json = file_functions.get_dict_from_json_files(tuple([json_file]), os.path, json,  logger=logger)
        for csv_file in csv_files:
            if file_functions.get_basename_without_extension(csv_file, os.path) in ignition_json.keys():
                ignition_json, address_csv = mitsubishi_tag_generator.get_generated_ignition_json_and_csv_files(
                    file_functions.get_dict_of_dfs_from_csv_files(tuple([csv_file]), os, pd),
                    ignition_json,
                    pd,
                    os.path,
                    logger=logger
                )
                file_functions.write_json_files(ignition_json, output_dir, os, json)
                file_functions.write_csv_files(address_csv, output_dir, os)
                break


    for json_file in json_files:
        generate_output(output_dir, csv_files, json_file)


