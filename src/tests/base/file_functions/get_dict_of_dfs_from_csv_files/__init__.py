import unittest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock

from tag_generator.base.file_functions import get_dict_of_dfs_from_csv_files

class Test_Get_Dict_Of_Dfs_From_Csv_Files(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('pandas.read_csv')
    def test_single_csv_file(self, mock_read_csv, mock_file):
        # Mock the CSV content
        mock_read_csv.return_value = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

        # Call the function
        result = get_dict_of_dfs_from_csv_files(('file1.csv',), pd.read_csv)

        # Check the result
        self.assertIn('file1', result)
        pd.testing.assert_frame_equal(result['file1'], pd.DataFrame({'A': [1, 2], 'B': [3, 4]}))