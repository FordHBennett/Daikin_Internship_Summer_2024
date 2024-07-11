import unittest
from tag_generator.base.file_functions import get_basename_without_extension

class Test_Get_Basename_Without_Extension(unittest.TestCase):
        def test_path_with_extension(self):
            file_path = '/path/to/file.txt'
            expected_result = 'file'
            self.assertEqual(get_basename_without_extension(file_path), expected_result)

        def test_path_without_extension(self):
            file_path = '/path/to/file'
            expected_result = 'file'
            self.assertEqual(get_basename_without_extension(file_path), expected_result)

        def test_path_with_multiple_extensions(self):
            # Test with a file path that has multiple extensions
            file_path = '/path/to/file.tar.gz'
            expected_result = 'file.tar'
            self.assertEqual(get_basename_without_extension(file_path), expected_result)

        def test_path_with_no_extension(self):
            # Test with a file path that starts with a dot
            file_path = '/path/to/.hidden_file'
            expected_result = '.hidden_file'
            self.assertEqual(get_basename_without_extension(file_path), expected_result)
