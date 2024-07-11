# import unittest 
# import os.path
# from tag_generator.base.file_functions import *
# from deepdiff import DeepDiff

# class Test_File_Functions(unittest.TestCase):

#     class Test_Get_Basename_Without_Extension(unittest.TestCase):
#         def test_path_with_extension(self):
#             file_path = '/path/to/file.txt'
#             expected_result = 'file'
#             self.assertEqual(get_basename_without_extension(file_path), expected_result)

#         def test_path_without_extension(self):
#             file_path = '/path/to/file'
#             expected_result = 'file'
#             self.assertEqual(get_basename_without_extension(file_path), expected_result)

#         def test_path_with_multiple_extensions(self):
#             # Test with a file path that has multiple extensions
#             file_path = '/path/to/file.tar.gz'
#             expected_result = 'file.tar'
#             self.assertEqual(get_basename_without_extension(file_path), expected_result)

#         def test_path_with_no_extension(self):
#             # Test with a file path that starts with a dot
#             file_path = '/path/to/.hidden_file'
#             expected_result = '.hidden_file'
#             self.assertEqual(get_basename_without_extension(file_path), expected_result)


#     def test_get_all_files(self):
#         dir = os.path.join('src','tests','files','input', 'mitsubishi')
#         extension = '.json'
#         expected_output = (
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'FITBasePanConveyor.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kaishi_Conv_tags.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kansei_Conv_tags.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_HIPOT_tags.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_LT1_tags.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_PD1_tags.json'),
#             os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_RC1_tags.json')
#         )
        
#         output = get_all_files(dir, extension)

#         diff = DeepDiff(expected_output, output, ignore_order=True, verbose_level=2)
#         if diff:
#             self.fail(f"Output does not match expected output: {diff}")


    

#     if __name__ == '__main__':
#         unittest.main()


