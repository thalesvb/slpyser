'''
Created on 22/07/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapTypeStructure(AbapObject):
    '''
    classdocs
    '''

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description):
        '''
        Constructor
        '''
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description

        self.__fields = {}

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def description(self):
        return self.__description

    @property
    def fields(self):
        return self.__fields


class AbapTypeTableType(AbapObject):

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description,
                 RowType,
                 RowKind):
        '''
        Constructor
        '''
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description
        self.__row_type = RowType
        self.__row_kind = RowKind

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def description(self):
        return self.__description

    @property
    def row_type(self):
        return self.__row_type

    @property
    def row_kind(self):
        return self.__row_kind
