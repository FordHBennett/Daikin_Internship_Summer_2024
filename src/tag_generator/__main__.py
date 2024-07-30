# Required Libraries
import tag_generator.base.file_functions as file_functions
import os.path as path
from tag_generator import generate_output_using_all_csv_files

if __name__ == '__main__':
    # Clean the output directory
    file_functions.clean_files_dir()

    # List of manufacturers
    manufacturers:tuple = ('mitsubishi', 'cj')
    
    # Get all the csv file paths in the input directory
    csv_files:tuple = file_functions.get_all_files(path.join('files', 'input'), '.csv')

    # Iterate over all the manufacturers
    for manufacturer in manufacturers:
        # Get the input and output directory paths
        input_dir = path.join('files', 'input', manufacturer)
        output_dir:path = path.join('files', 'output', manufacturer)
       
        # Get all the json files in the input directory
        json_files:tuple = file_functions.get_all_files(input_dir, '.json')
        
        # Iterate over all the json files to generate the output
        for json_file in json_files:
            generate_output_using_all_csv_files(output_dir, csv_files, json_file, manufacturer)


