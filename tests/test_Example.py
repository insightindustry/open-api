# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Example.py
***********************************

Tests for the :class:`Example` class.

"""

import pytest

from open_api.examples import Example


@pytest.mark.parametrize('value, error', [
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': 'http://www.validdomain.com/' }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': './test.txt' }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': 1.5 }, (ValueError, TypeError)),
])
def test_Example__init__(value, error):
    if not error:
        result = Example(**value)
        assert result is not None
        assert isinstance(result, Example) is True
        assert result.summary == value.get('summary')
        assert result.value == value.get('value', None)
        if value.get('external_value', None):
            assert result.external_value == value.get('external_value')
    else:
        with pytest.raises(error):
            result = Example(**value)

@pytest.mark.parametrize('value, error', [
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': 'http://www.validdomain.com/' }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': './test.txt' }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': 1.5 }, TypeError),
])
def test_Example_new_from_dict(value, error):
    if not error:
        summary = value.get('summary')
        result = Example.new_from_dict(value)
        assert isinstance(result, Example) is True
        assert result.summary == summary
        if value.get('value', None) is not None and value.get('external_value', None) is not None:
            assert result.is_valid is False
        else:
            assert result.is_valid is True
    else:
        with pytest.raises(error):
            result = Example.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True }, {'summary': 'updated summary'}, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True, 'external_value': 'http://www.validdomain.com/' }, {'summary': 'updated summary'}, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True}, {'value': None, 'external_value': './test.txt' }, None),
    ({ 'summary': 'test summary', 'description': 'Test Description', 'value': True}, {'external_value': 1.5}, (ValueError, TypeError)),
])
def test_Example_update_from_dict(value, updated_value, error):
    result = Example.new_from_dict(value)
    if not error:
        assert isinstance(result, Example) is True
        result.update_from_dict(updated_value)
        if updated_value.get('summary'):
            assert result.summary != value.get('summary')
            assert result.summary == updated_value.get('summary')
        if updated_value.get('external_value'):
            assert result.external_value != value.get('external_value', None)
            assert result.external_value == updated_value.get('external_value')

        if result.value is not None and result.external_value is not None:
            assert result.is_valid is False
        else:
            assert result.is_valid is True
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
