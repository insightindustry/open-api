# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Response.py
***********************************

Tests for the :class:`Response` class.

"""

import pytest

from open_api.responses import Response
from open_api.utility_classes import Markup, ManagedList


@pytest.mark.parametrize('value, error', [
    ({'description': 'Test Description'}, None),
])
def test_Response__init__(value, error):
    if not error:
        result = Response(**value)
        assert result is not None
        assert isinstance(result, Response) is True
        assert result.description == value.get('description')
        assert result.headers == value.get('headers', None)
    else:
        with pytest.raises(error):
            result = Response(**value)

@pytest.mark.parametrize('value, error', [
    ({'description': 'Test Description'}, None),
    ({}, (ValueError, TypeError)),
])
def test_Response_new_from_dict(value, error):
    if not error:
        description = value.get('description')
        result = Response.new_from_dict(value)
        assert isinstance(result, Response) is True
        assert result.description == description
        if description:
            assert result.is_valid is True
        else:
            assert result.is_valid is False
    else:
        with pytest.raises(error):
            result = Response.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'description': 'Test Description'}, {'description': 'Updated Description'}, None),
])
def test_Response_update_from_dict(value, updated_value, error):
    result = Response.new_from_dict(value)
    if not error:
        assert isinstance(result, Response) is True
        result.update_from_dict(updated_value)
        if updated_value.get('description'):
            assert result.description != value.get('description')
            assert result.description == updated_value.get('description')
        if updated_value.get('headers'):
            assert result.headers != value.get('headers')
            assert result.headers == updated_value.get('headers')
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
