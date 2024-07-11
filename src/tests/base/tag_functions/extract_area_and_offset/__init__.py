import unittest
from tag_generator.base.tag_functions import extract_area_and_offset
import tag_generator.base.constants as constants

class Test_Extract_Area_And_Offset(unittest.TestCase):
    def test_extract_area_and_offset_memory(self):
        assert extract_area_and_offset('M0.0', constants.ADDRESS_PATTERN) == ('M', '0.0')

    def test_extract_area_and_offset_db(self):
        assert extract_area_and_offset('DB1.DBD0', constants.ADDRESS_PATTERN) == ('DB', '1.DBD0')
