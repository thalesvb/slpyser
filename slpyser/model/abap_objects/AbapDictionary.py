'''
Created on 22/07/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject


class AbapDictionary:
    '''
    Elements from ABAP Dictionary (SE11).
    '''
    def __init__(self,
                 Domains,
                 DataElements,
                 Structures):
        self.__domains = Domains
        self.__data_elements = DataElements
        self.__structures = Structures
    
    @property
    def domains(self):
        return self.__domains

    @property
    def data_elements(self):
        return self.__data_elements

    @property
    def structures(self):
        return self.__structures


class AbapDataElement(AbapObject):
    '''
    Tag DTEL \ DD04V
    '''

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description,
                 DomainUsed,
                 DataType,
                 LabelShort,
                 LabelShortLength,
                 LabelMedium,
                 LabelMediumLength,
                 LabelLong,
                 LabelLongLength,
                 LabelHeading,
                 LabelHeadingLength,
                 Length,
                 OutputLength,
                 LowerCase,
                 Decimals,
                 RefKind,
                 RefType
                 ):
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description
        self.__domain_used = DomainUsed
        self.__data_type = DataType
        self.__label_short = LabelShort
        self.__label_short_length = LabelShortLength
        self.__label_medium = LabelMedium
        self.__label_medium_length = LabelMediumLength
        self.__label_long = LabelLong
        self.__label_long_length = LabelLongLength
        self.__label_heading = LabelHeading
        self.__label_heading_length = LabelHeadingLength
        self.__length = Length
        self.__output_length = OutputLength
        self.__lower_case = LowerCase
        self.__decimals = Decimals
        self.__ref_kind = RefKind
        self.__ref_type = RefType


class AbapDomain(AbapObject):
    '''
    Tag DOMA \ DD01V
    '''

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description,
                 DataType,
                 Length,
                 OutputLength,
                 Decimals,
                 LowerCase,
                 MaskLength):
        '''
        Constructor
        '''
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description
        self.__data_type = DataType
        self.__length = Length
        self.__output_length = OutputLength
        self.__decimals = Decimals
        self.__lower_case = LowerCase
        self.__mask_length = MaskLength

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def description(self):
        return self.__description

    @property
    def data_type(self):
        return self.__data_type

    @property
    def length(self):
        return self.__length

    @property
    def output_length(self):
        return self.__output_length

    @property
    def decimals(self):
        return self.__decimals

    @property
    def lower_case(self):
        return self.__lower_case

    @property
    def mask_length(self):
        return self.__mask_length


class AbapTypeStructure(AbapObject):
    '''
    Tag TABL
    '''

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description):
        '''
        Constructor
        '''
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description

        self.__fields = {}

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def description(self):
        return self.__description

    @property
    def fields(self):
        return self.__fields

    class AbapStructureField(AbapObject):
        '''
        Tag DD03P
        '''

        def __init__(self,
                     Name,
                     Position,
                     DataType):
            self.__name = Name
            self.__position = Position
            self.__data_type = DataType

        @property
        def name(self):
            return self.__name

        @property
        def position(self):
            return self.__position

        @property
        def data_type(self):
            return self.__data_type


class AbapTypeTableType(AbapObject):
    '''
    Tag TTYP
    '''

    def __init__(self,
                 Name,
                 OriginalLanguage,
                 Description,
                 RowType,
                 RowKind):
        '''
        Constructor
        '''
        self.__name = Name
        self.__original_language = OriginalLanguage
        self.__description = Description
        self.__row_type = RowType
        self.__row_kind = RowKind

    @property
    def name(self):
        return self.__name

    @property
    def original_language(self):
        return self.__original_language

    @property
    def description(self):
        return self.__description

    @property
    def row_type(self):
        return self.__row_type

    @property
    def row_kind(self):
        return self.__row_kind
