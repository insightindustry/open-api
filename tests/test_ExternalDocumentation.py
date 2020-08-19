# -*- coding: utf-8 -*-

"""
***********************************
tests.test_ExternalDocumentation.py
***********************************

Tests for the :class:`Contact` class.

"""

import pytest

from open_api.utility_classes import Markup, ManagedList, ExternalDocumentation


@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'description': 'Test Description'}, None),
    ({'url': 'invalid-url', 'description': 'Test Description'}, ValueError),
])
def test_ExternalDocumentation__init__(value, error):
    if not error:
        result = ExternalDocumentation(**value)
        assert result is not None
        assert isinstance(result, ExternalDocumentation) is True
        assert result.url == value.get('url')
        assert result.description == value.get('description', None)
    else:
        with pytest.raises(error):
            result = ExternalDocumentation(**value)

@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'description': 'Test Description'}, None),
    ({'url': 'invalid-url', 'description': 'Test Description'}, ValueError),
])
def test_ExternalDocumentation_new_from_dict(value, error):
    if not error:
        url = value.get('url')
        description = value.get('description')
        result = ExternalDocumentation.new_from_dict(value)
        assert isinstance(result, ExternalDocumentation) is True
        assert result.url == url
        assert result.description == description
        assert result.is_valid is True
    else:
        with pytest.raises(error):
            result = ExternalDocumentation.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'url': 'http://testapi.dev', 'description': 'Test Description'}, {'description': 'updated description', 'url': 'http://testapi2.dev'}, None),
    ({'url': 'http://testapi.dev', 'description': 'Test Description'}, {'url': 'invalid-url'}, ValueError),
])
def test_ExternalDocumentation_update_from_dict(value, updated_value, error):
    result = ExternalDocumentation.new_from_dict(value)
    if not error:
        assert isinstance(result, ExternalDocumentation) is True
        result.update_from_dict(updated_value)
        if updated_value.get('description'):
            assert result.description != value.get('description')
            assert result.description == updated_value.get('description')
        if updated_value.get('url'):
            assert result.url != value.get('url')
            assert result.url == updated_value.get('url')

        assert result.is_valid is True
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
