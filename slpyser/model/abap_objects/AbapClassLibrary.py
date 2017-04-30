"""
Represents class library (TCode SE24) objects, which are global classes and global interfaces.

This module contains the definition of the following classes:

 * :class:`.AbapClass`
 * :class:`.AbapClassInterface`
 * :class:`.AbapClassAttribute`
 * :class:`.AbapClassMethodParameter`
 * :class:`.AbapClassMethod`
 * :class:`.AbapInterfaceMethod`
"""


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
        """
        Constructor
        """

        super(AbapClass, self).__init__()

        self.__name = Name
        """Class's name, stored in attribute CLSNAME from element CLAS."""

        self.__description = Description
        """Class's description, stored in attribute DESCRIPT from element CLAS."""

        self.__parent_class_name = ParentClassName
        """Parent class, stored in attribute REFCLSNAME from element CLAS."""

        self.__exposure = Exposure
        """Class's exposure, stored in attribute EXPOSURE from element CLAS."""

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

        self.__local_implementation = AbapSourceCode()
        """Class's local implementation."""

        self.__local_macros = AbapSourceCode()
        """Class's local macros."""

        self.__local_types = AbapSourceCode()
        """Class's Local types."""

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
        """
        Class's name.
        """
        return self.__name

    @property
    def created_by(self):
        """
        User who created the class.
        """
        return self.__author

    @property
    def created_on(self):
        """
        Creation's date.
        """
        return self.__created_on

    @property
    def changed_by(self):
        """
        User who last modified the class.
        """
        return self.__changed_by

    @property
    def changed_on(self):
        """
        Date of the last modification.
        """
        return self.__changed_on

    @property
    def description(self):
        """
        Class's description.
        """
        return self.__description

    @property
    def parent_class(self):
        """
        The direct parent of this class.
        If empty, this class have no parent.
        """
        return self.__parent_class_name

    @property
    def exposure(self):
        """
        Class's constructor exposure.

        Possible values are:
         * '0': Private
         * '1': Protected
         * '2': Public
        """
        return self.__exposure

    @property
    def final(self):
        """
        Flag to indicate this is a final class.
        """
        return self.__final

    @property
    def fixed_point_arithmetic(self):
        """
        Flag to indicate this class uses fixed point arithmetic.
        """
        return self.__fixed_point_arithmetic

    @property
    def attributes(self):
        """
        List of :class:`attribute <.AbapClassAttribute>`.
        """
        return self.__attributes

    @property
    def methods(self):
        """
        List of :class:`methods <.AbapClassMethod>`.
        """
        return self.__methods

    @property
    def original_language(self):
        """
        The 'native' language of the class.
        """
        return self.__original_language

    @property
    def public_section(self):
        """
        The public section (:class:`source code <.AbapSourceCode>`) of the class.
        """
        return self.__public_section

    @property
    def protected_section(self):
        """
        The protected section (:class:`source code <.AbapSourceCode>`) of the class.
        """
        return self.__protected_section

    @property
    def private_section(self):
        """
        The private section (:class:`source code <.AbapSourceCode>`) of the class.
        """
        return self.__private_section

    @property
    def local_implementation(self):
        """
        Class's local implementation.
        """
        return self.__local_implementation

    @property
    def local_macros(self):
        """
        Class's local macros (:class:`source code <.AbapSourceCode>`).
        """
        return self.__local_macros

    @property
    def local_types(self):
        """
        Class's local types (:class:`source code <.AbapSourceCode>`).
        """
        return self.__local_types

    @property
    def text_pool(self):
        return self.__text_pool

    @property
    def unicode(self):
        """
        Flag to indicate this class is unicode compliance.
        """
        return self.__unicode


class AbapClassInterface(AbapClass):
    """
    Representation of an ABAP class interface.
    SAPLink representation is almost like a class, so this is a first
    hackish version for class interface.
    """
    pass

class AbapClassAttribute(AbapObject):
    """
    Atribute of a class.
    """

    def __init__(self,
                 ClassName,
                 AttributeName,
                 AttributeDeclType,
                 AttributeTypType,
                 AttributeExposure,
                 AttributeType,
                 Description):

        super(AbapClassAttribute, self).__init__()
        self.__comp_ref_name = ClassName
        self.__name = AttributeName
        self.__decl_type = AttributeDeclType
        self.__typ_type = AttributeTypType
        self.__exposure = AttributeExposure
        self.__type = AttributeType
        self.__description = Description

    @property
    def name(self):
        """
        Attribute's name.
        """
        return self.__name

    @property
    def decl_type(self):
        """
        Attribute's declaration type.

        Possible values are:
         * '0': Instance attribute
         * '1': Static attribute
         * '2': Constant
        """
        return self.__decl_type

    @property
    def typType(self):
        return self.__typ_type

    @property
    def exposure(self):
        """
        Attribute's exposure.

        Possible values are:
         * '0': Private
         * '1': Protected
         * '2': Public
        """
        return self.__exposure

    @property
    def type(self):
        return self.__type

    @property
    def description(self):
        """
        Attribute's description.
        """
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

        super(AbapClassMethodParameter, self).__init__()
        self.__name = Name
        self.__declaration_type = DeclType
        self.__pass_type = PassType
        self.__typ_type = TypType
        self.__type = Type

    @property
    def name(self):
        """
        Name of method's parameter.
        """
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
        """
        Constructor
        """

        super(AbapClassMethod, self).__init__()
        self.__name = Name
        self.__definition_class_name = DefinitionClassName
        self.__decl_type = DeclType
        self.__exposure = Exposure
        self.__description = Description
        self.__parameters = {}
        self.__source_code = AbapSourceCode()

    @property
    def name(self):
        """
        Method's name.
        """
        return self.__name

    @property
    def definition_class_name(self):
        """
        Class which declared the method (inherited or not).
        """
        return self.__definition_class_name

    @property
    def decl_type(self):
        """
        Declaration type.

        Possible values are:
         * '0': Instance method
         * '1': Static method
        """
        return self.__decl_type

    @property
    def exposure(self):
        """
        Method's exposure.

        Possible values are:
         * '0': Private
         * '1': Protected
         * '2': Public
        """
        return self.__exposure

    @property
    def description(self):
        """
        Method's description.
        """
        return self.__description

    @property
    def parameters(self):
        """
        List of method's parameters.
        """
        return self.__parameters

    @property
    def source_code(self):
        """
        Method's source code.
        """
        return self.__source_code


class AbapInterfaceMethod(AbapClassMethod):
    """Representation of a method declared/inherited from an interface."""
    pass
