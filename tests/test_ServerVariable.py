# -*- coding: utf-8 -*-

"""
***********************************
tests.test_ServerVariable.py
***********************************

Tests for the :class:`ServerVariable` class.

"""

import pytest

from open_api.server_variable import ServerVariable
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'name': 'TestVariable', 'description': '123', 'default': 'default value'}, None),
])
def test_ServerVariable__init__(value, error):
    if not error:
        result = ServerVariable(**value)
        assert result is not None
        assert isinstance(result, ServerVariable) is True
        assert result.name == value.get('name')
        assert result.default == value.get('default')
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        if value.get('enum', None):
            assert result.enum is not None
            assert isinstance(result.enum, ManagedList) is True
    else:
        with pytest.raises(error):
            result = ServerVariable(**value)


@pytest.mark.parametrize('value, error', [
    ({'name': 'TestVariable', 'description': '123', 'default': 'default value'}, None),
])
def test_ServerVariable_new_from_dict(value, error):
    if not error:
        result = ServerVariable.new_from_dict(value)
        assert isinstance(result, ServerVariable) is True
        print(value)
        print(value.get('name'))
        assert result.name == value.get('name')
        assert result.default == value.get('default')
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        if value.get('enum', None):
            assert result.enum is not None
            assert isinstance(result.enum, ManagedList) is True
    else:
        with pytest.raises(error):
            result = ServerVariable(**value)


@pytest.mark.parametrize('value, updated_value, error', [
    ({'name': 'TestVariable', 'description': '123', 'default': 'default value'}, {'description': '456'}, None),
])
def test_ServerVariable_update_from_dict(value, updated_value, error):
    if not error:
        result = ServerVariable.new_from_dict(value)
        assert isinstance(result, ServerVariable) is True
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        result.update_from_dict(updated_value)
        assert result.description != value.get('description', None)
        assert result.description == updated_value.get('description')
    else:
        with pytest.raises(error):
            result = ServerVariable(**value)
