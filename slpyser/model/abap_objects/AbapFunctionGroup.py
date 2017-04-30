'''
Created on 24/06/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject
from slpyser.model.abap_objects.AbapSourceCode import AbapSourceCode


class AbapFunctionGroup(AbapObject):
    """
    Representation of an ABAP Function Group.
    """

    def __init__(self,
                 Name,
                 Description,
                 OriginalLanguage):
        """
        Constructor
        """
        super(AbapFunctionGroup, self).__init__()
        self.__name = Name
        self.__description = Description
        self.__language = OriginalLanguage
        self.__include_programs = {}
        self.__function_modules = {}

    @property
    def name(self):
        """
        Function Group's name.
        """
        return self.__name

    @property
    def description(self):
        """
        Function group's description.
        """
        return self.__description

    @property
    def language(self):
        return self.__language

    @property
    def main_program(self):
        return self.__include_programs['MAIN']

    @property
    def include_programs(self):
        return self.__include_programs

    @property
    def function_modules(self):
        """
        List of :class:`function modules <.AbapFunctionModule>` from this function group.
        """
        return self.__function_modules


class AbapFunctionGroupMainProgram(AbapObject):
    """
    Main program of the function group.
    """
    def __init__(self,
                 Name):
        super(AbapFunctionGroupMainProgram, self).__init__()
        self.__name = Name
        self.__source = AbapSourceCode()

    @property
    def name(self):
        return self.__name

    @property
    def source(self):
        return self.__source


class AbapFunctionModule(AbapObject):
    """
    Representation of an ABAP Function Module.
    """

    def __init__(self,
                 FunctionGroup,
                 Name,
                 Description):
        super(AbapFunctionModule, self).__init__()
        self.__function_group = FunctionGroup
        self.__name = Name
        self.__description = Description

        self.__parameters_importing = {}
        self.__parameters_exporting = {}
        self.__parameters_changing = {}
        self.__parameters_tables = {}
        self.__exceptions = {}

        self.__source_code = AbapSourceCode()

    @property
    def function_group(self):
        return self.__function_group

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def parameters_importing(self):
        return self.__parameters_importing

    @property
    def parameters_exporting(self):
        return self.__parameters_exporting

    @property
    def parameters_changing(self):
        return self.__parameters_changing

    @property
    def parameters_tables(self):
        return self.__parameters_tables

    @property
    def exceptions(self):
        return self.__exceptions

    @property
    def source_code(self):
        return self.__source_code

    class AbapFunctionModuleParameter(AbapObject):

        def __init__(self,
                     Parameter,
                     IsReference,
                     IsOptional,
                     Type,
                     DefaultValue):
            super(AbapFunctionModule.AbapFunctionModuleParameter, self).__init__()
            self.__name = Parameter
            self.__is_reference = IsReference
            self.__is_optional = IsOptional
            self.__type = Type
            self.__default_value = DefaultValue

        @property
        def name(self):
            return self.__name

        @property
        def is_reference(self):
            return self.__is_reference

        @property
        def is_optional(self):
            return self.__is_optional

        @property
        def typ(self):
            return self.__type

        @property
        def default_value(self):
            return self.__default_value
