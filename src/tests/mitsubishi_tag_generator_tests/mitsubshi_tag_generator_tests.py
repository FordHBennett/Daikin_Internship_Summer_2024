from math import e
import shutil
import unittest 
from mitsubishi_tag_generator.process_tags import *
from base.base_functions import *
import os

class Test_Mitsubishi_Tag_Generator(unittest.TestCase):

    def test_convert_data_type_short_int2_word(self):

        data_type = 'Short'
        expected_data_type = ('Int2', 'Int16')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

        data_type = 'Int2'
        expected_data_type = ('Int2', 'Int16')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

        data_type = 'Word'
        expected_data_type = ('Int2', 'Int16')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

    def test_convert_data_type_integer_int4_bcd(self):
             
        data_type = 'Integer'
        expected_data_type = ('Int4', 'Int32')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

        data_type = 'Int4'
        expected_data_type = ('Int4', 'Int32')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

        data_type = 'BCD'
        expected_data_type = ('Int4', 'Int32')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

    def test_convert_data_type_boolean(self):   
             
        data_type = 'Boolean'
        expected_data_type = ('Boolean', 'Bool')
        self.assertEqual(Convert_Data_Type(data_type), expected_data_type)

    def test_update_area_and_path_data_type_without_sh_in_area(self):
        area = 'RTY'
        data_type = 'Short'
        expected_area = 'RTY'
        expected_data_type = 'Short'

        self.assertEqual(Update_Area_And_Path_Data_Type(area, data_type), (expected_area, expected_data_type))

    def test_update_area_and_path_data_type_with_sh_in_area(self):
        area = 'TWSHqer'
        data_type = 'Short'
        expected_area = 'TWqer'
        expected_data_type = 'String'

        self.assertEqual(Update_Area_And_Path_Data_Type(area, data_type), (expected_area, expected_data_type))

    def test_update_area_and_path_data_type_with_no_area_and_path_data_type(self):
        area = ''
        data_type = ''
        expected_area = ''
        expected_data_type = ''

        self.assertEqual(Update_Area_And_Path_Data_Type(area, data_type), (expected_area, expected_data_type))


    def test_modify_tags_for_direct_driver_communication(self):
        input_dir: str = os.path.join('src','tests','test_files','input_files', 'mitsubishi_devices')
        output_dir: str = os.path.join('src','tests','test_files','output_files', 'mitsubishi_devices')
        expected_output_dir: str = os.path.join('src','tests','test_files','expected_output_files', 'mitsubishi_devices')
    
        json_files = Get_ALL_JSON_Paths(input_dir)
        csv_files = Get_ALL_CSV_Paths(input_dir)

        ignition_json = Read_Json_Files(json_files)
        csv_df = Read_CSV_Files(csv_files)

        ignition_json, address_csv = Modify_Tags_For_Direct_Driver_Communication(csv_df, ignition_json)
        Write_Json_Files(ignition_json, output_dir)
        Write_Address_CSV(address_csv, output_dir)

        expected_output_json_files = Get_ALL_JSON_Paths(expected_output_dir)
        expected_ignition_json = Read_Json_Files(expected_output_json_files)

        expected_output_csv_files = Get_ALL_CSV_Paths(expected_output_dir)
        expected_address_csv = Read_CSV_Files(expected_output_csv_files)

        if self.assertEqual(ignition_json, expected_ignition_json) == None:
            shutil.rmtree(output_dir)

        # Find a way to assert dataframes


        
        
        


if __name__ == '__main__':
    unittest.main()