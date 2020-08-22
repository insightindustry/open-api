# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Content.py
***********************************

Tests for the :class:`Content` class.

"""

import pytest
from validator_collection import checkers

from open_api.parameters import Content
from open_api.schemas import MediaType
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ ('application/json', Reference.new_from_dict({ 'target': 'test_target' }) )], None),

    ([ ('application/json', 'invalid value' )], ValueError),
    ([ ('invalid key', Reference.new_from_dict({ 'target': 'test_target' }) )], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 'application/json': Reference.new_from_dict({ 'target': 'test_target' }) }, None),

    ({ 'application/json': 'invalid value' }, ValueError),
    ({ 'invalid key': Reference.new_from_dict({ 'target': 'test_target' }) }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 'application/json': Reference.new_from_dict({ 'target': 'test_target' }) }, { 'application/json': { 'schema': Reference.new_from_dict({'target': 'test_target'}), 'example': 'test example' } },None),

    ({ 'application/json': Reference.new_from_dict({ 'target': 'test_target' }) }, { 'application/json': 'invalid value' }, ValueError),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Content__init__(value, error):
    if not error:
        result = Content(value)
        assert result is not None
        assert isinstance(result, Content) is True
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
            result = Content(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Content_new_from_dict(value, error):
    if not error:
        result = Content.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Content) is True
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
            result = Content.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Response_update_from_dict(value, updated_value, error):
    result = Content.new_from_dict(value)
    if not error:
        assert isinstance(result, Content) is True
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
            print(key)
            print(repr(original_value))
            print(result[key].to_dict())
            assert result[key] != original_value
            assert result[key] == MediaType.new_from_dict(updated_dict_value)
            if key == 'default':
                assert result.default == updated_dict_value
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
