'''
Created on 04/06/2015

@author: thales
'''
from slpyser.model.abap_objects.AbapObject import AbapObject
from slpyser.model.abap_objects.AbapSourceCode import AbapSourceCode
from slpyser.model.abap_objects.AbapTextPool import AbapTextPool


class AbapClass(AbapObject):
    """
    Representation of an ABAP class.
    """

    def __init__(self,
                 Name,
                 Author,
                 CreatedOn,
                 ChangedBy,
                 ChangedOn,
                 Exposure,
                 OriginalLanguage,
                 Description=None,
                 ParentClassName=None,
                 IsFinal=None,
                 IsFixedPointArithmetic=None,
                 IsUnicode=None):
        '''
        Constructor
        '''

        self.__name = Name
        """Class name, stored in attribute CLSNAME from element CLAS."""

        self.__description = Description
        """Class description, stored in attribute DESCRIPT from element CLAS."""

        self.__parent_class_name = ParentClassName
        """Parent class, stored in attribute REFCLSNAME from element CLAS."""

        self.__exposure = Exposure
        """Class exposure, stored in attribute EXPOSURE from element CLAS."""

        self.__original_language = OriginalLanguage
        """Original language of that class, stored in attribute LANG from element CLAS."""

        self.__final = IsFinal
        """Tells if class is final, stored in attribute CLSFINAL from element CLAS."""

        self.__fixed_point_arithmetic = IsFixedPointArithmetic
        """ Tells if class use fixed point arithmetic, stored in attribute FIXPT from element CLAS."""

        self.__unicode = IsUnicode
        """Tells if class use unicode encoding, stored in attribute UNICODE from element CLAS."""

        self.__author = Author
        """Original author from class, stored in attribute AUTHOR from element CLAS."""

        self.__created_on = CreatedOn
        """Date when class was created"""

        self.__changed_by = ChangedBy
        """Last user who changed the class, stored in attribute CHANGEDBY from element CLAS."""

        self.__changed_on = ChangedOn
        """Date when the last change occurred on this class by user in __changed_by"""

        self.__public_section = AbapSourceCode()
        """The public section of the class (source code), stored in subelement public_section from element CLAS."""

        self.__protected_section = AbapSourceCode()
        """The protected section of the class (source code), stored in subelement protected_section from element CLAS."""

        self.__private_section = AbapSourceCode()
        """The private section of the class (source code), stored in subelement private_section from element CLAS."""

        self.__attributes = {}
        """Class attributes"""

        self.__methods = {}
        """Methods declared in this class (not inherited or redefined from parent class)"""

        self.__redefined_methods = {}
        """Methods that are redefined from parent class."""

        self.__text_pool = AbapTextPool()
        """Class's text pool."""

    @property
    def name(self):
        return self.__name

    @property
    def changed_by(self):
        return self.__changed_by

    @property
    def changed_on(self):
        return self.__changed_on

    @property
    def created_by(self):
        return self.__author

    @property
    def created_on(self):
        return self.__created_on

    @property
    def description(self):
        return self.__description

    @property
    def parent_class(self):
        return self.__parent_class_name

    @property
    def exposure(self):
        return self.__exposure

    @property
    def final(self):
        return self.__final

    @property
    def fixed_point_arithmetic(self):
        return self.__fixed_point_arithmetic

    @property
    def attributes(self):
        return self.__attributes

    @property
    def methods(self):
        return self.__methods

    @property
    def original_language(self):
        return self.__original_language

    @property
    def public_section(self):
        return self.__public_section

    @property
    def protected_section(self):
        return self.__protected_section

    @property
    def private_section(self):
        return self.__private_section

    @property
    def text_pool(self):
        return self.__text_pool

    @property
    def unicode(self):
        return self.__unicode


class AbapClassAttribute(AbapObject):

    def __init__(self,
                 ClassName,
                 AttributeName,
                 AttributeDeclType,
                 AttributeTypType,
                 AttributeExposure,
                 AttributeType,
                 Description):
        self.__compRefName = ClassName
        self.__name = AttributeName
        self.__decl_type = AttributeDeclType
        self.__typType = AttributeTypType
        self.__exposure = AttributeExposure
        self.__type = AttributeType
        self.__description = Description

    @property
    def name(self):
        return self.__name

    @property
    def decl_type(self):
        return self.__decl_type

    @property
    def typType(self):
        return self.__typType

    @property
    def exposure(self):
        return self.__exposure

    @property
    def type(self):
        return self.__type

    @property
    def description(self):
        return self.__description


class AbapClassMethodParameter(AbapObject):
    """
    Class representing a parameter of an ABAP method from an ABAP class.
    """

    def __init__(self,
                 Name,
                 DeclType,
                 PassType,
                 TypType,
                 Type):

        self.__name = Name
        self.__declaration_type = DeclType
        self.__pass_type = PassType
        self.__typ_type = TypType
        self.__type = Type

    @property
    def name(self):
        return self.__name

    @property
    def declaration_type(self):
        return self.__declaration_type

    @property
    def pass_type(self):
        return self.__pass_type

    @property
    def typ_type(self):
        return self.__typ_type

    @property
    def type_(self):
        return self.__type


class AbapClassMethod(AbapObject):
    """
    Representation of a method from an ABAP class.
    """

    def __init__(self,
                 Name,
                 DefinitionClassName,
                 DeclType,
                 Exposure,
                 Description):
        '''
        Constructor
        '''

        self.__name = Name
        self.__definition_class_name = DefinitionClassName
        """Class which declared the method (inherited or not)."""
        self.__decl_type = DeclType
        self.__exposure = Exposure
        self.__description = Description
        self.__parameters = {}
        self.__source_code = AbapSourceCode()

    @property
    def name(self):
        return self.__name

    @property
    def definition_class_name(self):
        return self.__definition_class_name

    @property
    def decl_type(self):
        return self.__decl_type

    @property
    def exposure(self):
        return self.__exposure

    @property
    def description(self):
        return self.__description

    @property
    def parameters(self):
        return self.__parameters

    @property
    def source_code(self):
        return self.__source_code


class AbapInterfaceMethod(AbapClassMethod):
    """Representation of a method declared/inherited from an interface."""
    pass
