# -*- coding: utf-8 -*-

"""
***********************************
tests.test_SecurityRequirements.py
***********************************

Tests for the :class:`SecurityRequirements` class.

"""

import pytest
from validator_collection import checkers

from open_api.security_scheme.SecurityRequirements import SecurityRequirements
from open_api.security_scheme.SecurityRequirement import SecurityRequirement
from open_api.utility_classes import ManagedList

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('test', SecurityRequirement(['1', '2', '3'])) ], None),
    ([ ('variable_name', ['1', '2', '3']) ], None),

    ([ (200, SecurityRequirement(['1', '2', '3'])) ], TypeError),
    ([ ('test_key', [1, 2, 3] )], TypeError),
]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'test': SecurityRequirement(['1', '2', '3']) }, None),
    ({ 'variable_name': ['1', '2', '3'] }, None),

    ({ 200: SecurityRequirement(['1', '2', '3']) }, TypeError),
    ({ 'test_key': [1, 2, 3] }, TypeError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'test': SecurityRequirement(['1', '2', '3']) }, { 'test': SecurityRequirement(['4', '5', '6']) }, None),

    ({ 'test_key': SecurityRequirement(['1', '2', '3']) }, { 'test_key': [1, 2, 3] }, TypeError),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_SecurityRequirements__init__(value, error):
    if not error:
        result = SecurityRequirements(value)
        assert result is not None
        assert isinstance(result, SecurityRequirements) is True
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
            result = SecurityRequirements(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_SecurityRequirements_new_from_dict(value, error):
    if not error:
        result = SecurityRequirements.new_from_dict(value)
        assert result is not None
        assert isinstance(result, SecurityRequirements) is True
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
            result = SecurityRequirements.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_SecurityRequirements_update_from_dict(value, updated_value, error):
    result = SecurityRequirements.new_from_dict(value)
    if not error:
        assert isinstance(result, SecurityRequirements) is True
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
