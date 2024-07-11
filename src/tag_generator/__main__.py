import tag_generator.base.file_functions as file_functions
import os.path as path
from tag_generator import generate_output

if __name__ == '__main__':


    file_functions.clean_files_dir()

    manufacturer:tuple = ('mitsubishi', 'cj')

    for brand in manufacturer:
        input_dir = path.join('files', 'input', brand)
        output_dir:path = path.join('files', 'output', brand)
       
        json_files:tuple = file_functions.get_all_files(input_dir, '.json')
        csv_files:tuple = file_functions.get_all_files(input_dir, '.csv')

        tuple(
            map(
                lambda json_file: 
                    generate_output(
                        output_dir, 
                        csv_files, 
                        json_file, 
                        brand
                    ), 
                json_files
            )
        )


