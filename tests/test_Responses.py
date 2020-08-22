# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Responses.py
***********************************

Tests for the :class:`Responses` class.

"""

import pytest
from validator_collection import checkers

from open_api.responses import Response, Responses
from open_api.utility_classes import Markup, ManagedList, Reference

NEW_INPUT_VALUES_AS_TUPLES = [
    ([ (200, Response.new_from_dict({ 'description': 'Test Description'})) ], None),
    ([ (201, Reference.new_from_dict( { 'target': 'test_target' } ) )], None),
    ([ (200, Response.new_from_dict({ 'description': 'Test Description'})),
       (201, Reference.new_from_dict( { 'target': 'test_target' } ))], None),
    ([ (200, Response.new_from_dict({ 'description': 'Test Description'})),
       (201, Reference.new_from_dict( { 'target': 'test_target' } )),
       ('default', Reference.new_from_dict( { 'target': 'test_target'} ))], None),

    ([ ('200', Response.new_from_dict({ 'description': 'Test Description'} )) ], None),
    ([ ('201', Reference.new_from_dict( { 'target': 'test_target' } )) ], None),
    ([ ('200', Response.new_from_dict({ 'description': 'Test Description'})),
       ('201', Reference.new_from_dict( { 'target': 'test_target' } ))], None),

    ([ ('invalid-key', Response.new_from_dict({ 'description': 'Test Description'} )) ], ValueError),
    ([ ('200', 'invalid-value' )], ValueError),

]


NEW_INPUT_VALUES_AS_DICT = [
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'} ) }, None),
    ({ 201: Reference.new_from_dict( { 'target': 'test_target' } ) }, None),
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'}),
       201: Reference.new_from_dict( { 'target': 'test_target' } )}, None),
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'}),
       201: Reference.new_from_dict( { 'target': 'test_target' } ),
       'default': Reference.new_from_dict( { 'target': 'test_target'} ) }, None),

    ({ '200': Response.new_from_dict({ 'description': 'Test Description'} ) }, None),
    ({ '201': Reference.new_from_dict( { 'target': 'test_target' } ) }, None),
    ({ '200': Response.new_from_dict({ 'description': 'Test Description'}),
       '201': Reference.new_from_dict( { 'target': 'test_target' } )}, None),

    ({ 'invalid-key': Response.new_from_dict({ 'description': 'Test Description'} ) }, ValueError),
    ({ '200': 'invalid-value' }, ValueError),

]


UPDATED_INPUT_VALUES_AS_DICT = [
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'} ) }, { 200: Reference.new_from_dict({ 'target': 'test_target' }) }, None),
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'}),
       201: Reference.new_from_dict( { 'target': 'test_target' } ),
       'default': Reference.new_from_dict( { 'target': 'test_target'} ) },
     { 'default': Response.new_from_dict({ 'description': 'Test Description'}) }, None),

    ({ 200: Response.new_from_dict({ 'description': 'Test Description'}) }, { 'invalid-key': Response.new_from_dict({ 'description': 'Test Description'} ) }, ValueError),
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'} ) }, { '200': 'invalid-value' }, ValueError),
    ({ 200: Response.new_from_dict({ 'description': 'Test Description'} ) }, 'not a dict', (ValueError, TypeError)),
]


@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_TUPLES)
def test_Responses__init__(value, error):
    if not error:
        result = Responses(value)
        assert result is not None
        assert isinstance(result, Responses) is True
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
            result = Responses(value)

@pytest.mark.parametrize('value, error', NEW_INPUT_VALUES_AS_DICT)
def test_Responses_new_from_dict(value, error):
    if not error:
        result = Responses.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Responses) is True
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
            result = Responses.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_VALUES_AS_DICT)
def test_Response_update_from_dict(value, updated_value, error):
    result = Responses.new_from_dict(value)
    if not error:
        assert isinstance(result, Responses) is True
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
            assert result[key] == updated_dict_value
            if key == 'default':
                assert result.default == updated_dict_value
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
