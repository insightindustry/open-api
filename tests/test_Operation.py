# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Operation.py
***********************************

Tests for the :class:`Operation` class.

"""

import pytest

from open_api.paths import Operation
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' }, None),
    ({'summary': 'test summary', 'parameters': 'invalid value'}, (ValueError, TypeError)),
    ({'summary': 'test summary', 'operation_id': 'invalid value'}, (ValueError, TypeError)),
])
def test_Operation__init__(value, error):
    if not error:
        result = Operation(**value)
        assert result is not None
        assert isinstance(result, Operation) is True
        assert result.summary == value.get('summary')
        assert result.operation_id == value.get('operation_id', None)
        if value.get('responses', None):
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = Operation(**value)

@pytest.mark.parametrize('value, error', [
    ({'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' }, None),
    ({'summary': 'test summary', 'parameters': 'invalid value'}, (ValueError, TypeError)),
    ({'summary': 'test summary', 'operation_id': 'invalid value'}, (ValueError, TypeError)),
])
def test_Operation_new_from_dict(value, error):
    if not error:
        summary = value.get('summary')
        result = Operation.new_from_dict(value)
        assert isinstance(result, Operation) is True
        assert result.summary == summary
        if value.get('responses', None):
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = Operation.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' }, {'summary': 'updated summary'}, None),
    ({'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' }, {'operation_id': 'new_operation_id'}, None),
    ({'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' }, {'operation_id': 'invalid value'}, ValueError),
])
def test_Operation_update_from_dict(value, updated_value, error):
    result = Operation.new_from_dict(value)
    if not error:
        assert isinstance(result, Operation) is True
        result.update_from_dict(updated_value)
        if updated_value.get('summary'):
            assert result.summary != value.get('summary')
            assert result.summary == updated_value.get('summary')
        if updated_value.get('operation_id'):
            assert result.operation_id != value.get('operation_id')
            assert result.operation_id == updated_value.get('operation_id')

        if value.get('responses', None):
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
