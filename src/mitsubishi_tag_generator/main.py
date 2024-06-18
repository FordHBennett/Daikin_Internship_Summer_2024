#!/usr/bin/env python

def main():
    from base.base_functions import Get_ALL_CSV_Paths, Get_ALL_JSON_Paths, Read_CSV_Files, Read_Json_Files, Write_Json_Files, Write_Address_CSV
    from mitsubishi_tag_generator.process_tags import Generate_Ignition_JSON_And_Address_CSV
    from os.path import join as os_path_join
    input_dir: str = os_path_join('input_files', 'mitsubishi')
    output_dir: str = os_path_join('output_files', 'mitsubishi')
   
    json_files = Get_ALL_JSON_Paths(input_dir)
    csv_files = Get_ALL_CSV_Paths(input_dir)

    ignition_json = Read_Json_Files(json_files)
    csv_df = Read_CSV_Files(csv_files)

    ignition_json, address_csv = Generate_Ignition_JSON_And_Address_CSV(csv_df, ignition_json)
    Write_Json_Files(ignition_json, output_dir)

    Write_Address_CSV(address_csv, output_dir)

    ignition_json = Read_Json_Files(json_files)
    csv_df = Read_CSV_Files(csv_files)

if __name__ == '__main__':
    main()

