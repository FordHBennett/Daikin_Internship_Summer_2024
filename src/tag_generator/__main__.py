if __name__ == '__main__':
    import tag_generator.base.file_functions as file_functions
    import os.path as path
    import tag_generator.ignition_tag_generator as ignition_tag_generator

    import pandas as pd
    from tag_generator import logger


    file_functions.clean_files_dir()

    input_dir:path = path.join('files', 'input', 'mitsubishi')
    output_dir:path = path.join('files', 'output', 'mitsubishi')
   
    json_files:list = file_functions.get_all_files(input_dir, '.json')
    csv_files:list = file_functions.get_all_files(input_dir, '.csv')


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
    
        ignition_json:dict = file_functions.get_dict_from_json_files(tuple([json_file]),  logger=logger, device=device)
        json_key: str = next(iter(ignition_json.keys()))

        for count, csv_file in enumerate(csv_files, start=1):
            csv_basename = file_functions.get_basename_without_extension(csv_file)

            if csv_basename == json_key:
                ignition_json, address_csv = ignition_tag_generator.get_generated_ignition_json_and_csv_files(
                    file_functions.get_dict_of_dfs_from_csv_files((csv_file,), pd.read_csv),
                    ignition_json,
                    pd.DataFrame,
                    device=device,
                    logger=logger
                )
                
                file_functions.write_json_files(ignition_json, output_dir)
                file_functions.write_csv_files(address_csv, output_dir)
                csv_files.remove(csv_file)
                break
            elif count == len(csv_files):
                # If no match is found, log and raise an error
                error_parts = [f'{json_key} does not match any of the following CSV files: ']
                error_parts.extend(f'{file_functions.get_basename_without_extension(csv_file)}, ' for csv_file in csv_files)
                error_parts.append('\nPlease ensure that the JSON tag name matches one of the CSV file names (without the file extension).')
                error_str = ''.join(error_parts)
                logger.log_message(error_str, device, level='ERROR')

                raise ValueError(error_str)

    list(map(lambda json_file: generate_output(output_dir, csv_files, json_file, 'mitsubishi'), json_files))

    input_dir:path = path.join('files', 'input', 'cj')
    output_dir:path = path.join('files', 'output', 'cj')
   
    json_files:list = file_functions.get_all_files(input_dir, '.json')
    csv_files:list = file_functions.get_all_files(input_dir, '.csv')

    list(map(lambda json_file: generate_output(output_dir, csv_files, json_file, 'cj'), json_files))


