'''
Created on 24/09/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapMessageClass(AbapObject):
    """
    Representation of a Message Class.
    """

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Responsible,
                 ShortText):
        """
        Constructor
        """
        super(AbapMessageClass, self).__init__()
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__responsible = Responsible
        self.__short_text = ShortText

        self.__map_language_message = {}

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def responsible(self):
        return self.__responsible

    @property
    def short_text(self):
        return self.__short_text

    @property
    def language_mapping(self):
        return self.__map_language_message

    class Message(AbapObject):

        def __init__(self,
                     Language,
                     Number,
                     Text):
            super(AbapMessageClass.Message, self).__init__()
            self.__language = Language
            self.__number = Number
            self.__text = Text

        @property
        def language(self):
            return self.__language

        @property
        def number(self):
            return self.__number

        @property
        def text(self):
            return self.__text
