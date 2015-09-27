'''
Created on 08/06/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapTextPool(AbapObject):
    """
    TextPools are represented by nested dictionaries.
    """

    def __init__(self):
        '''
        Constructor
        '''
        self.__language_mapping = {}

    @property
    def language_mapping(self):
        return self.__language_mapping

    def addTextElement(self,
                       Language,
                       TextElement):
        self.__language_mapping[Language][TextElement.id] = TextElement


class AbapTextElement(AbapObject):
    """
    Text elements from TextPool
    """

    def __init__(self,
                 TextId,
                 TextKey,
                 TextEntry,
                 Length):

        self.__id = TextId
        self.__key = TextKey
        self.__entry = TextEntry
        self.__length = Length

    def __str__(self):
        return (self.__entry + '( ' + self.__length + ')')

    def __repr__(self):
        return self.__str__()

    @property
    def id(self):
        return self.__id

    @property
    def key(self):
        return self.__key

    @property
    def entry(self):
        return self.__entry

    @property
    def length(self):
        return self.__length


class AbapClassDocumentation(AbapObject):

    def __init__(self,
                 ClassObjectRef):
        self.__class_object_ref = ClassObjectRef
        self.__language_mapping = {}

    @property
    def language_mapping(self):
        return self.__language_mapping

    def addLanguageLine(self,
                        Language,
                        TDFormat,
                        TDLine):
        pass

    class AbapTextLine(AbapObject):

        def __init__(self,
                     TDFormat=None,
                     TDLine=None):

            self.__td_format = TDFormat
            self.__td_line = TDLine

        @property
        def td_format(self):
            return self.__td_format

        @property
        def td_line(self):
            return self.__td_line
