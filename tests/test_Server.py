# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Server.py
***********************************

Tests for the :class:`Server` class.

"""

import pytest

from open_api.server import Server
from open_api.server_variable import ServerVariable
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'description': '123'}, None),
    ({'url': 'http://testapi.dev', 'description': '123', 'variables': ServerVariable(name = 'TestVariable', description = '123', default = 'default value')}, None),
])
def test_Server__init__(value, error):
    if not error:
        result = Server(**value)
        assert result is not None
        assert isinstance(result, Server) is True
        assert result.url == value.get('url')
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        if value.get('variables', None):
            assert result.variables is not None
            assert isinstance(result.variables, ManagedList) is True
            for variable in result.variables:
                assert isinstance(variable, ServerVariable) is True
    else:
        with pytest.raises(error):
            result = Server(**value)


@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'description': '123'}, None),
    ({'url': 'http://testapi.dev', 'description': '123', 'variables': ServerVariable(name = 'TestVariable', description = '123', default = 'default value')}, None),
    ({'description': '123'}, None),
])
def test_Server_new_from_dict(value, error):
    if not error:
        url = value.get('url')
        result = Server.new_from_dict(value)
        assert isinstance(result, Server) is True
        assert result.url == url
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        if value.get('variables', None):
            assert result.variables is not None
            assert isinstance(result.variables, ManagedList) is True
            for variable in result.variables:
                assert isinstance(variable, ServerVariable) is True

        if url:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = Server.new_from_dict(value)


@pytest.mark.parametrize('value, updated_value, error', [
    ({'url': 'http://testapi.dev', 'description': '123'}, { 'description': '456' }, None),
    ({'url': 'http://testapi.dev', 'description': '123', 'variables': ServerVariable(name = 'TestVariable', description = '123', default = 'default value')}, { 'description': '456' }, None),
])
def test_Server_update_from_dict(value, updated_value, error):
    if not error:
        result = Server.new_from_dict(value)
        assert isinstance(result, Server) is True
        if value.get('description', None):
            assert result.description is not None
            assert isinstance(result.description, Markup) is True
        result.update_from_dict(updated_value)
        assert result.description != value.get('description', None)
        assert result.description == updated_value.get('description')

        if result.url:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = Server(**value)
