'''
Created on 04/06/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapSourceCode(AbapObject):
    """
    Source code from function modules, class methods, class sections, ...
    While parsing, the source code lines are stacked in an array, and when
    its tag closes, a join operation is performed on that array to create a
    string representation of that source code.
    """

    def __init__(self,
                 SourceCode=None):
        '''
        Constructor
        '''
        self.source_code = SourceCode
