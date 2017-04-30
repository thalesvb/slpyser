# -*- coding: utf-8 -*-

import logging

from slpyser.model.abap_objects.AbapFunctionGroup import AbapFunctionGroup, \
    AbapFunctionGroupMainProgram, AbapFunctionModule
from .AbstractHandler import AbstractHandler


class FunctionGroupHandler(AbstractHandler):

    def __init__(self, owner):
        super(FunctionGroupHandler, self).__init__(owner=owner)
        self.__logger = logging.getLogger(__name__)
        self.__owner = owner

        self._abap_function_groups = {}
        self.__current_function_group = None
        self.__current_function_module = None

    @property
    def parsed_function_groups(self):
        return self._abap_function_groups

    def map_parse(self):
        return {
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
                self.__owner.charactersSourceCode,
                self._endFunctionModuleSourceCode
            ],
            'FM_SOURCE_NEW': [
                self._startFunctionModuleSourceCode,
                self.__owner.charactersSourceCode,
                self._endFunctionModuleSourceCode
            ],
        }

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
        self._abap_function_groups[self.__current_function_group.name] = self.__current_function_group
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
        # self.__current_source_code_reference = main_program.source
        # self.__current_source_code_reference.source_code = []
        self.__owner.set_current_source_code_reference(main_program.source)

    def _endFunctionGroupMainProgram(self, name):
        self.__logger.debug('End function group main program')
        # self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        # self.__current_source_code_reference = None
        self.__owner.finalize_source_code()

    def _startFunctionModule(self, name, attrs):
        self.__logger.debug('Start function module')
        name = attrs.get('NAME')
        description = attrs.get('STEXT')
        functionModule = AbapFunctionModule(FunctionGroup=self.__current_function_group,
                                            Name=name,
                                            Description=description)
        self.__current_function_module = functionModule
        # self.__current_source_code_reference = functionModule.source_code
        # self.__current_source_code_reference.source_code = []
        self.__owner.set_current_source_code_reference(functionModule.source_code)

    def _endFunctionModule(self, name):
        self.__logger.debug('End function module')
        self.__current_function_group.function_modules[self.__current_function_module.name] = self.__current_function_module
        self.__current_function_module = None
        # self.__current_source_code_reference.source_code = ''.join(self.__current_source_code_reference.source_code)
        # self.__current_source_code_reference = None
        self.__owner.finalize_source_code()

    def _startFunctionModuleSourceCode(self, name, attrs):
        self.__logger.debug('Start function module source code')

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
