# -*- coding: utf-8 -*-

"""
***********************************
tests.test_OAuthFlow.py
***********************************

Tests for the :class:`OAuthFlow` class.

"""

import pytest
from validator_collection import checkers

from open_api.security_scheme.OAuthFlow import OAuthFlow
from open_api.utility_classes import Reference

NEW_INPUT_DICTIONARY = [
    ({ 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, None),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, None),

    ({ 'authorization_url': 'not a valid url', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, ValueError),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'not a valid url', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, ValueError),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'not a valid url', 'scopes': { 'write:pets': 'modify pets in your account'} }, ValueError),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 123: 'this is a valid description' } }, TypeError),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 123 } }, TypeError),
]

UPDATED_INPUT_DICTIONARY = [
    ({
        'authorizationUrl': 'http://www.yahoo.com',
        'tokenUrl': 'http://www.yahoo.com',
        'refreshUrl': 'http://www.yahoo.com',
        'scopes': { 'write:pets': 'modify pets in your account'}
     }, { 'authorizationUrl': 'http://www.google.com' }, None),
    ({
        'authorization_url': 'http://www.yahoo.com',
        'token_url': 'http://www.yahoo.com',
        'refresh_url': 'http://www.yahoo.com',
        'scopes': { 'write:pets': 'modify pets in your account'}
     }, { 'authorizationUrl': 'http://www.google.com' }, None),

    ({
        'authorizationUrl': 'http://www.yahoo.com',
        'tokenUrl': 'http://www.yahoo.com',
        'refreshUrl': 'http://www.yahoo.com',
        'scopes': { 'write:pets': 'modify pets in your account'} }, { 'authorization_url': 'not a valid url', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, ValueError),
    ({ 'authorization_url': 'http://www.yahoo.com', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, { 'authorization_url': 'not a valid url', 'token_url': 'http://www.yahoo.com', 'refresh_url': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} }, ValueError),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_OAuthFlow__init__(value, error):
    if not error:
        result = OAuthFlow(**value)
        assert result is not None
        assert isinstance(result, OAuthFlow) is True

        assert result.authorization_url == value.get('authorization_url', None) or \
                                           value.get('authorizationUrl', None)
        assert result.token_url == value.get('token_url', None) or \
                                   value.get('tokenUrl', None)
        assert result.refresh_url == value.get('refresh_url', None) or \
                                     value.get('refreshUrl', None)
        if result.scopes:
            assert checkers.are_dicts_equivalent(result.scopes, value.get('scopes', {})) is True

    else:
        with pytest.raises(error):
            result = OAuthFlow(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_OAuthFlow_new_from_dict(value, error):
    if not error:
        result = OAuthFlow.new_from_dict(value)
        assert result is not None
        assert isinstance(result, OAuthFlow) is True

        assert result.authorization_url == value.get('authorization_url', None) or \
                                           value.get('authorizationUrl', None)
        assert result.token_url == value.get('token_url', None) or \
                                   value.get('tokenUrl', None)
        assert result.refresh_url == value.get('refresh_url', None) or \
                                     value.get('refreshUrl', None)
        if result.scopes:
            assert checkers.are_dicts_equivalent(result.scopes, value.get('scopes', {})) is True

    else:
        with pytest.raises(error):
            result = OAuthFlow(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_OAuthFlow_update_from_dict(value, updated_value, error):
    result = OAuthFlow.new_from_dict(value)
    if not error:
        assert isinstance(result, OAuthFlow) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
