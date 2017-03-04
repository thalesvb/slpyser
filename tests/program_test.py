# -*- coding: utf-8 -*-

import unittest
from context import slpyser, Util

class TestProgram(unittest.TestCase):


    def test_program(self):
        parsed_data = slpyser.parse(Util.file_path("NUGG_SLPUT_PROGRAMS.nugg"))
        programs_names = parsed_data.programs.keys()
        self.assertIn('ZSLPUT_PROGRAM_SIMPLE', programs_names)


if __name__ == '__main__':
    unittest.main()
