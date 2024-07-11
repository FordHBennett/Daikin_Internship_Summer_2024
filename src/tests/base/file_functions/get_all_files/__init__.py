import unittest
from tag_generator.base.file_functions import get_all_files
import os
from deepdiff import DeepDiff

class Test_Get_All_Files(unittest.TestCase):
    def test_get_all_files(self):
        dir = os.path.join('src','tests','files','input', 'mitsubishi')
        extension = '.json'
        expected_output = (
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'FITBasePanConveyor.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kaishi_Conv_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kansei_Conv_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_HIPOT_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_LT1_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_PD1_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_RC1_tags.json')
        )
        
        output = get_all_files(dir, extension)

        diff = DeepDiff(expected_output, output, ignore_order=True, verbose_level=2)
        if diff:
            self.fail(f"Output does not match expected output: {diff}")