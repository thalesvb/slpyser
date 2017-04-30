'''
Created on 04/06/2015

@author: thales
'''
import logging
import xml.sax
import slpyser.xmlparser.handlers as handlers

from slpyser.model.abap_objects.AbapDictionary import AbapDictionary
from slpyser.model.abap_objects.AbapMessageClass import AbapMessageClass
from slpyser.model.abap_objects.AbapTextPool import AbapTextElement


class SAPLinkContentHandle(xml.sax.ContentHandler):
    """
    Implementation for SAX XML parser handle SAPLink file syntax.
    """

    def __init__(self):
        """
        Constructor
        """
        self.__logger = logging.getLogger(__name__)
        xml.sax.ContentHandler.__init__(self)
        self._matrix_element_case_handler = {
            # TextPool elements
            'TEXTPOOL': [
                self._startTextPool,
                self._charactersTextPool,
                self._endTextPool
            ],
            'TEXTELEMENT': [
                self._startTextPoolTextElement,
                self._charactersTextPoolTextElement,
                self._endTextPoolTextElement
            ],

            # Message Class elements
            'MSAG': [
                self._startMessageClass,
                None,
                self._endMessageClass
            ],
            'T100': [
                self._startMessageClassMessage,
                None,
                None,
            ],

            # General elements
            'SOURCE': [
                self._startSourceCode,
                self._charactersSourceCode,
                self._endSourceCode
            ],
            'LANGUAGE': [
                self._startTextLanguage,
                self._charactersTextLanguage,
                self._endTextLanguage
            ],
        }
        """
        Each element have three handlers, declared in that order:
          1st: handle start of an element (retrieve element attributes);
          2nd: handle contents of an element (retrieve data inside element);
          3rd: handle end of an element.
        """
        self.__unhandled_element = [
            self._startUnhandled,
            self._charactersUnhandled,
            self._endUnhandled
        ]

        # Attributes to be returned after parsing
        self._abap_message_classes = {}

        # Internal attributes, store references of current processed abap objects
        self.__current_source_code_reference = None
        self.__current_text_pool_reference = None
        self.__current_class_documentation_reference = None
        self.__current_text_language = None
        self.__current_message_class = None

        # Helper attributes
        self.__current_tag = None
        self.__current_tag_stack = []

        # Decoupled parsers
        self.__programs_parser = handlers.Program(owner=self)
        self._matrix_element_case_handler.update(self.__programs_parser.map_parse())
        self.__ddic_parser = handlers.DDIC(owner=self)
        self._matrix_element_case_handler.update(self.__ddic_parser.map_parse())
        self.__class_library_parser = handlers.ClassLibrary(owner=self)
        self._matrix_element_case_handler.update(self.__class_library_parser.map_parse())
        self.__function_group_parser = handlers.FunctionGroup(owner=self)
        self._matrix_element_case_handler.update(self.__function_group_parser.map_parse())

    @property
    def abapClasses(self):
        return self.__class_library_parser.parsed_classes

    @property
    def abapFunctionGroups(self):
        return self.__function_group_parser.parsed_function_groups

    @property
    def abapMessageClasses(self):
        return self._abap_message_classes

    @property
    def abapDictionary(self):
        return AbapDictionary(Domains=self.__ddic_parser.parsed_domains,
                              DataElements=self.__ddic_parser.parsed_data_elements,
                              Structures=self.__ddic_parser.parsed_structures)

    @property
    def abapPrograms(self):
        return self.__programs_parser.parsed_programs

    def startElement(self, name, attrs):
        """Parses start element"""
        # Upper case on name because SAPLINK haven't used same case on all elements.
        self.__current_tag = name.upper()
        self.__current_tag_stack.append(self.__current_tag)
        startElementHandler = self._matrix_element_case_handler.get(self.__current_tag, self.__unhandled_element)[0]
        if startElementHandler is not None:
            startElementHandler(name.upper(), attrs)

    def characters(self, content):
        """
        Parses inner contents of current element.
        This method is called for each new line inside that element.
        """
        charactersHandler = self._matrix_element_case_handler.get(self.__current_tag, self.__unhandled_element)[1]
        if charactersHandler is not None:
            charactersHandler(content)

    def endElement(self, name):
        """Parses end of element."""
        if self.__current_tag != name.upper():
            self.__logger.error('ERROR parsing file, current element was %s but closing element was %s' % (self.__current_tag, name.upper()))
        endElementHandler = self._matrix_element_case_handler.get(self.__current_tag, self.__unhandled_element)[2]
        if endElementHandler is not None:
            endElementHandler(name.upper())
        self.__current_tag_stack.pop()
        # FIXME: Append None to currentTagStack to avoid little hack?
        self.__current_tag = self.__current_tag_stack[-1] if len(self.__current_tag_stack) > 0 else None

    # Below are declared method to properly handle elements and its contents

    def _startMessageClass(self, name, attrs):
        self.__logger.debug('Start message class')
        name = attrs.get('ARBGB')
        original_language = attrs.get('MASTERLANG')
        responsible = attrs.get('RESPUSER', '')
        short_text = attrs.get('STEXT', '')

        message_class = AbapMessageClass(Name=name,
                                         OriginalLanguage=original_language,
                                         Responsible=responsible,
                                         ShortText=short_text)
        self.__current_message_class = message_class

    def _endMessageClass(self, name):
        msg_class = self.__current_message_class
        self._abap_message_classes[msg_class.name] = msg_class
        self.__current_message_class = None

    def _startMessageClassMessage(self, name, attrs):
        self.__logger.debug('Start Message Class Message')
        language = attrs.get('SPRSL')
        number = attrs.get('MSGNR')
        text = attrs.get('TEXT')

        message = AbapMessageClass.Message(Language=language,
                                           Number=number,
                                           Text=text)

        if self.__current_message_class.language_mapping.get(language) == None:
            self.__current_message_class.language_mapping[language] = {}

        self.__current_message_class.language_mapping[language][number] = message

    def _startSourceCode(self, name, attrs):
        self.__logger.debug('Start Source Code')

    def _charactersSourceCode(self, content):
        self.__current_source_code_reference.source_code.append(content)

    def charactersSourceCode(self, content):
        self._charactersSourceCode(content)

    def _endSourceCode(self, name):
        self.__logger.debug('End Source Code')

    def _startTextLanguage(self, name, attrs):
        self.__logger.debug('Start Text Language')
        self.__current_text_language = attrs.get('SPRAS')
        # Initializing language dict
        if self.__current_text_pool_reference is not None:
            self.__current_text_pool_reference.language_mapping[self.__current_text_language] = {}
        elif self.__current_class_documentation_reference is not None:
            self.__current_class_documentation_reference.languageMappint[self.__current_text_language] = []

    def _charactersTextLanguage(self, content):
        pass

    def _endTextLanguage(self, name):
        self.__logger.debug('End Text Language')
        self.__current_text_language = None

    def _startTextPool(self, name, attrs):
        self.__logger.debug('Start Text Pool')

    def _charactersTextPool(self, content):
        pass

    def _endTextPool(self, name):
        self.__logger.debug('End Text Pool')

    def _startTextPoolTextElement(self, name, attrs):
        self.__logger.debug('Start Text Pool Text Element')
        textId = attrs.get('ID')
        key = attrs.get('KEY')
        entry = attrs.get('ENTRY')
        length = attrs.get('LENGTH')
        textElement = AbapTextElement(TextId=textId,
                                      TextKey=key,
                                      TextEntry=entry,
                                      Length=length)
        if self.__current_text_pool_reference is not None:
            self.__current_text_pool_reference.addTextElement(Language=self.__current_text_language,
                                                              TextElement=textElement)
        else:
            self.__logger.warn('[FIXME] A text pool''s entry "%s" was found but the current abap object wasn''t expecting a text pool.', entry)

    def _charactersTextPoolTextElement(self, content):
        pass

    def _endTextPoolTextElement(self, name):
        self.__logger.debug('End Text Pool Text Element')

    def _startUnhandled(self, name, attrs):
        self.__logger.warning('Start of an unhandled element: %s', name)

    def _charactersUnhandled(self, content):
        self.__logger.warning('Content of unhandled tag: %s', content)

    def _endUnhandled(self, name):
        self.__logger.warning('End of an unhandled element: %s', name)

    def set_current_source_code_reference(self, source_reference):
        self.__current_source_code_reference = source_reference
        source_reference.source_code = []

    def finalize_source_code(self):
        """
        Join the source code's array into a string, and clean it's reference from parser.
        """
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def set_current_textpool_reference(self, textpool_reference):
        self.__current_text_pool_reference = textpool_reference

    def finalize_textpool(self):
        self.__current_text_pool_reference = None
