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
        file_path = '/path/to/file.tar.gz'
        expected_result = 'file.tar'
        self.assertEqual(get_basename_without_extension(file_path), expected_result)

    def test_hidden_file(self):
        file_path = '/path/to/.hidden_file'
        expected_result = '.hidden_file'
        self.assertEqual(get_basename_without_extension(file_path), expected_result)

    def test_edge_case_empty_string(self):
        file_path = ''
        expected_result = ''
        self.assertEqual(get_basename_without_extension(file_path), expected_result)

    def test_edge_case_root_path(self):
        file_path = '/'
        expected_result = ''
        self.assertEqual(get_basename_without_extension(file_path), expected_result)
        
    # def test_edge_case_non_string_input(self):
    #     with self.assertRaises(TypeError):
    #         get_basename_without_extension(None)
