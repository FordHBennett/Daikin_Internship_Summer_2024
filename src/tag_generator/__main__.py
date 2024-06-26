#!/usr/bin/env python

import gc

from matplotlib.artist import get
# from memory_profiler import profile
from tag_generator.base.logging_class import Logger
# import tracemalloc

from guppy import hpy
h = hpy()

logger = Logger()

# @profile
def main():
    from tag_generator.base.file_functions import get_all_files
    from os.path import join as os_path_join
    # tracemalloc.start()
    input_dir = os_path_join('files', 'input', 'mitsubishi').encode('unicode-escape').decode()
    output_dir = os_path_join('files', 'output', 'mitsubishi').encode('unicode-escape').decode()
   

    json_files = get_all_files(input_dir, '.json')
    csv_files = get_all_files(input_dir, '.csv')

    # gc.collect()
    #FUTURE PROOF: get_dict_from_json_files will take a single file
    # csv_df = get_dict_of_dfs_from_csv_files(csv_files)
    # process_files(output_dir, json_files, csv_df)

    for json_file in json_files:
        generate_output(output_dir, csv_files, json_file)

    


        
# @profile
def process_files(output_dir, json_files, csv_df):
    from tag_generator.base.file_functions import get_dict_from_json_files, write_json_files, write_csv_files
    from tag_generator.mitsubishi_tag_generator.process_tags import get_generated_ignition_json_and_csv_files

    ignition_json = get_dict_from_json_files(json_files, logger=logger)
    ignition_json, address_csv = get_generated_ignition_json_and_csv_files(csv_df, ignition_json)

    write_json_files(ignition_json, output_dir)
    write_csv_files(address_csv, output_dir)


# @profile
def generate_output(output_dir, csv_files, json_file):
    from tag_generator.base.file_functions import get_dict_from_json_files, get_basename_without_extension
    ignition_json = get_dict_from_json_files(tuple([json_file]), logger=logger)
    for csv_file in csv_files:
        if get_basename_without_extension(csv_file) in ignition_json.keys():
            from tag_generator.base.file_functions import get_dict_of_dfs_from_csv_files, write_json_files, write_csv_files
            from tag_generator.mitsubishi_tag_generator.process_tags import get_generated_ignition_json_and_csv_files
            
            ignition_json, address_csv = get_generated_ignition_json_and_csv_files(get_dict_of_dfs_from_csv_files(tuple([csv_file])) , ignition_json)
            write_json_files(ignition_json, output_dir)
            write_csv_files(address_csv, output_dir)

            break


    



if __name__ == '__main__':
    # import cProfile
    gc.enable()
    # cProfile.run('main()', 'profile_stats')
    main()

