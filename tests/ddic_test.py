# -*- coding: utf-8 -*-

import unittest
from context import slpyser, Util

class TestDDIC(unittest.TestCase):


    def test_ddic(self):
        parsed_data = slpyser.parse(Util.file_path("NUGG_SLPUT_DDIC_BASIC.nugg"))

        # Assert class library contents
        class_lib_keys = parsed_data.classes.keys()
        self.assertIn('ZSLPUT_CL_CLASS', class_lib_keys)
        self.assertIn('ZSLPUT_IF_INTERFACE', class_lib_keys)

if __name__ == '__main__':
    unittest.main()