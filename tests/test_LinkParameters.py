# -*- coding: utf-8 -*-

"""
***********************************
tests.test_LinkParameters.py
***********************************

Tests for the :class:`LinkParameters` class.

"""

import pytest
from validator_collection import checkers

from open_api.link.LinkParameters import LinkParameters
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('test', 'constant value') ], None),
    ([ ('variable_name', '{$url}') ], None),

    ([ ('invalid key', 'constant value') ], ValueError),
    ([ (200, 'constant value') ], TypeError),
    ([ ('test_key', '{$ invalid runtime expression}' )], ValueError),
]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'test': 'constant value' }, None),
    ({ 'variable_name': '{$url}' }, None),

    ({ 'invalid key': 'constant value' }, ValueError),
    ({ 200: 'constant value' }, TypeError),
    ({ 'test_key': '{$ invalid runtime expression}' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'test': 'constant value' }, { 'test': '{$url}' }, None),

    ({ 'test_key': 'constant value' }, { 'test_key': '{$ invalid runtime expression}' }, ValueError),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_LinkParameters__init__(value, error):
    if not error:
        result = LinkParameters(value)
        assert result is not None
        assert isinstance(result, LinkParameters) is True
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
            result = LinkParameters(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_LinkParameters_new_from_dict(value, error):
    if not error:
        result = LinkParameters.new_from_dict(value)
        assert result is not None
        assert isinstance(result, LinkParameters) is True
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
            result = LinkParameters.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_LinkParameters_update_from_dict(value, updated_value, error):
    result = LinkParameters.new_from_dict(value)
    if not error:
        assert isinstance(result, LinkParameters) is True
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
