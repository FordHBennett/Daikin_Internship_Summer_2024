from math import e
import unittest 
from mitsubishi_tag_generator.process_tags import *
from base.base_functions import *
import os

class Test_Mitsubishi_Tag_Generator(unittest.TestCase):


    def test_extract_area_offset(self):
        test_tag_builder_properties = {
            "address": 'WER00000123456.0002345',
            "area": '',
            "offset": ''
        }

        Extract_Area_Offset(test_tag_builder_properties)


        try:
            self.assertEqual(test_tag_builder_properties['area'], 'WER')
        
            self.assertEqual(test_tag_builder_properties['offset'], '123456.0002345')
        except AssertionError as e:
            print(f'Error: {e}')
            print(f'Expected Area: WER')
            print(f'Expected Offset: 123456.0002345')
            print(f'Actual Area: {test_tag_builder_properties["area"]}')
            print(f'Actual Offset: {test_tag_builder_properties["offset"]}')
    
    def test_convert_area_to_mitsubishi_format(self):

        test_tag_builder_properties = {
            "address": 'WSH00000123456.0002345',
            "area": 'WSH',
            "offset": '123456.0002345',
            "array_size": ''
        }

        Convert_Tag_Builder_Properties_To_Mitsubishi_Format(test_tag_builder_properties)

        try:
            self.assertEqual(test_tag_builder_properties['area'], 'W')

            self.assertEqual(test_tag_builder_properties['offset'], '123456')

            self.assertEqual(test_tag_builder_properties['array_size'], '2345')
        except AssertionError as e:
            print(f'Error: {e}')
            print(f'Expected Area: W')
            print(f'Expected Offset: 123456')
            print(f'Expected Array Size: 2345')
            print(f'Actual Area: {test_tag_builder_properties["area"]}')
            print(f'Actual Offset: {test_tag_builder_properties["offset"]}')
            print(f'Actual Array Size: {test_tag_builder_properties["array_size"]}')


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

        # check if the contents of the output_files are the same as the expected_output_files
        output_files = Get_ALL_JSON_Paths(output_dir)
        expected_output_files = Get_ALL_JSON_Paths(expected_output_dir)

        output_json = Read_Json_Files(output_files)
        expected_output_json = Read_Json_Files(expected_output_files)

        self.assertEqual(output_json, expected_output_json)
        
        
        


if __name__ == '__main__':
    unittest.main()