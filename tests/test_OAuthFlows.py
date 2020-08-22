# -*- coding: utf-8 -*-

"""
***********************************
tests.test_OAuthFlows.py
***********************************

Tests for the :class:`OAuthFlows` class.

"""

import pytest
from validator_collection import checkers

from open_api.security_schemes import OAuthFlows, OAuthFlow

NEW_INPUT_DICTIONARY = [
    ({ 'implicit': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } }, None),
    ({ 'password': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } }, None),
    ({ 'client_credentials': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } }, None),
    ({ 'authorization_code': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } }, None),

    ({ 'authorization_code': 'invalid value' }, TypeError),

]

UPDATED_INPUT_DICTIONARY = [
    ({ 'implicit': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } },
     { 'implicit': { 'authorizationUrl': 'http://www.google.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } },
     None),

    ({ 'implicit': { 'authorizationUrl': 'http://www.yahoo.com', 'tokenUrl': 'http://www.yahoo.com', 'refreshUrl': 'http://www.yahoo.com', 'scopes': { 'write:pets': 'modify pets in your account'} } }, { 'authorization_code': 'invalid value' }, TypeError),

]

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_OAuthFlows__init__(value, error):
    if not error:
        result = OAuthFlows(**value)
        assert result is not None
        assert isinstance(result, OAuthFlows) is True

        if result.implicit:
            assert checkers.are_dicts_equivalent(result.implicit.to_dict(),
                                                 value.get('implicit', {})) is True
        if result.password:
            assert checkers.are_dicts_equivalent(result.password.to_dict(),
                                                 value.get('password', {})) is True

        if result.authorization_code:
            assert checkers.are_dicts_equivalent(result.authorization_code.to_dict(),
                                                 value.get('authorization_code', {}) or \
                                                 value.get('authorizationCode', {})) is True
        if result.client_credentials:
            assert checkers.are_dicts_equivalent(result.client_credentials.to_dict(),
                                                 value.get('client_credentials', {}) or \
                                                 value.get('clientCredentials', {})) is True

    else:
        with pytest.raises(error):
            result = OAuthFlows(**value)

@pytest.mark.parametrize('value, error', NEW_INPUT_DICTIONARY)
def test_OAuthFlows_new_from_dict(value, error):
    if not error:
        result = OAuthFlows.new_from_dict(value)
        assert result is not None
        assert isinstance(result, OAuthFlows) is True

        if result.implicit:
            assert checkers.are_dicts_equivalent(result.implicit.to_dict(),
                                                 value.get('implicit', {})) is True
        if result.password:
            assert checkers.are_dicts_equivalent(result.password.to_dict(),
                                                 value.get('password', {})) is True

        if result.authorization_code:
            assert checkers.are_dicts_equivalent(result.authorization_code.to_dict(),
                                                 value.get('authorization_code', {}) or \
                                                 value.get('authorizationCode', {})) is True
        if result.client_credentials:
            assert checkers.are_dicts_equivalent(result.client_credentials.to_dict(),
                                                 value.get('client_credentials', {}) or \
                                                 value.get('clientCredentials', {})) is True

    else:
        with pytest.raises(error):
            result = OAuthFlows(**value)

@pytest.mark.parametrize('value, updated_value, error', UPDATED_INPUT_DICTIONARY)
def test_OAuthFlows_update_from_dict(value, updated_value, error):
    result = OAuthFlows.new_from_dict(value)
    if not error:
        assert isinstance(result, OAuthFlows) is True
        result.update_from_dict(updated_value)

    else:
        with pytest.raises(error):
            print(updated_value)
            result.update_from_dict(updated_value)
            print(result.authorization_code)
