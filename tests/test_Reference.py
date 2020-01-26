# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Reference.py
***********************************

Tests for the :class:`Reference` class.

"""

import pytest

from open_api.utility_classes import Markup, ManagedList, Reference


@pytest.mark.parametrize('value, error', [
    ({'target': 'test_target' }, None),
    ({'$ref': 'test_target'}, None),
])
def test_Reference__init__(value, error):
    if not error:
        result = Reference(**value)
        assert result is not None
        assert isinstance(result, Reference) is True
        assert result.target == value.get('target') or value.get('$ref')
    else:
        with pytest.raises(error):
            result = Reference(**value)

@pytest.mark.parametrize('value, error', [
    ({'$ref': 'test_target' }, None),
    ({'target': 'test_target'}, None),
])
def test_Reference_new_from_dict(value, error):
    if not error:
        target = value.get('target') or value.get('$ref')
        result = Reference.new_from_dict(value)
        assert isinstance(result, Reference) is True
        assert result.target == target
    else:
        with pytest.raises(error):
            result = Reference.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({'$ref': 'test_target' }, {'$ref': 'updated_target'}, None),
])
def test_Reference_update_from_dict(value, updated_value, error):
    result = Reference.new_from_dict(value)
    if not error:
        assert isinstance(result, Reference) is True
        result.update_from_dict(updated_value)
        if updated_value.get('$ref'):
            assert result.target != value.get('$ref')
            assert result.target == updated_value.get('$ref')

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
