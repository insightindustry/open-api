# -*- coding: utf-8 -*-

"""
***********************************
tests.test_SecurityScheme.py
***********************************

Tests for the :class:`SecurityScheme` class.

"""

import pytest
from validator_collection import checkers

from open_api.security_scheme.SecurityScheme import SecurityScheme
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'type_': 'oauth2' }, None),

    ({ 'description': 'Test Description', 'type_': 'invalid value' }, ValueError),
]

UPDATED_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'type_': 'oauth2' }, { 'description': 'Test Description', 'type_': 'http' }, None),

    ({ 'description': 'Test Description', 'type_': 'oauth2' }, { 'description': 'Test Description', 'type_': 'invalid value' }, ValueError),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_SecurityScheme__init__(value, error):
    if not error:
        print(value)
        result = SecurityScheme(**value)
        assert result is not None
        assert isinstance(result, SecurityScheme) is True

        assert result.description == value.get('description')
        print(value)
        print(result.type_)
        assert result.type_ == value.get('type_')

    else:
        with pytest.raises(error):
            result = SecurityScheme(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_SecurityScheme_new_from_dict(value, error):
    if not error:
        print(value)
        result = SecurityScheme.new_from_dict(value)
        assert result is not None
        assert isinstance(result, SecurityScheme) is True

        assert result.description == value.get('description')
        assert result.type_ == value.get('type_')

    else:
        with pytest.raises(error):
            result = SecurityScheme(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_SecurityScheme_update_from_dict(value, updated_value, error):
    result = SecurityScheme.new_from_dict(value)
    if not error:
        assert isinstance(result, SecurityScheme) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
