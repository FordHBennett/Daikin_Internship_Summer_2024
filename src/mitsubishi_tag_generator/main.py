#!/usr/bin/env python




from base.logging_class import Logger

logger = Logger()

def main():
    from base.file_functions import Get_ALL_JSON_Paths, Get_ALL_CSV_Paths, Read_Json_Files, Read_CSV_Files, Write_Json_Files, Write_Address_CSV
    from mitsubishi_tag_generator.process_tags import Generate_Ignition_JSON_And_Address_CSV
    from os.path import join as os_path_join


    input_dir: str = os_path_join('files', 'input', 'mitsubishi')
    output_dir: str = os_path_join('files', 'output', 'mitsubishi')
   

    json_files = Get_ALL_JSON_Paths(input_dir)
    csv_files = Get_ALL_CSV_Paths(input_dir)


    #FUTURE PROOF: Read_Json_Files will take a single file
    ignition_json = Read_Json_Files(json_files, logger=logger)
    csv_df = Read_CSV_Files(csv_files)


    ignition_json, address_csv = Generate_Ignition_JSON_And_Address_CSV(csv_df, ignition_json)

    Write_Json_Files(ignition_json, output_dir)
    Write_Address_CSV(address_csv, output_dir)
    


if __name__ == '__main__':
    main()
