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
from open_api.examples.Examples import Examples


NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('foo', { 'summary': 'test summary', 'description': 'Test Description', 'value': True }) ], None),
    ([ ('bar', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('{not valid}', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('not valid', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('foo', 'invalid-value') ], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'foo': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } }, None),
    ({ 'bar': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ '{not valid}': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ 'not valid': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ 'foo': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'foo': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } }, { 'foo': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ 'bar': Reference.new_from_dict( { 'target': 'test_target' }) }, { 'bar': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } }, None),

    ({ 'foo': Reference.new_from_dict( { 'target': 'test_target' }) }, { 'foo': 'invalid-value' }, ValueError),

]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Examples__init__(value, error):
    if not error:
        result = Examples(value)
        assert result is not None
        assert isinstance(result, Examples) is True
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
            result = Examples(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Examples_new_from_dict(value, error):
    if not error:
        result = Examples.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Examples) is True
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
            result = Examples.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Examples_update_from_dict(value, updated_value, error):
    result = Examples.new_from_dict(value)
    if not error:
        assert isinstance(result, Examples) is True
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
