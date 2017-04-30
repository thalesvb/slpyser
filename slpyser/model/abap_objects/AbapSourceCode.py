"""
Definition of AbapSourceCode class
"""


from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapSourceCode(AbapObject):
    """
    Source code from function modules, class methods, class sections, ...

    While parsing, the source code lines are stacked in an array, and when
    its tag closes, a join operation is performed on that array to create a
    string representation of source code.
    """

    def __init__(self,
                 SourceCode=None):
        """
        Constructor
        """
        super(AbapSourceCode, self).__init__()
        self.source_code = SourceCode
