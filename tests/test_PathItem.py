# -*- coding: utf-8 -*-

"""
***********************************
tests.test_PathItem.py
***********************************

Tests for the :class:`PathItem` class.

"""

import pytest

from validator_collection import checkers

from open_api.paths import PathItem
from open_api.utility_classes import ManagedList

NEW_TEST_PARAMETERS = [
    ({ '$ref': '#/components/schemas/ErrorModel' }, None),
    ({ 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }, None),

    ({ 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'summary': 'test summary', 'parameters': 'invalid value'} }, (ValueError, TypeError)),
]

UPDATE_TEST_PARAMETERS = [
    ({ '$ref': '#/components/schemas/ErrorModel' }, { '$ref': '#/components/ErrorModel' }, None),
    ({ 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } }, { 'summary': 'New Test Summary' }, None),
]


@pytest.mark.parametrize('value, error', NEW_TEST_PARAMETERS)
def test_PathItem__init__(value, error):
    if not error:
        result = PathItem(**value)
        assert result is not None
        assert isinstance(result, PathItem) is True
        if value.get('$ref', None):
            assert result.is_reference is True
            assert result.reference is not None
            assert result.reference.target == value.get('$ref')
        else:
            assert result.summary == value.get('summary')
            assert result.get_ is not None
            assert checkers.is_type(result.get_, 'Operation') is True
            assert result.is_valid
    else:
        with pytest.raises(error):
            result = PathItem(**value)

@pytest.mark.parametrize('value, error', NEW_TEST_PARAMETERS)
def test_PathItem_new_from_dict(value, error):
    if not error:
        result = PathItem.new_from_dict(value)
        assert result is not None
        assert isinstance(result, PathItem) is True
        if value.get('$ref', None):
            assert result.is_reference is True
            assert result.reference is not None
            assert result.reference.target == value.get('$ref')
        else:
            assert result.summary == value.get('summary')
            assert result.get_ is not None
            assert checkers.is_type(result.get_, 'Operation') is True
            assert result.is_valid
    else:
        with pytest.raises(error):
            result = PathItem.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', UPDATE_TEST_PARAMETERS)
def test_PathItem_update_from_dict(value, updated_value, error):
    result = PathItem.new_from_dict(value)
    if not error:
        assert isinstance(result, PathItem) is True
        result.update_from_dict(updated_value)
        if updated_value.get('summary', None):
            assert result.summary != value.get('summary')
            assert result.summary == updated_value.get('summary')
        if updated_value.get('$ref', None):
            assert result.is_reference is True
            assert result.reference.target != value.get('$ref')
            assert result.reference.target == updated_value.get('$ref')
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
