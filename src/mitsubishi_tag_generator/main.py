#!/usr/bin/env python




from base.logging_class import Logger

logger = Logger()

def main():
    from base.file_functions import get_all_json_files, get_all_csv_files, get_dict_from_json_files, get_dict_of_dfs_from_csv_files, write_json_files, write_csv_files
    from mitsubishi_tag_generator.process_tags import get_generated_ignition_json_and_csv_files
    from os.path import join as os_path_join


    input_dir: str = os_path_join('files', 'input', 'mitsubishi')
    output_dir: str = os_path_join('files', 'output', 'mitsubishi')
   

    json_files = get_all_json_files(input_dir)
    csv_files = get_all_csv_files(input_dir)


    #FUTURE PROOF: get_dict_from_json_files will take a single file
    ignition_json = get_dict_from_json_files(json_files, logger=logger)
    csv_df = get_dict_of_dfs_from_csv_files(csv_files)


    ignition_json, address_csv = get_generated_ignition_json_and_csv_files(csv_df, ignition_json)

    write_json_files(ignition_json, output_dir)
    write_csv_files(address_csv, output_dir)
    


if __name__ == '__main__':
    main()
