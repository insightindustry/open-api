# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Responses.py
***********************************

Tests for the :class:`Responses` class.

"""

import pytest
from validator_collection import checkers

from open_api.paths import PathItem
from open_api.paths.Paths import Paths
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('/pets/mine', { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }) ], None),
    ([ ('/pets/mine', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('/pets/{petId}', { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }) ], None),
    ([ ('/pets/{petId}', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('/pets/{petId}/longer_path', { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }) ], None),
    ([ ('/pets/{petId}/longer_path', Reference.new_from_dict( { 'target': 'test_target' })) ], None),

    ([ ('', Reference.new_from_dict( { 'target': 'test_target' })) ], ValueError),
    ([ ('/pets/{petId}/longer_path', 'invalid-value') ], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ '/pets/mine': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),
    ({ '/pets/mine': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '/pets/{petId}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),
    ({ '/pets/{petId}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '/pets/{petId}/longer_path': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),
    ({ '/pets/{petId}/longer_path': Reference.new_from_dict( { 'target': 'test_target' }) }, None),

    ({ '': Reference.new_from_dict( { 'target': 'test_target' }) }, ValueError),
    ({ '/pets/{petId}/longer_path': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ '/pets/mine': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, { '/pets/mine': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ '/pets/mine': Reference.new_from_dict( { 'target': 'test_target' }) }, { '/pets/mine': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),

    ({ '/pets/{petId}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, { '/pets/{petId}': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ '/pets/{petId}': Reference.new_from_dict( { 'target': 'test_target' }) }, { '/pets/{petId}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),

    ({ '/pets/{petId}/longer_path': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, { '/pets/{petId}/longer_path': Reference.new_from_dict( { 'target': 'test_target' }) }, None),
    ({ '/pets/{petId}/longer_path': Reference.new_from_dict( { 'target': 'test_target' }) }, { '/pets/{petId}/longer_path': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }, None),

    ({ '/pets/{petId}': Reference.new_from_dict( { 'target': 'test_target' }) }, { '/pets/{petId}': 'invalid-value' }, ValueError),

]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Paths__init__(value, error):
    if not error:
        result = Paths(value)
        assert result is not None
        assert isinstance(result, Paths) is True
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
            result = Paths(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Paths_new_from_dict(value, error):
    if not error:
        result = Paths.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Paths) is True
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
            result = Paths.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Paths_update_from_dict(value, updated_value, error):
    result = Paths.new_from_dict(value)
    if not error:
        assert isinstance(result, Paths) is True
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
