import unittest
from unittest.mock import patch, MagicMock
from deepdiff import DeepDiff
from tag_generator.base.file_functions import get_all_files

class Test_Get_All_Files(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_files_found(self, mock_os_walk, mock_isdir):
        # Mock the os.walk to return a specific file structure
        mock_os_walk.return_value = [
            ('/some/dir', ('subdir',), ('file1.txt', 'file2.txt', 'file3.csv')),
            ('/some/dir/subdir', (), ('file4.txt', 'file5.csv')),
        ]
        
        expected_result = (
            '/some/dir/file1.txt',
            '/some/dir/file2.txt',
            '/some/dir/subdir/file4.txt'
        )
        
        # Call the function
        result = get_all_files('/some/dir', '.txt')
        
        # Check the result
        self.assertEqual(DeepDiff(result, expected_result, ignore_order=True), {})

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_no_files_found(self, mock_os_walk, mock_isdir):
        # Mock the os.walk to return an empty directory
        mock_os_walk.return_value = [
            ('/some/dir', ('subdir',), ()),
            ('/some/dir/subdir', (), ()),
        ]
        
        # Call the function and expect a FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            get_all_files('/some/dir', '.txt')

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_files_found_in_subdir(self, mock_os_walk, mock_isdir):
        # Mock the os.walk to return a specific file structure
        mock_os_walk.return_value = [
            ('/some/dir', ('subdir',), ()),
            ('/some/dir/subdir', (), ('file1.txt', 'file2.csv')),
        ]
        
        expected_result = (
            '/some/dir/subdir/file1.txt',
        )
        
        # Call the function
        result = get_all_files('/some/dir', '.txt')
        
        # Check the result
        self.assertEqual(DeepDiff(result, expected_result, ignore_order=True), {})

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_files_with_different_extensions(self, mock_os_walk, mock_isdir):
        # Mock the os.walk to return a specific file structure
        mock_os_walk.return_value = [
            ('/some/dir', ('subdir',), ('file1.txt', 'file2.csv', 'file3.md')),
            ('/some/dir/subdir', (), ('file4.md', 'file5.csv')),
        ]
        
        expected_result = (
            '/some/dir/file3.md',
            '/some/dir/subdir/file4.md',
        )
        
        # Call the function
        result = get_all_files('/some/dir', '.md')
        
        # Check the result
        self.assertEqual(DeepDiff(result, expected_result, ignore_order=True), {})
