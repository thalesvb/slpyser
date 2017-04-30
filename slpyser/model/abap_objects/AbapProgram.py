"""
Definition of AbapProgram class.
"""

from slpyser.model.abap_objects.AbapObject import AbapObject
from slpyser.model.abap_objects.AbapTextPool import AbapTextPool
from slpyser.model.abap_objects.AbapSourceCode import AbapSourceCode


class AbapProgram(AbapObject):
    """
    Representation of an ABAP program.
    """

    def __init__(self,
                 Name,
                 CreatedBy,
                 CreatedOn,
                 ChangedBy,
                 ChangedOn,
                 ProgramType,
                 ProgramStatus):
        """
        Constructor
        """
        super(AbapProgram, self).__init__()
        self.__name = Name
        self.__created_by = CreatedBy
        self.__created_on = CreatedOn
        self.__changed_by = ChangedBy
        self.__changed_on = ChangedOn
        self.__type = ProgramType
        self.__status = ProgramStatus

        self.__text_pool = AbapTextPool()

        self.__source_code = AbapSourceCode()

    @property
    def name(self):
        """
        Program's name
        """
        return self.__name

    @property
    def created_by(self):
        """
        User who created the program.
        """
        return self.__created_by

    @property
    def created_on(self):
        """
        Creation's date.
        """
        return self.__created_on

    @property
    def changed_by(self):
        """
        User who last modified the program.
        """
        return self.__changed_by

    @property
    def changed_on(self):
        """
        Date of the last modification.
        """
        return self.__changed_on

    @property
    def type(self):
        """
        Program's type.

        Possible values are:
         * '1': Executable program
         * 'I': INCLUDE program
         * 'M': Module Pool
         * 'F': Function Group
         * 'S': Subroutine pool
         * 'K': Class pool
         * 'T': Type pool
         * 'X': XSLT program

        Due SAPLink implementation, types F, K should never be parsed as programs, since they are
        handled by specific plugins.
        """
        return self.__type

    @property
    def status(self):
        """
        Program's status.

        Possible values are:
         * 'P': SAP Standard Production Program
         * 'K': Customer Production Program
         * 'S': System Program
         * 'T': Test Program
        """
        return self.__status

    @property
    def text_pool(self):
        """
        Program's text pool (REPS).
        """
        return self.__text_pool

    @property
    def source_code(self):
        """
        Program's source code.
        """
        return self.__source_code
