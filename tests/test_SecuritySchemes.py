# -*- coding: utf-8 -*-

"""
***********************************
tests.test_SecuritySchemes.py
***********************************

Tests for the :class:`SecuritySchemes` class.

"""

import pytest
from validator_collection import checkers

from open_api.security_scheme.SecurityScheme import SecurityScheme
from open_api.security_scheme.SecuritySchemes import SecuritySchemes
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('test', SecurityScheme.new_from_dict({ 'description': 'Test Description', 'type_': 'oauth2' })) ], None),
    ([ ('variable_name', Reference.new_from_dict( { 'target': 'test_target' } ) )], None),

    ([ ('invalid key', SecurityScheme.new_from_dict({ 'description': 'Test Description'} )) ], ValueError),
    ([ (200, SecurityScheme.new_from_dict({ 'description': 'Test Description'} )) ], TypeError),
    ([ ('test_key', 'invalid-value' )], ValueError),
]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'test': SecurityScheme.new_from_dict({ 'description': 'Test Description', 'type_': 'oauth2' }) }, None),
    ({ 'variable_name': Reference.new_from_dict( { 'target': 'test_target' } ) }, None),

    ({ 'invalid key': SecurityScheme.new_from_dict({ 'description': 'Test Description'} ) }, ValueError),
    ({ 200: SecurityScheme.new_from_dict({ 'description': 'Test Description'} ) }, TypeError),
    ({ 'test_key': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'test': SecurityScheme.new_from_dict({ 'description': 'Test Description', 'type_': 'oauth2' }) }, { 'test': Reference.new_from_dict({ 'target': 'test_target' }) }, None),

    ({ 'test_key': SecurityScheme.new_from_dict({ 'description': 'Test Description'} ) }, { 'test_key': 'invalid-value' }, ValueError),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_SecuritySchemes__init__(value, error):
    if not error:
        result = SecuritySchemes(value)
        assert result is not None
        assert isinstance(result, SecuritySchemes) is True
        assert isinstance(result, dict) is True
        assert len(result) == len(value)
        for item in value:
            original_item = item
            assert item[0] in result or str(item[0]) in result
            if checkers.is_integer(item[0]):
                key = str(item[0])
            else:
                key = item[0]
            key_value = item[1]
            assert result[key] is not None
            assert result[key] == key_value
            if key == 'default':
                assert result.default == key_value

    else:
        with pytest.raises(error):
            result = SecuritySchemes(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_SecuritySchemes_new_from_dict(value, error):
    if not error:
        result = SecuritySchemes.new_from_dict(value)
        assert result is not None
        assert isinstance(result, SecuritySchemes) is True
        assert isinstance(result, dict) is True
        assert len(result) == len(value)
        for item in value:
            original_item = item
            assert item in result or str(item) in result
            if checkers.is_integer(item):
                key = str(item)
            else:
                key = item
            key_value = value[item]
            assert result[key] is not None
            assert result[key] == key_value
            if key == 'default':
                assert result.default == key_value

    else:
        with pytest.raises(error):
            result = SecuritySchemes.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_SecuritySchemes_update_from_dict(value, updated_value, error):
    result = SecuritySchemes.new_from_dict(value)
    if not error:
        assert isinstance(result, SecuritySchemes) is True
        result.update_from_dict(updated_value)
        assert len(result) == len(value)
        for item in updated_value:
            original_item = item
            assert item in result or str(item) in result
            if checkers.is_integer(item):
                key = str(item)
            else:
                key = item
            original_value = value[original_item]
            updated_dict_value = updated_value[original_item]
            print(key)
            print(repr(original_value))
            print(result[key].to_dict())
            assert result[key] != original_value
            assert result[key] == updated_dict_value
            if key == 'default':
                assert result.default == updated_dict_value
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
