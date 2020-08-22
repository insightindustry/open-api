# -*- coding: utf-8 -*-

"""
***********************************
tests.test_MediaType.py
***********************************

Tests for the :class:`MediaType` class.

"""

import pytest
from validator_collection import checkers

from open_api.schemas import MediaType
from open_api.utility_classes import ExternalDocumentation, Reference

NEW_INPUT_DICTIONARY = [
    ({ 'schema': Reference.new_from_dict({'target': 'test_target'}), 'example': 'test example' }, False),

    ({ 'schema': 'invalid-type' }, TypeError),
]

UPDATED_INPUT_DICTIONARY = [
    ({ 'schema': Reference.new_from_dict({'target': 'test_target'}), 'example': 'test example' }, { 'example': 'new test example' }, False),
]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_MediaType__init__(value, error):
    if not error:
        result = MediaType(**value)
        assert result is not None
        assert isinstance(result, MediaType) is True
        assert result.schema is not None
        assert checkers.is_type(result.schema, ('Schema', 'Reference')) is True

    else:
        with pytest.raises(error):
            result = MediaType(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_MediaType_new_from_dict(value, error):
    if not error:
        result = MediaType.new_from_dict(value)
        assert result is not None
        assert isinstance(result, MediaType) is True
        assert result.schema is not None
        assert checkers.is_type(result.schema, ('Schema', 'Reference'))

    else:
        with pytest.raises(error):
            result = MediaType.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_MediaType_update_from_dict(value, updated_value, error):
    result = MediaType.new_from_dict(value)
    if not error:
        assert isinstance(result, MediaType) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
