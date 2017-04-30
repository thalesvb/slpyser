# -*- coding: utf-8 -*-

import unittest
from tests.context import slpyser, Util

class TestClassLibrary(unittest.TestCase):


    def test_class_library(self):
        parsed_data = slpyser.parse(Util.file_path("NUGG_CLASSLIBRARY_BASIC.nugg"))


if __name__ == '__main__':
    unittest.main()
