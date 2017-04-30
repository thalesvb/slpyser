# -*- coding: utf-8 -*-

import logging

from slpyser.model.abap_objects.AbapClassLibrary import AbapClass, AbapClassMethod, \
    AbapClassAttribute, AbapClassMethodParameter, AbapClassInterface
from slpyser.model.abap_objects.AbapTextPool import AbapClassDocumentation
from .AbstractHandler import AbstractHandler


class ClassLibraryHandler(AbstractHandler):

    def __init__(self, owner):
        super(ClassLibraryHandler, self).__init__(owner=owner)
        self.__logger = logging.getLogger(__name__)
        self.__owner = owner

        self.__abap_classes = {}
        self.__current_class = None

    @property
    def parsed_classes(self):
        return self.__abap_classes

    def map_parse(self):
        return {
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
            'INTF': [
                self._startClassInterface,
                None,
                self._endClassInterface
            ],
            'PUBLICSECTION': [
                self._startClassPublicSection,
                self.__owner.charactersSourceCode,
                self._endClassPublicSection
            ],
            'PROTECTEDSECTION': [
                self._startClassProtectedSection,
                self.__owner.charactersSourceCode,
                self._endClassProtectedSection
            ],
            'PRIVATESECTION': [
                self._startClassPrivateSection,
                self.__owner.charactersSourceCode,
                self._endClassPrivateSection
            ],
            'LOCALIMPLEMENTATION': [
                self._startClassLocalImplementation,
                self.__owner.charactersSourceCode,
                self._endClassLocalImplementation
            ],
            'LOCALTYPES': [
                self._startClassLocalTypes,
                self.__owner.charactersSourceCode,
                self._endClassLocalTypes
            ],
            'LOCALMACROS': [
                self._startClassLocalMacros,
                self.__owner.charactersSourceCode,
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
            'EXCEPTION': [
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
        }

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
        self.__owner.set_current_textpool_reference(abapClass.text_pool)

    def _endClass(self, name):
        self.__logger.debug('End class ' + name)
        self.__abap_classes[self.__current_class.name] = self.__current_class
        self.__current_class = None
        #self.__current_text_pool_reference = None
        self.__owner.finalize_textpool()

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

    def _startClassInterface(self, name, attrs):
        self.__logger.debug('Start Class interface')

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

        abapClassInterface = AbapClassInterface(Name=name,
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

        self.__current_class = abapClassInterface
        self.__current_text_pool_reference = abapClassInterface.text_pool

    def _endClassInterface(self, name):
        self.__logger.debug('End class interface')
        self.__abap_classes[self.__current_class.name] = self.__current_class
        self.__current_class = None
        self.__current_text_pool_reference = None

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
        self.__owner.set_current_source_code_reference(classMethod.source_code)

    def _endClassMethod(self, name):
        self.__logger.debug('End class method')
        self.__owner.finalize_source_code()

    def _startClassMethodParameter(self, name, attrs):
        self.__logger.debug('Start class method parameter')
        param_name = attrs.get('SCONAME', '')
        decl_type = attrs.get('PARDECLTYP', '')
        pass_type = attrs.get('PARPASSTYP', '')
        typ_type = attrs.get('TYPTYPE', '')
        type_ = attrs.get('TYPE', '')

        ref_method = attrs.get('CMPNAME')
        ref_class = attrs.get('CLSNAME')

        if name == 'EXCEPTION':
            decl_type = 'EXCP'

        methodParameter = AbapClassMethodParameter(Name=param_name,
                                                   DeclType=decl_type,
                                                   PassType=pass_type,
                                                   TypType=typ_type,
                                                   Type=type_)
        self.__current_class.methods[ref_method].parameters[param_name] = methodParameter

    def _startClassMethodRedefinition(self, name, attrs):
        self.__logger.debug('Start Method Redefinition')

    def _endClassMethodRedefinition(self, name):
        self.__logger.debug('End class method redefinition')

    def _startClassPublicSection(self, name, attrs):
        self.__logger.debug('Start public section')
        self.__owner.set_current_source_code_reference(self.__current_class.public_section)

    def _endClassPublicSection(self, name):
        self.__logger.debug('End class public section')
        self.__owner.finalize_source_code()

    def _startClassProtectedSection(self, name, attrs):
        self.__logger.debug('Start protected section')
        self.__owner.set_current_source_code_reference(self.__current_class.protected_section)

    def _endClassProtectedSection(self, name):
        self.__logger.debug('End class protected section')
        self.__owner.finalize_source_code()

    def _startClassPrivateSection(self, name, attrs):
        self.__logger.debug('Start private section')
        self.__owner.set_current_source_code_reference(self.__current_class.private_section)

    def _endClassPrivateSection(self, name):
        self.__logger.debug('End class private section')
        self.__owner.finalize_source_code()

    def _startClassLocalImplementation(self, name, attrs):
        self.__logger.debug('Start class local implementation')
        self.__owner.set_current_source_code_reference(self.__current_class.local_implementation)

    def _endClassLocalImplementation(self, name):
        self.__logger.debug('End class local implementation')
        self.__owner.finalize_source_code()

    def _startClassLocalTypes(self, name, attrs):
        self.__logger.debug('Start class local types')
        self.__owner.set_current_source_code_reference(self.__current_class.local_types)
        
    def _endClassLocalTypes(self, name):
        self.__logger.debug('End class local types')
        self.__owner.finalize_source_code()

    def _startClassLocalMacros(self, name, attrs):
        self.__logger.debug('Start class local macros')
        self.__owner.set_current_source_code_reference(self.__current_class.local_macros)

    def _endClassLocalMacros(self, name):
        self.__logger.debug('End class local macros')
        self.__owner.finalize_source_code()

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
        self.__owner.set_current_source_code_reference(interfaceMethod.source_code)

    def _endInterfaceMethod(self, name):
        self.__logger.debug('End interface method')
        self.__owner.finalize_source_code()
