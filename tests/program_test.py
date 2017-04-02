# -*- coding: utf-8 -*-

import unittest
from tests.context import slpyser, Util

class TestProgram(unittest.TestCase):


    def test_simple_program(self):
        SIMPLE_PROGRAM_NAME = 'ZSLPUT_PROGRAM_SIMPLE'
        parsed_data = slpyser.parse(Util.file_path("NUGG_SLPUT_PROGRAMS.nugg"))
        programs = parsed_data.programs
        programs_names = programs.keys()
        # The program should exists in the parsed list.
        self.assertIn(SIMPLE_PROGRAM_NAME, programs_names)
        
        simple_program = programs.get(SIMPLE_PROGRAM_NAME)
        # Some source code should exists in the program.
        self.assertGreater(len(simple_program.source_code.source_code), 0)
        # At least one text pool language should exists for a program.
        self.assertGreater(len(simple_program.text_pool.language_mapping), 0)


if __name__ == '__main__':
    unittest.main()
