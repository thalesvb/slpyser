# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import slpyser

class Util:

    __C_DIR_TESTS = "tests"
    __C_DIR_TEST_DATA = "test_data"
    __calculated_dir_test_data = None

    @staticmethod
    def __dir_test_data():
        """
        Identify test data directory.
        """
        if Util.__calculated_dir_test_data is None:
            if (os.path.basename(os.path.abspath(os.path.curdir))) == Util.__C_DIR_TESTS:
                Util.__calculated_dir_test_data = Util.__C_DIR_TEST_DATA
            else:
                Util.__calculated_dir_test_data = os.path.join(Util.__C_DIR_TESTS,
                                                               Util.__C_DIR_TEST_DATA)
        return Util.__calculated_dir_test_data

    @staticmethod
    def file_path(file_name):
        return os.path.abspath(os.path.join(Util.__dir_test_data(), file_name))
