import unittest
import pandas as pd
from tag_generator.base.tag_functions import find_row_by_tag_name

class Test_Find_Row_By_Tag_Name(unittest.TestCase):
    def test_find_row_by_tag_name_existing_tag(self):
        data = {'Tag Name': ['Tag1', 'Tag2', 'Tag3'],
                'Address': ['Address1', 'Address2', 'Address3'],
                'Data Type': ['Type1', 'Type2', 'Type3']}
        df = pd.DataFrame(data)

        tag_name = 'Tag2'
        expected_result = pd.Series(['Tag2', 'Address2', 'Type2'], index=['Tag Name', 'Address', 'Data Type'])
        result = find_row_by_tag_name(df, tag_name)
        assert result.equals(expected_result)


    def test_find_row_by_tag_name_non_existing_tag(self):
        df = pd.DataFrame({'Tag Name': ['tag1', 'tag2', 'tag3'], 'Value': [1, 2, 3]})
        assert find_row_by_tag_name(df, 'tag4') is None
