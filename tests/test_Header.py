# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Header.py
***********************************

Tests for the :class:`Header` class.

"""

import pytest
from validator_collection import checkers

from open_api.parameters import Header, Content
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }, None),
    ({ 'description': 'Test Description',
       'required': True,
       'deprecated': False,
       'allowEmptyValue': False,
       'content': Content.new_from_dict({
           'application/json': Reference.new_from_dict({ 'target': 'test_target' }),
           'text/xhtml': Reference.new_from_dict({ 'target': 'test_target' })
        })}, None),
    ({ 'name': 'test_name', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }, None),

    ({ 'in_': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }, AttributeError),
]

UPDATED_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'description': 'New Test Description' },
     None),

    ({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'name': 'new_test_name' },
     None),

    ({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False },
     { 'in': 'query' },
     AttributeError),
]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Header__init__(value, error):
    if not error:
        result = Header(**value)
        assert result is not None
        assert isinstance(result, Header) is True

        assert result.in_ == 'header'
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
            result = Header(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Header_new_from_dict(value, error):
    if not error:
        print(value)
        result = Header.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Header) is True

        assert result.in_ == 'header'
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
            result = Header(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_Header_update_from_dict(value, updated_value, error):
    result = Header.new_from_dict(value)
    if not error:
        assert isinstance(result, Header) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
