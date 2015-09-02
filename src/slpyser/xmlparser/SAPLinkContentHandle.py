'''
Created on 04/06/2015

@author: thales
'''
import logging
import xml.sax

from slpyser.model.abap_objects.AbapClass import AbapClass, AbapClassMethod, \
    AbapClassAttribute, AbapClassMethodParameter
from slpyser.model.abap_objects.AbapFunctionGroup import AbapFunctionGroup, \
    AbapFunctionGroupMainProgram, AbapFunctionModule
from slpyser.model.abap_objects.AbapProgram import AbapProgram
from slpyser.model.abap_objects.AbapTextPool import AbapTextElement, \
    AbapClassDocumentation


class SAPLinkContentHandle(xml.sax.ContentHandler):
    """
    Implementation for SAX XML parser handle SAPLink file syntax.
    """

    def __init__(self):
        '''
        Constructor
        '''
        self.__logger = logging.getLogger(__name__)
        xml.sax.ContentHandler.__init__(self)
        self._matrix_element_case_handler = {
            # Classes specific elements
            'CLAS': [
                self._startClass,
                None,
                self._endClass
            ],
            'CLASSDOCUMENTATION': [
                None,
                None,
                None
            ],
            'INHERITANCE': [
                self._startClassInheritance,
                None,
                self._endClassInheritance
            ],
            'PUBLICSECTION': [
                self._startClassPublicSection,
                self._charactersClassPublicSection,
                self._endClassPublicSection
            ],
            'PROTECTEDSECTION': [
                self._startClassProtectedSection,
                self._charactersClassProtectedSection,
                self._endClassProtectedSection
            ],
            'PRIVATESECTION': [
                self._startClassPrivateSection,
                self._charactersClassPrivateSection,
                self._endClassPrivateSection
            ],
            'LOCALIMPLEMENTATION': [
                self._startClassLocalImplementation,
                None,
                self._endClassLocalImplementation
            ],
            'LOCALTYPES': [
                self._startClassLocalTypes,
                None,
                self._endClassLocalTypes
            ],
            'LOCALMACROS': [
                self._startClassLocalMacros,
                None,
                self._endClassLocalMacros
            ],
            'METHOD': [
                self._startClassMethod,
                None,
                self._endClassMethod
            ],
            'INTERFACEMETHOD': [
                self._startInterfaceMethod,
                None,
                self._endInterfaceMethod,
            ],
            'PARAMETER': [
                self._startClassMethodParameter,
                None,
                None,
            ],
            'ATTRIBUTE': [
                self._startClassAttribute,
                None,
                self._endClassAttribute
            ],
            'REDEFINITION': [
                self._startClassMethodRedefinition,
                None,
                self._endClassMethodRedefinition
            ],

            # Function Groups and Function Modules specific elements
            'FUGR': [
                self._startFunctionGroup,
                None,
                self._endFunctionGroup
            ],
            'MAINPROGRAM': [
                self._startFunctionGroupMainProgram,
                None,
                self._endFunctionGroupMainProgram
            ],
            'INCLUDEPROGRAMS': [
                None,
                None,
                None
            ],
            'INCLUDE': [
                None,
                None,
                None
            ],
            'FUNCTIONMODULES': [
                None,
                None,
                None
            ],
            'FUNCTIONMODULE': [
                self._startFunctionModule,
                None,
                self._endFunctionModule
            ],
            'IMPORTING': [
                self._startFunctionModuleParameter,
                None,
                self._endFunctionModuleParameter
            ],
            'EXPORTING': [
                self._startFunctionModuleParameter,
                None,
                self._endFunctionModuleParameter
            ],
            'CHANGING': [
                self._startFunctionModuleParameter,
                None,
                self._endFunctionModuleParameter
            ],
            'TABLES': [
                self._startFunctionModuleParameter,
                None,
                self._endFunctionModuleParameter
            ],
            'EXCEPTIONS': [
                self._startFunctionModuleException,
                None,
                None
            ],
            'FM_SOURCE': [
                self._startFunctionModuleSourceCode,
                self._charactersFunctionModuleSourceCode,
                self._endFunctionModuleSourceCode
            ],
            'FM_SOURCE_NEW': [
                self._startFunctionModuleSourceCode,
                self._charactersFunctionModuleSourceCode,
                self._endFunctionModuleSourceCode
            ],

            # Programs specific elements
            'PROG': [
                self._startProgram,
                None,
                self._endProgram
            ],

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
        self._abapClasses = {}
        self._abapFunctionGroups = {}
        self._abapPrograms = {}

        # Internal attributes, store references of current processed abap objects
        self.__current_class = None
        self.__current_function_group = None
        self.__current_function_module = None
        self.__current_program = None
        self.__current_source_code_reference = None
        self.__current_text_pool_reference = None
        self.__current_class_documentation_reference = None
        self.__current_text_language = None

        # Helper attributes
        self.__current_tag = None
        self.__current_tag_stack = []

    @property
    def abapClasses(self):
        return self._abapClasses

    @property
    def abapFunctionGroups(self):
        return self._abapFunctionGroups

    @property
    def abapPrograms(self):
        return self._abapPrograms

    def startElement(self, name, attrs):
        """Parses start element"""
        # Upper case on name because SAPLINK haven't used same case on all elements.
        self.__current_tag = name.upper()
        self.__current_tag_stack.append(self.__current_tag)
        startElementHandler = self._matrix_element_case_handler.get(self.__current_tag, self.__unhandled_element)[0]
        if startElementHandler is not None:
            startElementHandler(name, attrs)

    def characters(self, content):
        """
        Parses inner contents of current element.
        This method is called for each new line inside that element.
        """
        charactersHandler = self._matrix_element_case_handler.get(self.__current_tag,self.__unhandled_element)[1]
        if charactersHandler is not None:
            charactersHandler(content)

    def endElement(self, name):
        """Parses end of element."""
        if self.__current_tag != name.upper():
            self.__logger.error('ERROR parsing file, current element was %s but closing element was %s' % (self.__current_tag, name.upper()))
        endElementHandler = self._matrix_element_case_handler.get(self.__current_tag, self.__unhandled_element)[2]
        if endElementHandler is not None:
            endElementHandler(name)
        self.__current_tag_stack.pop()
        # FIXME: Append None to currentTagStack to avoid little hack?
        self.__current_tag = self.__current_tag_stack[-1] if len(self.__current_tag_stack) > 0 else None

    # Below are declared method to properly handle elements and its contents
    def _startClass(self, name, attrs):
        self.__logger.debug('Start Class')

        name = attrs.get('CLSNAME', '')
        author = attrs.get('AUTHOR', '')
        created_on = attrs.get('CREATEDON', '')
        changed_by = attrs.get('CHANGEDBY', '')
        changed_on = attrs.get('CHANGEDON', '')
        description = attrs.get('DESCRIPT', '')
        exposure = attrs.get('EXPOSURE', '')
        original_language = attrs.get('LANGU', '')
        final = attrs.get('CLSFINAL', '')
        fixed_point_arithmetic = attrs.get('FIXPT', '')
        parentClassName = attrs.get('REFCLSNAME', '')
        unicode = attrs.get('UNICODE', '')

        abapClass = AbapClass(Name=name,
                              Author=author,
                              CreatedOn=created_on,
                              ChangedBy=changed_by,
                              ChangedOn=changed_on,
                              Exposure=exposure,
                              OriginalLanguage=original_language,
                              Description=description,
                              ParentClassName=parentClassName,
                              IsFinal=final,
                              IsFixedPointArithmetic=fixed_point_arithmetic,
                              IsUnicode=unicode)

        self.__current_class = abapClass

    def _endClass(self, name):
        self.__logger.debug('End class')
        self.abapClasses[self.__current_class.name] = self.__current_class
        self.__current_class = None

    def _startClassAttribute(self, name, attrs):
        self.__logger.debug('Start class attribute')
        classRefName = attrs.get('CLSNAME', '')
        componentName = attrs.get('CMPNAME', '')
        description = attrs.get('DESCRIPT', '')
        declarationType = attrs.get('ATTDECLTYP', '')
        exposure = attrs.get('EXPOSURE', '')
        typType = attrs.get('TYPTYPE', '')
        attrType = attrs.get('TYPE', '')

        classAttribute = AbapClassAttribute(ClassName=classRefName,
                                            AttributeName=componentName,
                                            AttributeDeclType=declarationType,
                                            AttributeTypType=typType,
                                            AttributeExposure=exposure,
                                            AttributeType=attrType,
                                            Description=description)
        self.__current_class.attributes[componentName] = classAttribute

    def _endClassAttribute(self, name):
        self.__logger.debug('End class attribute')

    def _startClassDocumentation(self, name, attrs):
        self.__logger.debug('Start class documentation')
        classObject = attrs.get('OBJECT')
        classDocumentation = AbapClassDocumentation(ClassObjectRef=classObject)
        self.__current_class_documentation_reference = classDocumentation

    def _endClassDocumentation(self, name):
        self.__logger.debug('End class documentation')
        self.__current_class_documentation_reference = None

    def _startClassInheritance(self, name, attrs):
        self.__logger.debug('Start class inheritance')

    def _endClassInheritance(self, name):
        self.__logger.debug('End class inheritance')

    def _startClassMethod(self, name, attrs):
        self.__logger.debug('Start class method')
        name = attrs.get('CMPNAME')
        definition_class_name = attrs.get('CLSNAME', '')
        declarationType = attrs.get('MTDDECLTYP', '')
        exposure = attrs.get('EXPOSURE', '')
        description = attrs.get('DESCRIPT', '')

        classMethod = AbapClassMethod(Name=name,
                                      DefinitionClassName=definition_class_name,
                                      DeclType=declarationType,
                                      Exposure=exposure,
                                      Description=description)

        self.__current_class.methods[classMethod.name] = classMethod
        self.__current_source_code_reference = classMethod.source_code
        self.__current_source_code_reference.source_code = []

    def _endClassMethod(self, name):
        self.__logger.debug('End class method')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startClassMethodParameter(self, name, attrs):
        self.__logger.debug('Start class method parameter')
        name = attrs.get('SCONAME', '')
        decl_type = attrs.get('PARDECLTYP', '')
        pass_type = attrs.get('PARPASSTYP', '')
        typ_type = attrs.get('TYPTYPE', '')
        type_ = attrs.get('TYPE', '')

        ref_method = attrs.get('CMPNAME')
        ref_class = attrs.get('CLSNAME')

        methodParameter = AbapClassMethodParameter(Name=name,
                                                   DeclType=decl_type,
                                                   PassType=pass_type,
                                                   TypType=typ_type,
                                                   Type=type_)
        self.__current_class.methods[ref_method].parameters[name] = methodParameter

    def _startClassMethodRedefinition(self, name, attrs):
        self.__logger.debug('Start Method Redefinition')

    def _endClassMethodRedefinition(self, name):
        self.__logger.debug('End class method redefinition')

    def _startClassPublicSection(self, name, attrs):
        self.__logger.debug('Start public section')
        self.__current_source_code_reference = self.__current_class.public_section
        self.__current_source_code_reference.source_code = []

    def _charactersClassPublicSection(self, content):
        self.__current_source_code_reference.source_code.append(content)

    def _endClassPublicSection(self, name):
        self.__logger.debug('End class public section')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startClassProtectedSection(self, name, attrs):
        self.__logger.debug('Start protected section')
        self.__current_source_code_reference = self.__current_class.protected_section
        self.__current_source_code_reference.source_code = []

    def _charactersClassProtectedSection(self, content):
        self.__current_source_code_reference.source_code.append(content)

    def _endClassProtectedSection(self, name):
        self.__logger.debug('End class protected section')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startClassPrivateSection(self, name, attrs):
        self.__logger.debug('Start private section')
        self.__current_source_code_reference = self.__current_class.private_section
        self.__current_source_code_reference.source_code = []

    def _charactersClassPrivateSection(self, content):
        self.__current_source_code_reference.source_code.append(content)

    def _endClassPrivateSection(self, name):
        self.__logger.debug('End class private section')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startClassLocalImplementation(self, name, attrs):
        self.__logger.debug('Start class local implementation')

    def _endClassLocalImplementation(self, name):
        self.__logger.debug('End class local implementation')

    def _startClassLocalTypes(self, name, attrs):
        self.__logger.debug('Start class local types')

    def _endClassLocalTypes(self, name):
        self.__logger.debug('End class local types')

    def _startClassLocalMacros(self, name, attrs):
        self.__logger.debug('Start class local macros')

    def _endClassLocalMacros(self, name):
        self.__logger.debug('End class local types')

    def _startFunctionGroup(self, name, attrs):
        self.__logger.debug('Start function group')
        name = attrs.get('AREA')
        description = attrs.get('AREAT')
        original_language = attrs.get('SPRAS')
        function_group = AbapFunctionGroup(Name=name,
                                           Description=description,
                                           OriginalLanguage=original_language)

        self.__current_function_group = function_group

    def _endFunctionGroup(self, name):
        self.__logger.debug('End function group')
        self.abapFunctionGroups[self.__current_function_group.name] = self.__current_function_group
        self.__current_function_group = None

    def _startFunctionGroupMainProgram(self, name, attrs):
        self.__logger.debug('Start function group main program')
        name = attrs.get('NAME', '')
        created_by = attrs.get('CNAM', '')
        created_on = attrs.get('CDAT', '')
        changed_by = attrs.get('UNAM', '')
        changed_on = attrs.get('UDAT', '')

        main_program = AbapFunctionGroupMainProgram(Name=name)
        self.__current_function_group.include_programs['MAIN'] = main_program
        self.__current_source_code_reference = main_program.source
        self.__current_source_code_reference.source_code = []

    def _endFunctionGroupMainProgram(self, name):
        self.__logger.debug('End function group main program')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startFunctionModule(self, name, attrs):
        self.__logger.debug('Start function module')
        name = attrs.get('NAME')
        description = attrs.get('STEXT')
        functionModule = AbapFunctionModule(FunctionGroup=self.__current_function_group,
                                            Name=name,
                                            Description=description)
        self.__current_function_module = functionModule
        self.__current_source_code_reference = functionModule.source_code
        self.__current_source_code_reference.source_code = []

    def _endFunctionModule(self, name):
        self.__logger.debug('End function module')
        self.__current_function_group.function_modules[self.__current_function_module.name] = self.__current_function_module
        self.__current_function_module = None
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startFunctionModuleSourceCode(self, name, attrs):
        self.__logger.debug('Start function module source code')

    def _charactersFunctionModuleSourceCode(self, content):
        # Should do same thing as _charactersSourceCode
        self._charactersSourceCode(content)

    def _endFunctionModuleSourceCode(self, name):
        self.__logger.debug('End function module source code')

    def _startFunctionModuleException(self, name, attrs):
        self.__logger.debug('Start function module exception')
        exceptionName = attrs.get('EXCEPTION', '')
        self.__current_function_module.exceptions[exceptionName] = exceptionName

    def _startFunctionModuleParameter(self, name, attrs):
        """
        Process importing, exporting and tables parameter from functionModule.
        """
        self.__logger.debug('Start function module parameter: %s', name)
        parameter = attrs.get('PARAMETER', '')
        reference = attrs.get('REFERENCE', '')
        optional = attrs.get('OPTIONAL', '')
        typ = attrs.get('TYP', '')
        default_value = attrs.get('DEFAULT', '')
        functionParameter = AbapFunctionModule.AbapFunctionModuleParameter(Parameter=parameter,
                                                                           IsReference=reference,
                                                                           IsOptional=optional,
                                                                           Type=typ,
                                                                           DefaultValue=default_value)
        if name == 'importing':
            self.__current_function_module.parameters_importing[parameter] = functionParameter
        elif name == 'exporting':
            self.__current_function_module.parameters_exporting[parameter] = functionParameter
        elif name == 'changing':
            self.__current_function_module.parameters_changing[parameter] = functionParameter
        elif name == 'tables':
            self.__current_function_module.parameters_tables[parameter] = functionParameter

    def _endFunctionModuleParameter(self, name):
        self.__logger.debug('End function module parameter: %s', name)

    def _startInterfaceMethod(self, name, attrs):
        self.__logger.debug('Start interface method')
        name = attrs.get('CPDNAME')
        definition_class_name = attrs.get('CLSNAME', '')
        declarationType = attrs.get('MTDDECLTYP', '')
        exposure = attrs.get('EXPOSURE', '')
        description = attrs.get('DESCRIPT', '')

        interfaceMethod = AbapClassMethod(Name=name,
                                      DefinitionClassName=definition_class_name,
                                      DeclType=declarationType,
                                      Exposure=exposure,
                                      Description=description)

        self.__current_class.methods[interfaceMethod.name] = interfaceMethod
        self.__current_source_code_reference = interfaceMethod.source_code
        self.__current_source_code_reference.source_code = []

    def _endInterfaceMethod(self, name):
        self.__logger.debug('End interface method')
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startProgram(self, name, attrs):
        self.__logger.debug('Start program')
        name = attrs.get('NAME')
        created_by = attrs.get('CNAM')
        created_on = attrs.get('CDAT')
        changed_by = attrs.get('UNAM')
        changed_on = attrs.get('UDAT')
        programType = attrs.get('SUBC')
        programStatus = attrs.get('RSTAT')

        program = AbapProgram(Name=name,
                              CreatedBy=created_by,
                              CreatedOn=created_on,
                              ChangedBy=changed_by,
                              ChangedOn=changed_on,
                              ProgramType=programType,
                              ProgramStatus=programStatus)

        self.__current_program = program
        self.__current_source_code_reference = program.source_code
        self.__current_source_code_reference.source_code = []
        self.__current_text_pool_reference = program.text_pool

    def _endProgram(self, name):
        self.__logger.debug('End program')
        self.abapPrograms[self.__current_program.name] = self.__current_program
        self.__current_program = None
        self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        self.__current_source_code_reference = None

    def _startSourceCode(self, name, attrs):
        self.__logger.debug('Start Source Code')

    def _charactersSourceCode(self, content):
        self.__current_source_code_reference.source_code.append(content)

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
        entry = attrs.get('ENTRY')
        length = attrs.get('LENGTH')
        textElement = AbapTextElement(TextId=textId,
                                      TextEntry=entry,
                                      Length=length)
        self.__current_text_pool_reference.addTextElement(Language=self.__current_text_language,
                                                          TextElement=textElement)

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
