from math import e
import unittest 
from mitsubishi_tag_generator.process_tags import *
from base.base_functions import *
import os

class Test_Mitsubishi_Tag_Generator(unittest.TestCase):


    def test_extract_tag_name(self):

        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.PLC_PHS_Heartbeat'
        expected_tag_name = 'PLC_PHS_Heartbeat'
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

    def test_extract_tag_name_with_no_tag_name(self):

        tag_name = 'A_KanseiConveyor.MA_KanseiConveyor.'
        expected_tag_name = ''
        self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

    def test_extract_tag_name_with_no_tag_name_and_no_period(self):
            
            tag_name = 'A_KanseiConveyorMA_KanseiConveyor'
            expected_tag_name = 'A_KanseiConveyorMA_KanseiConveyor'
            self.assertEqual(Extract_Tag_Name(tag_name), expected_tag_name)

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

    
    def test_extract_area_and_offset(self):
        address = 'RTY000023456.000000987456789'
        expected_area = 'RTY'
        expected_offset = '23456.000000987456789'

        self.assertEqual(Extract_Area_And_Offset(address), (expected_area, expected_offset))

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

    def test_extract_offset_and_array_size(self):
        offset = '23456.000000987456789'
        expected_offset = '23456'
        expected_array_size = '987456789'

        self.assertEqual(Extract_Offset_And_Array_Size(offset), (expected_offset, expected_array_size))


    def test_modify_tags_for_direct_driver_communication(self):

        input_dir: str = os.path.join('src','tests','test_files','input_files', 'mitsubishi_devices')
        output_dir: str = os.path.join('src','tests','test_files','output_files', 'mitsubishi_devices')
        expected_output_dir: str = os.path.join('src','tests','test_files','expected_output_files', 'mitsubishi_devices')
    
        json_files = Get_ALL_JSON_Paths(input_dir)
        csv_files = Get_ALL_CSV_Paths(input_dir)

        ignition_json = Read_Json_Files(json_files)
        csv_df = Read_CSV_Files(csv_files)

        ignition_json = Modify_Tags_For_Direct_Driver_Communication(csv_df, ignition_json)
        Write_Json_Files(ignition_json, output_dir)

        
        
        


if __name__ == '__main__':
    unittest.main()