import unittest
from tag_generator.base.tag_functions import extract_area_and_offset
import tag_generator.base.constants as constants

class Test_Extract_Area_And_Offset(unittest.TestCase):
    def test_extract_area_and_offset_memory(self):
        assert extract_area_and_offset('M0.0', constants.ADDRESS_PATTERN) == ('M', '0.0')

    def test_extract_area_and_offset_db(self):
        assert extract_area_and_offset('DB1.DBD0', constants.ADDRESS_PATTERN) == ('DB', '1.DBD0')

    def test_basic_address(self):
        address = 'M0.0'
        expected_result = ('M', '0.0')
        self.assertEqual(extract_area_and_offset(address, constants.ADDRESS_PATTERN), expected_result)

    def test_address_with_db(self):
        address = 'DB1.DBD0'
        expected_result = ('DB', '1.DBD0')
        self.assertEqual(extract_area_and_offset(address, constants.ADDRESS_PATTERN), expected_result)


    def test_address_with_leading_zero_offset(self):
        address = 'DB001.DBD002'
        expected_result = ('DB', '1.DBD002')
        self.assertEqual(extract_area_and_offset(address, constants.ADDRESS_PATTERN), expected_result)

    def test_address_without_numbers(self):
        address = 'ABCDEF'
        with self.assertRaises(Exception):
            extract_area_and_offset(address, constants.ADDRESS_PATTERN)

    def test_address_with_zero(self):
        address = 'DB0.DBD0'
        expected_result = ('DB', '0.DBD0')
        self.assertEqual(extract_area_and_offset(address, constants.ADDRESS_PATTERN), expected_result)

    def test_address_with_dot_offset(self):
        address = 'DB1.DBD.123'
        expected_result = ('DB', '1.DBD.123')
        self.assertEqual(extract_area_and_offset(address, constants.ADDRESS_PATTERN), expected_result)

