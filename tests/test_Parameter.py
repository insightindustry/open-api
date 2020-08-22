# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Parameter.py
***********************************

Tests for the :class:`Parameter` class.

"""

import pytest
from validator_collection import checkers

from open_api.parameters import Parameter, Content
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }, None),

    ({ 'name': 'test_name', 'in': 'invalid in', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }, ValueError),
    ({ 'name': 'test_name',
       'in': 'query',
       'description': 'Test Description',
       'required': True,
       'deprecated': False,
       'allowEmptyValue': False,
       'content': Content.new_from_dict({
           'application/json': Reference.new_from_dict({ 'target': 'test_target' }),
           'text/xhtml': Reference.new_from_dict({ 'target': 'test_target' })
        })}, ValueError),

]

UPDATED_INPUT_DICTIONARY = [
    ({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'name': 'new_test_name' },
     None),

    ({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'in': 'invalid value' },
     ValueError),
    ({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'name': 'test_name',
       'in': 'query',
       'description': 'Test Description',
       'required': True,
       'deprecated': False,
       'allowEmptyValue': False,
       'content': Content.new_from_dict({
           'application/json': Reference.new_from_dict({ 'target': 'test_target' }),
           'text/xhtml': Reference.new_from_dict({ 'target': 'test_target' })
        })}, ValueError),
]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Parameter__init__(value, error):
    if not error:
        result = Parameter(**value)
        assert result is not None
        assert isinstance(result, Parameter) is True

        assert result.name == value.get('name', None)
        assert result.in_ == value.get('in_', None) or value.get('in', None)
        assert result.location == result.in_
        assert result.required == value.get('required', False)
        assert result.allow_empty_value == value.get('allow_empty_value', False) or \
                                           value.get('allowEmptyValue', False)
        assert result.allow_reserved_characters == value.get('allow_reserved_characters', None) or \
                                                   value.get('allowReservedCharacters', True)
        assert result.schema == value.get('schema', None)
        assert result.example == value.get('example', None)

    else:
        with pytest.raises(error):
            result = Parameter(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Parameter_new_from_dict(value, error):
    if not error:
        result = Parameter.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Parameter) is True

        assert result.name == value.get('name', None)
        assert result.in_ == value.get('in_', None) or value.get('in', None)
        assert result.location == result.in_
        assert result.required == value.get('required', False)
        assert result.allow_empty_value == value.get('allow_empty_value', False) or \
                                           value.get('allowEmptyValue', False)
        assert result.allow_reserved_characters == value.get('allow_reserved_characters', None) or \
                                                   value.get('allowReservedCharacters', True)
        assert result.schema == value.get('schema', None)
        assert result.example == value.get('example', None)

    else:
        with pytest.raises(error):
            result = Parameter(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_Parameter_update_from_dict(value, updated_value, error):
    result = Parameter.new_from_dict(value)
    if not error:
        assert isinstance(result, Parameter) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
