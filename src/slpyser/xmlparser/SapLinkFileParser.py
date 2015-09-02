'''
Created on 17/06/2015

@author: thales
'''

import codecs
import xml.sax

from slpyser.xmlparser.SAPLinkContentHandle import SAPLinkContentHandle
from xml.sax._exceptions import SAXParseException


class SapLinkFileParser(object):
    """
    Parser implementation.
    It do the dirty job of open file, use custom Content handle to parse
    SAPLink syntax and output all recognizable objects from that file.
    """

    def __init__(self, FilePath):
        """
        This constructor already do the parsing, less work for you!
        """

        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        # override handler
        self.__handler = SAPLinkContentHandle()
        parser.setContentHandler(self.__handler)
        try:
            parser.parse(FilePath)
        except (SAXParseException, UnicodeDecodeError):
            # Some plugins of SAPLink have encoding declared as UTF-16 but
            # default parser can't open it.
            # It opens OK using UTF-8
            parser.parse(codecs.open(FilePath, 'r', 'utf-8'))

    def getClasses(self):

        return self.__handler.abapClasses

    def getFunctionGroups(self):

        return self.__handler.abapFunctionGroups

    def getPrograms(self):

        return self.__handler.abapPrograms
