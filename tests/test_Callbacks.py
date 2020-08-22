# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Callbacks.py
***********************************

Tests for the :class:`Callbacks` class.

"""

import pytest
from validator_collection import checkers

from open_api.paths import PathItem, Callbacks
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('{$url}', { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }) ], None),
    ([ ('{$url}', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('{$request.query.queryUrl}', { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }) ], None),
    ([ ('{$request.query.queryUrl}', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('{$url}', 'invalid-value') ], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ '{$url}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),
    ({ '{$url}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '{$request.query.queryUrl}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),
    ({ '{$request.query.queryUrl}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ '{$url}': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ '{$url}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, { '{$url}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ '{$url}': Reference.new_from_dict( { 'target': 'test_target' }) }, { '{$url}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),

    ({ '{$request.query.queryUrl}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, { '{$request.query.queryUrl}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ '{$request.query.queryUrl}': Reference.new_from_dict( { 'target': 'test_target' }) }, { '{$request.query.queryUrl}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),

    ({ '{$url}': Reference.new_from_dict( { 'target': 'test_target' }) }, { '{$url}': 'invalid-value' }, ValueError),

]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Callbacks__init__(value, error):
    if not error:
        result = Callbacks(value)
        assert result is not None
        assert isinstance(result, Callbacks) is True
        assert isinstance(result, dict) is True
        assert len(result) == len(value)
        for item in value:
            original_item = item
            key = result._validate_key(item[0])
            assert item[0] in result or str(item[0]) in result
            key = item[0]
            key_value = item[1]
            assert result[key] is not None
            assert result[key] == key_value
    else:
        with pytest.raises(error):
            result = Callbacks(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Callbacks_new_from_dict(value, error):
    if not error:
        result = Callbacks.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Callbacks) is True
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
            result = Callbacks.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Callbacks_update_from_dict(value, updated_value, error):
    result = Callbacks.new_from_dict(value)
    if not error:
        assert isinstance(result, Callbacks) is True
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
