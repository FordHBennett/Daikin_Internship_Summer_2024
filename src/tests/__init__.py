from tests.base.file_functions import Test_File_Functions
from tests.base.tag_functions import Test_Tag_Functions
from tests.ignition_tag_generator import Test_Mitsubishi_Tag_Generator
import unittest

file_functions_tests = unittest.TestLoader().loadTestsFromTestCase(Test_File_Functions)
tag_functions_tests = unittest.TestLoader().loadTestsFromTestCase(Test_Tag_Functions)
mitsubishi_tag_generator_tests = unittest.TestLoader().loadTestsFromTestCase(Test_Mitsubishi_Tag_Generator)



