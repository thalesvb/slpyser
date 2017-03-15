# -*- coding: utf-8 -*-

import unittest
from context import slpyser, Util

class TestDDIC(unittest.TestCase):


    def test_ddic(self):
        parsed_data = slpyser.parse(Util.file_path("NUGG_SLPUT_DDIC_BASIC.nugg"))

        # Assert DDIC contents
        ddic = parsed_data.data_dictionary
        domains = ddic.domains
        self.assertIn('ZSLPUT_DOMAIN', domains)
        data_elements_keys = ddic.data_elements.keys()
        for data_element in ('ZSLPUT_DATAELEMENT_DOMAIN',
                             'ZSLPUT_DATAELEMENT_PREDEFINED',
                             'ZSLPUT_DATAELEMENT_REFOBJECT',
                             'ZSLPUT_DATAELEMENT_REFTYPE'):
            self.assertIn(data_element, data_elements_keys)
        
        structures = ddic.structures
        self.assertIn('ZSLPUT_STRUCTURE', structures)

        # Assert class library contents
        class_lib_keys = parsed_data.classes.keys()

        self.assertIn('ZSLPUT_CL_CLASS', class_lib_keys)
        self.assertIn('ZSLPUT_IF_INTERFACE', class_lib_keys)

if __name__ == '__main__':
    unittest.main()