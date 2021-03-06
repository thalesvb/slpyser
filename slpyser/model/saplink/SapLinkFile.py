# -*- coding: utf-8 -*-
"""
Contains models classes representing data parsed from SAPLink files.
"""


class SapLinkFile(object):
    """
    Represents a parsed file from SAPLink xml syntax.
    Its subclasses tells which file type was the original file.
    Such information will be necessary in a (not) near future.
    """

    def __init__(self,
                 FilePath):
        self.__file_path = FilePath

    @property
    def file_path(self):
        return self.__file_path


class NuggetFile(SapLinkFile):
    """
    *.nugg file
    """

    def __init__(self,
                 FilePath,
                 AbapClasses=None,
                 AbapFunctionGroups=None,
                 AbapPrograms=None,
                 AbapMessageClasses=None,
                 DataDictionary=None):
        """
        Assemble the object with all objects parsed from file.
        """
        super(NuggetFile, self).__init__(FilePath=FilePath)
        self.__classes = AbapClasses
        self.__function_groups = AbapFunctionGroups
        self.__programs = AbapPrograms
        self.__message_classes = AbapMessageClasses
        self.__data_dictionary = DataDictionary

        # FIXME: Storing all functions in another attribute to easy development.
        # In the future rewrite it to find inside Function Groups on demand.
        self.__function_modules = {
            functionName: functionImpl
            for function_group in self.__function_groups.values()
            for (functionName, functionImpl) in function_group.function_modules
            .items()
        }

    @property
    def classes(self):
        return self.__classes

    @property
    def function_groups(self):
        return self.__function_groups

    @property
    def function_modules(self):
        return self.__function_modules

    @property
    def message_classes(self):
        return self.__message_classes

    @property
    def programs(self):
        return self.__programs

    @property
    def data_dictionary(self):
        return self.__data_dictionary
