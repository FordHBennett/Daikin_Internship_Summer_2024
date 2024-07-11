import unittest
import pytest
from tests.base.file_functions import Test_File_Functions
from tests.base.tag_functions import Test_Tag_Functions
from tests.tag_generator import Test_Mitsubishi_Tag_Generator

def suite():
    suite = unittest.TestSuite()
    # Add tests from each test class
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_File_Functions))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_Tag_Functions))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_Mitsubishi_Tag_Generator))
    return suite

if __name__ == "__main__":
    # run pytest tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

