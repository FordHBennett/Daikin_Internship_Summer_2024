import unittest
from tag_generator.base.tag_functions import get_offset_and_array_size

class Test_Get_Offset_And_Array_Size(unittest.TestCase):
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