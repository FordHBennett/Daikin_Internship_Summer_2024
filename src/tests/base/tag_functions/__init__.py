import unittest 
import pandas as pd
from tag_generator.base.tag_functions import *

class Test_Tag_Functions(unittest.TestCase):
    def test_find_row_by_tag_name(self):
        df = pd.DataFrame({'Tag Name': ['tag1', 'tag2', 'tag3'], 'Value': [1, 2, 3]})
        self.assertEqual(find_row_by_tag_name(df, 'tag2').iloc[0], 'tag2')
        self.assertIsNone(find_row_by_tag_name(df, 'tag4'))

    def test_extract_kepware_path(self):
        self.assertEqual(extract_kepware_path("nsu\u003dThingWorx Kepware Server;s\u003dMA_PD1.MA_PD1.TestResult.TestResult_TrendDataFN"), 'TestResult.TestResult_TrendDataFN')

    def test_extract_area_and_offset(self):
        import tag_generator.base.constants as constants
        self.assertEqual(extract_area_and_offset('M0.0',constants), ('M', '0.0'))
        self.assertEqual(extract_area_and_offset('DB1.DBD0',constants), ('DB', '1.DBD0'))