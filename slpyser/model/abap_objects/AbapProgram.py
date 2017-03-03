'''
Created on 08/06/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapTextPool import AbapTextPool
from slpyser.model.abap_objects.AbapSourceCode import AbapSourceCode


class AbapProgram(object):
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
        '''
        Constructor
        '''
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
        return self.__name

    @property
    def created_by(self):
        return self.__created_by

    @property
    def created_on(self):
        return self.__created_on

    @property
    def changed_by(self):
        return self.__changed_by

    @property
    def changed_on(self):
        return self.__changed_on

    @property
    def type(self):
        return self.__type

    @property
    def status(self):
        return self.__status

    @property
    def text_pool(self):
        return self.__text_pool

    @property
    def source_code(self):
        return self.__source_code
