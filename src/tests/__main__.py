import unittest
from . import file_functions_tests, tag_functions_tests, mitsubishi_tag_generator_tests

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(file_functions_tests)
    unittest.TextTestRunner(verbosity=2).run(tag_functions_tests)
    unittest.TextTestRunner(verbosity=2).run(mitsubishi_tag_generator_tests)
