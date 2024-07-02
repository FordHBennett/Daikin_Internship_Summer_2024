# from . import main

if __name__ == '__main__':
    from tag_generator.base.file_functions import remove_output_dir, remove_log_dir, get_all_files
    from os.path import join as os_path_join
    from tag_generator.base.tag_functions import generate_output

    remove_output_dir()
    remove_log_dir()

    input_dir = os_path_join('files', 'input', 'mitsubishi')
    output_dir = os_path_join('files', 'output', 'mitsubishi')
   
    json_files = get_all_files(input_dir, '.json')
    csv_files = get_all_files(input_dir, '.csv')

    for json_file in json_files:
        generate_output(output_dir, csv_files, json_file)