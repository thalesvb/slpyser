# -*- coding: utf-8 -*-
"""
Handle parsing of program data contained in a SAPLink file.
"""

import logging

from slpyser.model.abap_objects.AbapProgram import AbapProgram
from .AbstractHandler import AbstractHandler

class ProgramHandler(AbstractHandler):
    """
    Handles the parsing of Programs.
    """

    def __init__(self, owner):
        super(ProgramHandler, self).__init__(owner=owner)
        self.__logger = logging.getLogger(__name__)
        self.__current_program = None
        self.__abap_programs = {}

    def map_parse(self):
        """
        Tags used by programs.
        """
        return {
            'PROG': [
                self.__start_program,
                None,
                self.__end_program
            ],
        }

    @property
    def parsed_programs(self):
        """
        Dictionary containing programs parsed from file.

        Those programs are encapsulated in
        :class:`~slpyser.model.abap_objects.AbapProgram.AbapProgram` objects.
        """
        return self.__abap_programs

    def __start_program(self, name, attrs):
        self.__logger.debug('Start program')
        name = attrs.get('NAME')
        created_by = attrs.get('CNAM')
        created_on = attrs.get('CDAT')
        changed_by = attrs.get('UNAM')
        changed_on = attrs.get('UDAT')
        program_type = attrs.get('SUBC')
        program_status = attrs.get('RSTAT')

        program = AbapProgram(Name=name,
                              CreatedBy=created_by,
                              CreatedOn=created_on,
                              ChangedBy=changed_by,
                              ChangedOn=changed_on,
                              ProgramType=program_type,
                              ProgramStatus=program_status)

        self.__current_program = program
        self._owner.set_current_source_code_reference(source_reference=program.source_code)
        self._owner.set_current_textpool_reference(textpool_reference=program.text_pool)

    def __end_program(self, name):
        self.__logger.debug('End program' + name)
        self.__abap_programs[self.__current_program.name] = self.__current_program
        self._owner.finalize_source_code()
        self._owner.finalize_textpool()
        self.__current_program = None
