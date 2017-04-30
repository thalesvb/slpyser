# -*- coding: utf-8 -*-
import logging

from slpyser.model.abap_objects.AbapDictionary import AbapDomain, AbapDataElement, \
    AbapTypeStructure
from .AbstractHandler import AbstractHandler


class DDICHandler(AbstractHandler):

    def __init__(self, owner):
        super(DDICHandler, self).__init__(owner=owner)
        self.__logger = logging.getLogger(__name__)
        self.__owner = owner

        self.__current_data_element = None
        self._abap_ddic_structures = {}
        self._abap_ddic_domain = {}
        self._abap_ddic_data_element = {}

    @property
    def parsed_data_elements(self):
        return self._abap_ddic_data_element

    @property
    def parsed_domains(self):
        return self._abap_ddic_domain

    @property
    def parsed_structures(self):
        return self._abap_ddic_structures

    def map_parse(self):
        # ABAP Dictionary
        return {
            # # Domain
            'DOMA' : [
                self._startDomainDeclaration,
                None,
                self._endDomainDeclaration,
            ],
            'DD01V' : [
                self._startDomainDefinition,
                None,
                self._endDomainDefinition,
            ],
            # # Data Element
            'DTEL' : [
                self._startDataElementDeclaration,
                None,
                self._endDataElementDeclaration
            ],
            'DD04V' : [
                self._startDataElementDefinition,
                None,
                self._endDataElementDefinition
            ],

            'DDLANGUAGE' : [
                None,
                None,
                None
            ],

            # # Structure
            'TABL' : [
                self._startStructure,
                None,
                self._endStructure
            ],
            'DD03P' : [
                self._startStructureField,
                None,
                None
            ],
            # # Table Type
            'TTYP' : [
                None,
                None,
                None
            ],
        }

    def _startDataElementDeclaration(self, name, attrs):
        self.__logger.debug('Start data element declaration')
        name = attrs.get('ROLLNAME', '')
        description = attrs.get('DDTEXT', '')
        data_type = attrs.get('DATATYPE', '')
        domain_used = attrs.get('DOMNAME', '')
        label_short = attrs.get('SCRTEXT_S', '')
        label_short_length = attrs.get('SCRLEN1', '')
        label_medium = attrs.get('SCRTEXT_M', '')
        label_medium_length = attrs.get('SCRLEN2', '')
        label_long = attrs.get('SCRTEXT_L', '')
        label_long_length = attrs.get('SCRLEN3', '')
        label_heading = attrs.get('REPTEXT', '')
        label_heading_length = attrs.get('HEADLEN', '')
        multilanguage_support = attrs.get('MultiLanguageSupport', '')
        ref_kind = attrs.get('REFKIND', '')

    def _endDataElementDeclaration(self, name):
        self.__logger.debug('End data element declaration')

    def _startDataElementDefinition(self, name, attrs):
        self.__logger.debug('Start data element definition')
        name = attrs.get('ROLLNAME', '')
        original_language = attrs.get('DDLANGUAGE', '')
        description = attrs.get('DDTEXT', '')
        domain_used = attrs.get('DOMNAME', '')
        data_type = attrs.get('DATATYPE', '')
        label_short = attrs.get('SCRTEXT_S', '')
        label_short_length = attrs.get('SCRLEN1', '')
        label_medium = attrs.get('SCRTEXT_M', '')
        label_medium_length = attrs.get('SCRLEN2', '')
        label_long = attrs.get('SCRTEXT_L', '')
        label_long_length = attrs.get('SCRLEN3', '')
        label_heading = attrs.get('REPTEXT', '')
        label_heading_length = attrs.get('HEADLEN', '')
        length = attrs.get('LENG', '')
        output_length = attrs.get('OUTPUTLEN', '')
        lower_case = attrs.get('LOWERCASE', '')
        decimals = attrs.get('DECIMALS', '')
        ref_kind = attrs.get('REFKIND', '')
        ref_type = attrs.get('REFTYPE', '')

        data_element = AbapDataElement(Name=name,
                                       OriginalLanguage=original_language,
                                       Description=description,
                                       DomainUsed=domain_used,
                                       DataType=data_type,
                                       LabelShort=label_short,
                                       LabelShortLength=label_short_length,
                                       LabelMedium=label_medium,
                                       LabelMediumLength=label_medium_length,
                                       LabelLong=label_long,
                                       LabelLongLength=label_long_length,
                                       LabelHeading=label_heading,
                                       LabelHeadingLength=label_heading_length,
                                       Length=length,
                                       OutputLength=output_length,
                                       LowerCase=lower_case,
                                       Decimals=decimals,
                                       RefKind=ref_kind,
                                       RefType=ref_type)

        self._abap_ddic_data_element[name] = data_element

    def _endDataElementDefinition(self, name):
        self.__logger.debug('End data element definition')

    def _startDomainDeclaration(self, name, attrs):
        self.__logger.debug('Start domain declaration')
        domain_name = attrs.get('DOMNAME', '')
        multilanguage_support = attrs.get('MultiLanguageSupport', '')

    def _endDomainDeclaration(self, name):
        self.__logger.debug('End domain declaration')

    def _startDomainDefinition(self, name, attrs):
            self.__logger.debug('Start domain definition')
            domain_name = attrs.get('DOMNAME', '')
            language = attrs.get('DDLANGUAGE', '')
            description = attrs.get('DDTEXT', '')
            data_type = attrs.get('DATA_TYPE', '')
            length = attrs.get('LENG','')
            output_length = attrs.get('OUTPUTLEN', '')
            decimals = attrs.get('DECIMALS', '')
            lower_case = attrs.get('LOWERCASE', '')
            mask_length = attrs.get('MASKLEN', '')

            domain = AbapDomain(Name=domain_name,
                                OriginalLanguage=language,
                                Description=description,
                                DataType=data_type,
                                Length=length,
                                OutputLength=output_length,
                                Decimals=decimals,
                                LowerCase=lower_case,
                                MaskLength=mask_length)
            
            self._abap_ddic_domain[domain_name] = domain

    def _endDomainDefinition(self, name):
        self.__logger.debug('End domain definition')

    def _startStructure(self, name, attrs):
        self.__logger.debug('Start Structure')
        name = attrs.get('TABNAME')
        original_language = attrs.get('DDLANGUAGE')
        description = attrs.get('DDTEXT')
        structure = AbapTypeStructure(Name=name,
                                      OriginalLanguage=original_language,
                                      Description=description)
        self.__current_data_element = structure

    def _endStructure(self, name):
        self.__logger.debug('End Structure')
        self._abap_ddic_structures[self.__current_data_element.name] = self.__current_data_element
        self.__current_data_element = None

    def _startStructureField(self, name, attrs):
        self.__logger.debug('Start Structure Field')
        field_name = attrs.get('FIELDNAME')
        position = attrs.get('POSITION')
        inttype = attrs.get('INTTYPE')
        intlength = attrs.get('INTLEN')
        data_type = attrs.get('DATATYPE')
        length = attrs.get('LENG')
        output_length = attrs.get('OUTPUTLEN')
        decimals = attrs.get('DECIMALS')
        mask = attrs.get('MASK')
        mask_length = attrs.get('MASKLEN')
        
        structure_attribute = AbapTypeStructure.AbapStructureField(Name=field_name,
                                                                   Position=position,
                                                                   DataType=data_type)
        self.__current_data_element.fields[field_name] = structure_attribute
