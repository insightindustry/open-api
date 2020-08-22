# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Responses.py
***********************************

Tests for the :class:`Responses` class.

"""

import pytest
from validator_collection import checkers

from open_api.utility_classes import Reference
from open_api.schemas import Schemas


NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('foo', { 'title': 'Test Title' }) ], None),
    ([ ('bar', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('{not valid}', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('not valid', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('foo', 'invalid-value') ], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'foo': { 'title': 'Test Title' } }, None),
    ({ 'bar': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ '{not valid}': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ 'not valid': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ 'foo': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'foo': { 'title': 'Test Title' } }, { 'foo': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ 'bar': Reference.new_from_dict( { 'target': 'test_target' }) }, { 'bar': { 'title': 'Test Title' } }, None),

    ({ 'foo': Reference.new_from_dict( { 'target': 'test_target' }) }, { 'foo': 'invalid-value' }, ValueError),

]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Schemas__init__(value, error):
    if not error:
        result = Schemas(value)
        assert result is not None
        assert isinstance(result, Schemas) is True
        assert isinstance(result, dict) is True
        assert len(result) == len(value)
        for item in value:
            original_item = item
            assert item[0] in result or str(item[0]) in result
            key = item[0]
            key_value = item[1]
            assert result[key] is not None
            assert result[key] == key_value
    else:
        with pytest.raises(error):
            result = Schemas(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Schemas_new_from_dict(value, error):
    if not error:
        result = Schemas.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Schemas) is True
        assert isinstance(result, dict) is True
        assert len(result) == len(value)
        for item in value:
            original_item = item
            assert item in result or str(item) in result
            key = item
            key_value = result._validate_value(value[item])
            assert result[key] is not None
            assert result[key] == key_value

    else:
        with pytest.raises(error):
            result = Schemas.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Schemas_update_from_dict(value, updated_value, error):
    result = Schemas.new_from_dict(value)
    if not error:
        assert isinstance(result, Schemas) is True
        result.update_from_dict(updated_value)
        assert len(result) == len(value)
        for item in updated_value:
            original_item = item
            assert item in result or str(item) in result
            key = item
            original_value = value[original_item]
            updated_dict_value = result._validate_value(updated_value[original_item])
            assert result[key] != original_value
            assert result[key] == updated_dict_value
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
