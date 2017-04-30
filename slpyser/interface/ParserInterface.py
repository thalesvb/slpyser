'''
Created on 17/06/2015

@author: thales
'''
from slpyser.model.saplink.SapLinkFile import NuggetFile
from slpyser.xmlparser.SapLinkFileParser import SapLinkFileParser


class _ParserInterface:
    """
    Handle SAPLink file type, parsing it and returning it's respective object.
    """

    @staticmethod
    def parse_file(FilePath):
        parser = SapLinkFileParser(FilePath=FilePath)

        file = NuggetFile(FilePath=FilePath,
                          AbapClasses=parser.getClasses(),
                          AbapFunctionGroups=parser.getFunctionGroups(),
                          AbapMessageClasses=parser.getMessageClasses(),
                          AbapPrograms=parser.getPrograms(),
                          DataDictionary=parser.getAbapDictionary())
        return file


def parse(FilePath):
    """
    All parsing using the library should use this function to parse file
    """
    return _ParserInterface.parse_file(FilePath)
