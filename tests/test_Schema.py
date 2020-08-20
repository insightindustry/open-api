# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Schema.py
***********************************

Tests for the :class:`Schema` class.

"""

import pytest
from validator_collection import checkers

from open_api.schema.Schema import Schema
from open_api.schema.XML import XML
from open_api.schema.Discriminator import Discriminator
from open_api.utility_classes import ExternalDocumentation

NEW_INPUT_DICTIONARY = [
    ({ 'title': 'Test Title' }, None),
    ({ 'type': 'boolean' }, None),
    ({ 'default': 1 }, None),
    ({ 'XML': { 'name': 'valid_name' } }, None),
    ({ 'external_documentation': {'url': 'http://testapi.dev', 'description': 'Test Description'} }, None),
    ({ 'example': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } }, None),
    ({ 'discriminator': { 'property_name': 'petType' } }, None),
    ({ 'all_of': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'any_of': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'one_of': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'not': { 'title': 'Test Title' } }, None),
    ({ 'multiple_of': 2 }, None),
    ({ 'maximum': 2 }, None),
    ({ 'exclusive_maximum': True }, None),
    ({ 'minimum': 1 }, None),
    ({ 'exclusive_minimum': True }, None),
    ({ 'max_length': 5 }, None),
    ({ 'min_length': 2 }, None),
    ({ 'pattern': 'test' }, None),
    ({ 'max_items': 2 }, None),
    ({ 'min_items': 1 }, None),
    ({ 'unique_items': True }, None),
    ({ 'items': { 'title': 'Test Title' } }, None),
    ({ 'max_properties': 2 }, None),
    ({ 'min_properties': 1 }, None),
    ({ 'required': ['test', 'test2'] }, None),
    ({ 'properties': { 'test': { 'title': 'Test Title' } } }, None),
    ({ 'additional_properties': True }, None),
    ({ 'enum': ['test1', 'test2', 'test3'] }, None),
    ({ 'format': 'test' }, None),
    ({ 'nullable': True }, None),
    ({ 'read_only': True }, None),
    ({ 'write_only': True }, None),
    ({ 'deprecated': True }, None),

    ({ 'externalDocs': {'url': 'http://testapi.dev', 'description': 'Test Description'} }, None),
    ({ 'allOf': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'anyOf': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'oneOf': [ { 'title': 'Test Title' }, { 'title': 'Second Test Title' } ] }, None),
    ({ 'multipleOf': 2 }, None),
    ({ 'exclusiveMaximum': True }, None),
    ({ 'exclusiveMinimum': True }, None),
    ({ 'maxLength': 5 }, None),
    ({ 'minLength': 2 }, None),
    ({ 'maxItems': 2 }, None),
    ({ 'minItems': 1 }, None),
    ({ 'uniqueItems': True }, None),

    ({ 'type': 'invalid-type' }, ValueError),
]

UPDATED_INPUT_DICTIONARY = [
    ({ 'title': 'Test Title' }, { 'title': 'New Title' }, None),
    ({ 'type': 'boolean' }, { 'type': 'string' }, None),
    ({ 'default': 1 }, { 'default': 2 }, None),
    ({ 'XML': { 'name': 'valid_name' } }, {'XML': { 'name': 'invalid_name' } }, None),
    ({ 'external_documentation': {'url': 'http://testapi.dev', 'description': 'Test Description'} }, { 'external_documentation': {'url':'http://testapi.com', 'description': 'New Test Description' } }, None),
    ({ 'type': 'string' }, { 'type': 'invalid-type' }, ValueError),
]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Schema__init__(value, error):
    if not error:
        result = Schema(**value)
        assert result is not None
        assert isinstance(result, Schema) is True

        assert result.title == value.get('title', None)
        assert result.type == value.get('type', None)
        assert result.default == value.get('default', None)

        if value.get('XML', None) or value.get('xml', None):
            assert checkers.are_dicts_equivalent(result.XML.to_dict(),
                                                 XML(**value.get('XML', None)).to_dict()) is True

        if value.get('external_documentation', None) or value.get('externalDocs', None):
            external_documentation = value.get('external_documentation', None) or \
                                     value.get('externalDocs', None)
            assert result.external_documentation is not None
            assert checkers.are_dicts_equivalent(result.external_documentation.to_dict(),
                                                 ExternalDocumentation(**external_documentation).to_dict()) is True

        assert result.example == value.get('example', None)
        if value.get('discriminator', None):
            assert checkers.are_dicts_equivalent(result.discriminator.to_dict(),
                                                 Discriminator(**value.get('discriminator',
                                                               None)).to_dict()) is True

        if value.get('all_of', None) or value.get('allOf', None):
            assert len(result.all_of) == len(value.get('all_of', None) or \
                                             value.get('allOf', None))
            for item in result.all_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('any_of', None) or value.get('anyOf', None):
            assert len(result.any_of) == len(value.get('any_of', None) or \
                                             value.get('anyOf', None))
            for item in result.any_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('one_of', None) or value.get('oneOf', None):
            assert len(result.one_of) == len(value.get('one_of', None) or \
                                             value.get('oneOf', None))
            for item in result.one_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('not_', None) or value.get('not', None):
            assert checkers.is_type(result.not_, ['Schema', 'Reference']) is True

        assert result.multiple_of == value.get('multiple_of', 1) or \
                                     value.get('multipleOf', 1)

        assert result.maximum == value.get('maximum', None)
        assert result.exclusive_maximum == value.get('exclusive_maximum', False) or \
                                     value.get('exclusiveMaximum', False)

        assert result.minimum == value.get('minimum', None)
        assert result.exclusive_minimum == value.get('exclusive_minimum', False) or \
                                     value.get('exclusiveMinimum', False)

        assert result.max_length == value.get('max_length', None) or \
                                    value.get('maxLength', None)

        assert result.min_length == value.get('min_length', None) or \
                                    value.get('minLength', None)

        assert result.pattern == value.get('pattern', None)

        assert result.max_items == value.get('max_items', None) or \
                                   value.get('maxItems', None)
        assert result.min_items == value.get('min_items', None) or \
                                   value.get('minItems', None)
        assert result.unique_items == value.get('unique_items', False) or \
                                      value.get('uniqueItems', False)

        if value.get('items', None):
            items_dict = result.items.to_dict()
            for key in value.get('items'):
                assert items_dict[key] == value.get('items')[key]

        assert result.max_properties == value.get('max_properties', None) or \
                                        value.get('maxProperties', None)

        assert result.min_properties == value.get('min_properties', None) or \
                                        value.get('minProperties', None)

        assert checkers.are_equivalent(result.required,
                                       value.get('required', [])) is True

        if value.get('properties', {}):
            for key in result.properties:
                assert key in value.get('properties')
                item_dict = result.properties[key].to_dict()
                value_dict = value.get('properties')[key]
                for value_key in value_dict:
                    assert value_key in item_dict
                    assert item_dict[value_key] == value_dict[value_key]

        if value.get('additional_properties', None) or value.get('additionalProperties', None):
            additional_properties = value.get('additional_properties', None) or value.get('additionalProperties', True)
            if isinstance(additional_properties, bool):
                assert result.additional_properties == additional_properties
            else:
                result_dict = result.additional_properties.to_dict()
                assert checkers.are_dicts_equivalent(result_dict, additional_properties) is True

        assert checkers.are_equivalent(result.enum, value.get('enum', [])) is True

        assert result.format == value.get('format', None)

        assert result.nullable == value.get('nullable', False)

        assert result.read_only == value.get('read_only', False) or \
                                   value.get('readOnly', False)

        assert result.write_only == value.get('write_only', False) or \
                                    value.get('writeOnly', False)

        assert result.deprecated == value.get('deprecated', False)

    else:
        with pytest.raises(error):
            result = Schema(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Schema_new_from_dict(value, error):
    if not error:
        result = Schema(**value)
        assert result is not None
        assert isinstance(result, Schema) is True

        assert result.title == value.get('title', None)
        assert result.type == value.get('type', None)
        assert result.default == value.get('default', None)

        if value.get('XML', None) or value.get('xml', None):
            assert checkers.are_dicts_equivalent(result.XML.to_dict(),
                                                 XML(**value.get('XML', None)).to_dict()) is True

        if value.get('external_documentation', None) or value.get('externalDocs', None):
            external_documentation = value.get('external_documentation', None) or \
                                     value.get('externalDocs', None)
            assert result.external_documentation is not None
            assert checkers.are_dicts_equivalent(result.external_documentation.to_dict(),
                                                 ExternalDocumentation(**external_documentation).to_dict()) is True

        assert result.example == value.get('example', None)
        if value.get('discriminator', None):
            assert checkers.are_dicts_equivalent(result.discriminator.to_dict(),
                                                 Discriminator(**value.get('discriminator',
                                                               None)).to_dict()) is True

        if value.get('all_of', None) or value.get('allOf', None):
            assert len(result.all_of) == len(value.get('all_of', None) or \
                                             value.get('allOf', None))
            for item in result.all_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('any_of', None) or value.get('anyOf', None):
            assert len(result.any_of) == len(value.get('any_of', None) or \
                                             value.get('anyOf', None))
            for item in result.any_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('one_of', None) or value.get('oneOf', None):
            assert len(result.one_of) == len(value.get('one_of', None) or \
                                             value.get('oneOf', None))
            for item in result.one_of:
                assert checkers.is_type(item, ['Schema', 'Reference'])

        if value.get('not_', None) or value.get('not', None):
            assert checkers.is_type(result.not_, ['Schema', 'Reference']) is True

        assert result.multiple_of == value.get('multiple_of', 1) or \
                                     value.get('multipleOf', 1)

        assert result.maximum == value.get('maximum', None)
        assert result.exclusive_maximum == value.get('exclusive_maximum', False) or \
                                     value.get('exclusiveMaximum', False)

        assert result.minimum == value.get('minimum', None)
        assert result.exclusive_minimum == value.get('exclusive_minimum', False) or \
                                     value.get('exclusiveMinimum', False)

        assert result.max_length == value.get('max_length', None) or \
                                    value.get('maxLength', None)

        assert result.min_length == value.get('min_length', None) or \
                                    value.get('minLength', None)

        assert result.pattern == value.get('pattern', None)

        assert result.max_items == value.get('max_items', None) or \
                                   value.get('maxItems', None)
        assert result.min_items == value.get('min_items', None) or \
                                   value.get('minItems', None)
        assert result.unique_items == value.get('unique_items', False) or \
                                      value.get('uniqueItems', False)

        if value.get('items', None):
            items_dict = result.items.to_dict()
            for key in value.get('items'):
                assert items_dict[key] == value.get('items')[key]

        assert result.max_properties == value.get('max_properties', None) or \
                                        value.get('maxProperties', None)

        assert result.min_properties == value.get('min_properties', None) or \
                                        value.get('minProperties', None)

        assert checkers.are_equivalent(result.required,
                                       value.get('required', [])) is True

        if value.get('properties', {}):
            for key in result.properties:
                assert key in value.get('properties')
                item_dict = result.properties[key].to_dict()
                value_dict = value.get('properties')[key]
                for value_key in value_dict:
                    assert value_key in item_dict
                    assert item_dict[value_key] == value_dict[value_key]

        if value.get('additional_properties', None) or value.get('additionalProperties', None):
            additional_properties = value.get('additional_properties', None) or value.get('additionalProperties', True)
            if isinstance(additional_properties, bool):
                assert result.additional_properties == additional_properties
            else:
                result_dict = result.additional_properties.to_dict()
                assert checkers.are_dicts_equivalent(result_dict, additional_properties) is True

        assert checkers.are_equivalent(result.enum, value.get('enum', [])) is True

        assert result.format == value.get('format', None)

        assert result.nullable == value.get('nullable', False)

        assert result.read_only == value.get('read_only', False) or \
                                   value.get('readOnly', False)

        assert result.write_only == value.get('write_only', False) or \
                                    value.get('writeOnly', False)

        assert result.deprecated == value.get('deprecated', False)

    else:
        with pytest.raises(error):
            result = Schema(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_Schema_update_from_dict(value, updated_value, error):
    result = Schema.new_from_dict(value)
    if not error:
        assert isinstance(result, Schema) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
