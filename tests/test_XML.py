# -*- coding: utf-8 -*-

"""
***********************************
tests.test_XML.py
***********************************

Tests for the :class:`XML` class.

"""

import pytest

from open_api.schema.XML import XML


@pytest.mark.parametrize('value, error', [
    ({ 'name': 'animal' }, None),
    ({ 'namespace': 'http://example.com/schema/sample', 'prefix': 'sample' }, None),
    ({ 'attribute': True }, None),
    ({ 'wrapped': False }, None)
])
def test_XML__init__(value, error):
    if not error:
        result = XML(**value)
        assert result is not None
        assert isinstance(result, XML) is True
        assert result.name == value.get('name', None)
        assert result.namespace == value.get('namespace', None)
        assert result.prefix == value.get('prefix', None)
        assert result.attribute == value.get('attribute', False)
        assert result.wrapped == value.get('wrapped', False)
    else:
        with pytest.raises(error):
            result = XML(**value)

@pytest.mark.parametrize('value, error', [
    ({ 'name': 'animal' }, None),
    ({ 'namespace': 'http://example.com/schema/sample', 'prefix': 'sample' }, None),
    ({ 'attribute': True }, None),
    ({ 'wrapped': False }, None)
])
def test_XML_new_from_dict(value, error):
    if not error:
        result = XML.new_from_dict(value)
        assert isinstance(result, XML) is True
        assert result.name == value.get('name', None)
        assert result.namespace == value.get('namespace', None)
        assert result.prefix == value.get('prefix', None)
        assert result.attribute == value.get('attribute', False)
        assert result.wrapped == value.get('wrapped', False)
    else:
        with pytest.raises(error):
            result = XML.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({ 'name': 'animal' }, { 'name': 'new_animal' }, None),
    ({ 'namespace': 'http://example.com/schema/sample', 'prefix': 'sample' }, { 'namespace': 'http://newnamespace.com' }, None),
    ({ 'attribute': True }, { 'attribute': False }, None),
    ({ 'wrapped': False }, { 'wrapped': False }, None)
])
def test_XML_update_from_dict(value, updated_value, error):
    result = XML.new_from_dict(value)
    if not error:
        assert isinstance(result, XML) is True
        result.update_from_dict(updated_value)
        if updated_value.get('name'):
            assert result.name != value.get('name', None)
            assert result.name == updated_value.get('name')
        if updated_value.get('namespace'):
            assert result.namespace != value.get('namespace', None)
            assert result.namespace == updated_value.get('namespace')
        if updated_value.get('prefix'):
            assert result.prefix != value.get('prefix', None)
            assert result.prefix == updated_value.get('prefix')
        if updated_value.get('attribute'):
            assert result.attribute != value.get('attribute', False)
            assert result.attribute == updated_value.get('attribute')
        if updated_value.get('wrapped'):
            assert result.wrapped != value.get('wrapped', False)
            assert result.wrapped == updated_value.get('wrapped')
    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
