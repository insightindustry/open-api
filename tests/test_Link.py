# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Link.py
***********************************

Tests for the :class:`Link` class.

"""

import pytest
from validator_collection import checkers

from open_api.link.Link import Link

NEW_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, None),

    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'invalid name', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, ValueError),
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': 'invalid value', 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, TypeError),
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{invalid runtime expression}'} }, ValueError),
]

UPDATED_INPUT_DICTIONARY = [
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, {'parameters': {'test': '{$url}', 'test2': '{$url}'}}, None),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Link__init__(value, error):
    if not error:
        print(value)
        result = Link(**value)
        assert result is not None
        assert isinstance(result, Link) is True

        assert result.description == value.get('description')

    else:
        with pytest.raises(error):
            result = Link(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Link_new_from_dict(value, error):
    if not error:
        print(value)
        result = Link.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Link) is True

        assert result.description == value.get('description')

    else:
        with pytest.raises(error):
            result = Link(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_Link_update_from_dict(value, updated_value, error):
    result = Link.new_from_dict(value)
    if not error:
        assert isinstance(result, Link) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
