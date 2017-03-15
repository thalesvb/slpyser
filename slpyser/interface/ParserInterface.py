'''
Created on 17/06/2015

@author: thales
'''
from slpyser.model.saplink.SapLinkFile import NuggetFile
from slpyser.model.abap_objects.AbapDictionary import AbapDictionary
from slpyser.xmlparser.SapLinkFileParser import SapLinkFileParser


class _ParserInterface:
    """
    Handle SAPLink file type, parsing it and returning it's respective object.
    """

    @staticmethod
    def parse_file(FilePath):
        parser = SapLinkFileParser(FilePath=FilePath)

        data_dictionary = AbapDictionary(Domains=parser.getDomains(),
                                         DataElements=parser.getDataElements(),
                                         Structures=parser.getStructures())

        file = NuggetFile(FilePath=FilePath,
                          AbapClasses=parser.getClasses(),
                          AbapFunctionGroups=parser.getFunctionGroups(),
                          AbapMessageClasses=parser.getMessageClasses(),
                          AbapPrograms=parser.getPrograms(),
                          DataDictionary=data_dictionary)
        return file


def parse(FilePath):
    """
    All parsing using the library should use this function to parse file
    """
    return _ParserInterface.parse_file(FilePath)
