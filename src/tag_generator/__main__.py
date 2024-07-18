import tag_generator.base.file_functions as file_functions
import os.path as path
from tag_generator import generate_output, generate_output_using_all_csv_files

if __name__ == '__main__':


    file_functions.clean_files_dir()

    manufacturer:tuple = ('mitsubishi', 'cj')
    csv_files:tuple = file_functions.get_all_files(path.join('files', 'input'), '.csv')
    for brand in manufacturer:
        input_dir = path.join('files', 'input', brand)
        output_dir:path = path.join('files', 'output', brand)
       
        json_files:tuple = file_functions.get_all_files(input_dir, '.json')
        

        # tuple(
        #     map(
        #         lambda json_file: 
        #             generate_output(
        #                 output_dir, 
        #                 csv_files, 
        #                 json_file, 
        #                 brand
        #             ), 
        #         json_files
        #     )
        # )
        for json_file in json_files:
            generate_output_using_all_csv_files(output_dir, csv_files, json_file, brand)


