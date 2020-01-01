# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Contact.py
***********************************

Tests for the :class:`Contact` class.

"""

import pytest

from open_api.info import Contact
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'invalid-email'}, ValueError),
    ({'url': 'invalid-url', 'name': 'Test Name', 'email': 'contact@domain.dev'}, (ValueError, TypeError)),
])
def test_Contact__init__(value, error):
    if not error:
        result = Contact(**value)
        assert result is not None
        assert isinstance(result, Contact) is True
        assert result.url == value.get('url')
        assert result.name == value.get('name', None)
        assert result.email == value.get('email', None)
    else:
        with pytest.raises(error):
            result = Contact(**value)

@pytest.mark.parametrize('value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'invalid-email'}, ValueError),
    ({'url': 'invalid-url', 'name': 'Test Name', 'email': 'contact@domain.dev'}, (ValueError, TypeError)),
])
def test_Contact_new_from_dict(value, error):
    if not error:
        url = value.get('url')
        name = value.get('name')
        email = value.get('email')
        result = Contact.new_from_dict(value)
        assert isinstance(result, Contact) is True
        assert result.url == url
        assert result.name == name
        assert result.email == email
        assert result.is_valid is True
    else:
        with pytest.raises(error):
            result = Contact.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, {'name': 'Test Name 2'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name'}, {'email': 'contact@domain.dev'}, None),
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, {'email': 'invalid-email'}, ValueError),
    ({'url': 'http://testapi.dev', 'name': 'Test Name', 'email': 'contact@domain.dev'}, {'url': 'invalid-url'}, (ValueError, TypeError)),
])
def test_Contact_update_from_dict(value, updated_value, error):
    result = Contact.new_from_dict(value)
    if not error:
        assert isinstance(result, Contact) is True
        result.update_from_dict(updated_value)
        if updated_value.get('name'):
            assert result.name != value.get('name')
            assert result.name == updated_value.get('name')
        if updated_value.get('email'):
            assert result.email != value.get('email')
            assert result.email == updated_value.get('email')
        if updated_value.get('url'):
            assert result.url != value.get('url')
            assert result.url == updated_value.get('url')

        assert result.is_valid is True
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
