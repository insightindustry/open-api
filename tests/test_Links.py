# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Links.py
***********************************

Tests for the :class:`Links` class.

"""

import pytest
from validator_collection import checkers

from open_api.links import Links
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('test', { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }) ], None),
    ([ ('variable_name', Reference.new_from_dict({'target': 'test_target'})) ], None),

    ([ ('invalid key', { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }) ], ValueError),
    ([ (200, { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }) ], TypeError),
    ([ ('test_key', { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{invalid runtime expression}'} } )], ValueError),
]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'test': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, None),
    ({ 'variable_name': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, None),

    ({ 'invalid key': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, ValueError),
    ({ 200: { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, TypeError),
    ({ 'test_key': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{invalid runtime expression}'} } }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'test': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, { 'test': Reference.new_from_dict({'target': 'test_target'}) }, None),

    ({ 'test_key': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } }, { 'test_key': 'invalid value' }, ValueError),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Links__init__(value, error):
    if not error:
        result = Links(value)
        assert result is not None
        assert isinstance(result, Links) is True
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
            if type(result[key]) != type(key_value) and hasattr(type(result[key]), 'new_from_dict'):
                interim_key_value = type(result[key]).new_from_dict(key_value)
                assert result[key] == interim_key_value
            else:
                assert result[key] == key_value
            if key == 'default':
                assert result.default == key_value

    else:
        with pytest.raises(error):
            result = Links(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Links_new_from_dict(value, error):
    if not error:
        result = Links.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Links) is True
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
            if type(result[key]) != type(key_value) and hasattr(type(result[key]), 'new_from_dict'):
                interim_key_value = type(result[key]).new_from_dict(key_value)
                assert result[key] == interim_key_value
            else:
                assert result[key] == key_value
            if key == 'default':
                assert result.default == key_value

    else:
        with pytest.raises(error):
            result = Links.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Links_update_from_dict(value, updated_value, error):
    result = Links.new_from_dict(value)
    if not error:
        assert isinstance(result, Links) is True
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
            assert result[key] != original_value
            assert result[key] == updated_dict_value
            if key == 'default':
                assert result.default == updated_dict_value
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
