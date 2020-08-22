# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Components.py
***********************************

Tests for the :class:`Components` class.

"""

import pytest
from validator_collection import checkers

from open_api.components import Components
from open_api.responses import Response
from open_api.parameters import Parameter, Header
from open_api.paths import RequestBody
from open_api.security_schemes import SecurityScheme
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({
        'schemas': { 'foo': { 'title': 'Test Title' } },
        'responses': { 'test': Response.new_from_dict({ 'description': 'Test Description'} ) },
        'parameters': { 'test': Parameter.new_from_dict({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }) },
        'examples': { 'foo': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } },
        'requestBodies': { 'test': RequestBody.new_from_dict({ 'description': 'Test Description'} ) },
        'headers': { 'test': Header.new_from_dict({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }) },
        'securitySchemes': { 'test': SecurityScheme.new_from_dict({ 'description': 'Test Description', 'type_': 'oauth2' }) },
        'links': { 'test': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } },
        'callbacks': { '{$url}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }
    }, None),

    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'invalid name', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, ValueError),
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': 'invalid value', 'request_body': 'test value', 'parameters': {'test': '{$url}'} }, ValueError),
    ({ 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{invalid runtime expression}'} }, ValueError),
]

UPDATED_INPUT_DICTIONARY = [
    ({
        'schemas': { 'foo': { 'title': 'Test Title' } },
        'responses': { 'test': Response.new_from_dict({ 'description': 'Test Description'} ) },
        'parameters': { 'test': Parameter.new_from_dict({ 'name': 'test_name', 'in': 'query', 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }) },
        'examples': { 'foo': { 'summary': 'test summary', 'description': 'Test Description', 'value': True } },
        'requestBodies': { 'test': RequestBody.new_from_dict({ 'description': 'Test Description'} ) },
        'headers': { 'test': Header.new_from_dict({ 'description': 'Test Description', 'required': True, 'deprecated': False, 'allowEmptyValue': False }) },
        'securitySchemes': { 'test': SecurityScheme.new_from_dict({ 'description': 'Test Description', 'type_': 'oauth2' }) },
        'links': { 'test': { 'description': 'Test Description', 'operation_ref': '#/valid/value/here', 'operation_id': 'testName', 'server': {'url': 'http://testapi.dev', 'description': 'Test Server Description'}, 'request_body': 'test value', 'parameters': {'test': '{$url}'} } },
        'callbacks': { '{$url}': { 'summary': 'Test Summary', 'description': 'Test Description', 'get': {'tags': ['test1', 'test2'], 'summary': 'test summary', 'description': 'Test Description', 'operation_id': 'testOperionId' } } }
    }, {'parameters': {'test': Reference.new_from_dict({'target': 'test_target'})}}, None),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Components__init__(value, error):
    if not error:
        print(value)
        result = Components(**value)
        assert result is not None
        assert isinstance(result, Components) is True

        if 'schemas' in value:
            assert result.schemas is not None
            assert checkers.is_type(result.schemas, 'Schemas') is True
        if 'responses' in value:
            assert result.responses is not None
            assert checkers.is_type(result.responses, 'NamedResponses') is True
        if 'parameters' in value:
            assert result.parameters is not None
            assert checkers.is_type(result.parameters, 'Parameters') is True
        if 'examples' in value:
            assert result.examples is not None
            assert checkers.is_type(result.examples, 'Examples') is True
        if 'requestBodies' in value:
            assert result.request_bodies is not None
            assert checkers.is_type(result.request_bodies, 'RequestBodies') is True
        if 'headers' in value:
            assert result.headers is not None
            assert checkers.is_type(result.headers, 'Headers') is True
        if 'securitySchemes' in value:
            assert result.security_schemes is not None
            assert checkers.is_type(result.security_schemes, 'SecuritySchemes') is True
        if 'links' in value:
            assert result.links is not None
            assert checkers.is_type(result.links, 'Links') is True
        if 'callbacks' in value:
            assert result.callbacks is not None
            assert checkers.is_type(result.callbacks, 'Callbacks') is True
    else:
        with pytest.raises(error):
            result = Components(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_Components_new_from_dict(value, error):
    if not error:
        print(value)
        result = Components.new_from_dict(value)
        assert result is not None
        assert isinstance(result, Components) is True

        if 'schemas' in value:
            assert result.schemas is not None
            assert checkers.is_type(result.schemas, 'Schemas') is True
        if 'responses' in value:
            assert result.responses is not None
            assert checkers.is_type(result.responses, 'NamedResponses') is True
        if 'parameters' in value:
            assert result.parameters is not None
            assert checkers.is_type(result.parameters, 'Parameters') is True
        if 'examples' in value:
            assert result.examples is not None
            assert checkers.is_type(result.examples, 'Examples') is True
        if 'requestBodies' in value:
            assert result.request_bodies is not None
            assert checkers.is_type(result.request_bodies, 'RequestBodies') is True
        if 'headers' in value:
            assert result.headers is not None
            assert checkers.is_type(result.headers, 'Headers') is True
        if 'securitySchemes' in value:
            assert result.security_schemes is not None
            assert checkers.is_type(result.security_schemes, 'SecuritySchemes') is True
        if 'links' in value:
            assert result.links is not None
            assert checkers.is_type(result.links, 'Links') is True
        if 'callbacks' in value:
            assert result.callbacks is not None
            assert checkers.is_type(result.callbacks, 'Callbacks') is True

    else:
        with pytest.raises(error):
            result = Components(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_Components_update_from_dict(value, updated_value, error):
    result = Components.new_from_dict(value)
    if not error:
        assert isinstance(result, Components) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
