# -*- coding: utf-8 -*-

"""
***********************************
tests.test_RequestBody.py
***********************************

Tests for the :class:`RequestBody` class.

"""

import pytest
from validator_collection import checkers

from open_api.paths.RequestBody import RequestBody
from open_api.parameter.Content import Content
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'required': True, 'content': None }, None),
    ({ 'description': 'Test Description',
       'required': True,
       'content': Content.new_from_dict({
           'application/json': Reference.new_from_dict({ 'target': 'test_target' }),
           'text/xhtml': Reference.new_from_dict({ 'target': 'test_target' })
       })
     },
     None),

    ({ 'description': 'Test Description', 'required': True, 'content': 'invalid value' }, TypeError),

]

UPDATED_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'required': True, 'content': None },
     { 'description': 'Updated Description' },
     None),

    ({ 'description': 'Test Description',
       'required': True,
       'content': Content.new_from_dict({
           'application/json': Reference.new_from_dict({ 'target': 'test_target' }),
           'text/xhtml': Reference.new_from_dict({ 'target': 'test_target' })
       })
     },
     { 'description': 'Test Description',
       'required': True,
       'content': 'invalid value'
     },
     TypeError),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_RequestBody__init__(value, error):
    if not error:
        result = RequestBody(**value)
        assert result is not None
        assert isinstance(result, RequestBody) is True

        assert result.description == value.get('description', None)
        assert result.required == value.get('required', False)

        if value.get('content', None):
            assert result.content is not None
            assert result.content == value.get('content')

    else:
        with pytest.raises(error):
            result = RequestBody(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_RequestBody_new_from_dict(value, error):
    if not error:
        result = RequestBody.new_from_dict(value)
        assert result is not None
        assert isinstance(result, RequestBody) is True

        assert result.description == value.get('description', None)
        assert result.required == value.get('required', False)

        if value.get('content', None):
            assert result.content is not None
            assert result.content == value.get('content')

    else:
        with pytest.raises(error):
            result = RequestBody(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_RequestBody_update_from_dict(value, updated_value, error):
    result = RequestBody.new_from_dict(value)
    if not error:
        assert isinstance(result, RequestBody) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
