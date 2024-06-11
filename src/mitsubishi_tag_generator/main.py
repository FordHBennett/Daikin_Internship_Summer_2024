#!/usr/bin/env python

from base.base_functions import *
from mitsubishi_tag_generator.process_tags import *
import os
from typing import List

def main():
    input_dir: str = os.path.join('input_files', 'mitsubishi_devices')
    output_dir: str = os.path.join('output_files', 'mitsubishi_devices')
   
    json_files = Get_ALL_JSON_Paths(input_dir)
    csv_files = Get_ALL_CSV_Paths(input_dir)

    ignition_json = Read_Json_Files(json_files)
    csv_df = Read_CSV_Files(csv_files)

    ignition_json = Modify_Tags_For_Direct_Driver_Communication(csv_df, ignition_json)
    Write_Json_Files(ignition_json, output_dir)

    address_csv = Generate_Address_CSV(csv_df, ignition_json)
    Write_Address_CSV(address_csv, output_dir)

if __name__ == '__main__':
    main()
