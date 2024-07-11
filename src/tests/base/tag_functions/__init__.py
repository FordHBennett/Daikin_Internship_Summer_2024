import unittest 
import pandas as pd
from tag_generator.base.tag_functions import *
import tag_generator.base.constants as constants

class Test_Tag_Functions(unittest.TestCase):
    def test_find_row_by_tag_name_existing_tag(self):
        data = {'Tag Name': ['Tag1', 'Tag2', 'Tag3'],
                'Address': ['Address1', 'Address2', 'Address3'],
                'Data Type': ['Type1', 'Type2', 'Type3']}
        df = pd.DataFrame(data)

        # Test case for finding an existing tag name
        tag_name = 'Tag2'
        expected_result = pd.Series(['Tag2', 'Address2', 'Type2'], index=['Tag Name', 'Address', 'Data Type'])
        result = find_row_by_tag_name(df, tag_name)
        assert result.equals(expected_result)


    def test_find_row_by_tag_name_non_existing_tag(self):
        df = pd.DataFrame({'Tag Name': ['tag1', 'tag2', 'tag3'], 'Value': [1, 2, 3]})
        assert find_row_by_tag_name(df, 'tag4') is None

    def test_extract_kepware_path_valid(self):
        assert extract_kepware_path("nsu\u003dThingWorx Kepware Server;s\u003dMA_PD1.MA_PD1.TestResult.TestResult_TrendDataFN") == 'TestResult.TestResult_TrendDataFN'

    def test_extract_area_and_offset_memory(self):
        assert extract_area_and_offset('M0.0', constants.ADDRESS_PATTERN) == ('M', '0.0')

    def test_extract_area_and_offset_db(self):
        assert extract_area_and_offset('DB1.DBD0', constants.ADDRESS_PATTERN) == ('DB', '1.DBD0')

    def test_get_offset_and_array_size_no_array_size(self):
        offset = '123'
        expected_result = ('123', '')
        assert get_offset_and_array_size(offset) == expected_result

    def test_get_offset_and_array_size_with_array_size(self):
        offset = '456.789'
        expected_result = ('456', '789')
        assert get_offset_and_array_size(offset) == expected_result

    def test_get_offset_and_array_size_leading_zeros(self):
        offset = '001.002'
        expected_result = ('1', '2')
        assert get_offset_and_array_size(offset) == expected_result

    def test_get_offset_and_array_size_no_array_size_trailing_zeros(self):
        offset = '123.000'
        expected_result = ('123', '0')
        assert get_offset_and_array_size(offset) == expected_result

    def test_get_offset_and_array_size_no_array_size_leading_trailing_zeros(self):
        offset = '001.000'
        expected_result = ('1', '0')
        assert get_offset_and_array_size(offset) == expected_result
