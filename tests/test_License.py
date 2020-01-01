# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Contact.py
***********************************

Tests for the :class:`Contact` class.

"""

import pytest

from open_api.info import License
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, None),
    ({'url': 'http://testapi.dev'}, None),
    ({'url': 'invalid-url', 'name': 'Test Name'}, (ValueError, TypeError)),
])
def test_License__init__(value, error):
    if not error:
        result = License(**value)
        assert result is not None
        assert isinstance(result, License) is True
        assert result.url == value.get('url')
        assert result.name == value.get('name', None)
        if result.name:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = License(**value)

@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, None),
    ({'url': 'http://testapi.dev'}, None),
    ({'url': 'invalid-url', 'name': 'Test Name'}, (ValueError, TypeError)),
])
def test_License_new_from_dict(value, error):
    if not error:
        url = value.get('url')
        name = value.get('name')
        result = License.new_from_dict(value)
        assert isinstance(result, License) is True
        assert result.url == url
        assert result.name == name
        if name:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = License.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, {'name': 'Test Name 2'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, {'url': 'invalid-url'}, (ValueError, TypeError)),
])
def test_License_update_from_dict(value, updated_value, error):
    result = License.new_from_dict(value)
    if not error:
        assert isinstance(result, License) is True
        result.update_from_dict(updated_value)
        if updated_value.get('name'):
            assert result.name != value.get('name')
            assert result.name == updated_value.get('name')
        if updated_value.get('url'):
            assert result.url != value.get('url')
            assert result.url == updated_value.get('url')

        if result.name:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
