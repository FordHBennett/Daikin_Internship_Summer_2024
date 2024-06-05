#!bin/python3

from mitsubishi_tag_generator.base import *
from mitsubishi_tag_generator.process_tags import *
import os
from typing import List

def main():
    input_dir: str = 'input_files'
    dir_list: List[str] = os.listdir(input_dir)
    for dir in dir_list:
        if not dir.startswith('.'):      
            current_dir = os.path.join(input_dir, dir)
            json_files = Get_ALL_JSON_Paths(current_dir)
            csv_files = Get_ALL_CSV_Paths(current_dir)

            ignition_json = Read_Json_Files(json_files)
            csv_df = Read_CSV_Files(csv_files)

            ignition_json = Modify_Tags_For_Direct_Driver_Communication(csv_df, ignition_json)
            Write_Json_Files(ignition_json, dir)

            address_csv = Generate_Address_CSV(csv_df, ignition_json)
            Write_Address_CSV(address_csv, current_dir)

if __name__ == '__main__':
    main()
