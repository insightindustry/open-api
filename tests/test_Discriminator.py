# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Descriminator.py
***********************************

Tests for the :class:`Discriminator` class.

"""

import pytest

from validator_collection import checkers

from open_api.errors import UnsupportedPropertyError

from open_api.schema.Discriminator import Discriminator
from open_api.utility_classes.Reference import Reference


@pytest.mark.parametrize('value, error', [
    ({ 'property_name': 'petType' }, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': '#/components/schemas/Dog' }}, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': None }}, UnsupportedPropertyError),
])
def test_Discriminator__init__(value, error):
    if not error:
        result = Discriminator(**value)
        assert result is not None
        assert isinstance(result, Discriminator) is True
        assert result.property_name == value.get('property_name', None)
        if value.get('mapping', None):
            stringified_references = {}
            if result.mapping:
                for key in result.mapping:
                    assert isinstance(result.mapping[key], Reference)
                    stringified_references[key] = '#/' + result.mapping[key].explicit_path
                    print(result.mapping[key].explicit_path)

                assert checkers.are_dicts_equivalent(stringified_references, value.get('mapping', {}))
    else:
        with pytest.raises(error):
            result = Discriminator(**value)

@pytest.mark.parametrize('value, error', [
    ({ 'property_name': 'petType' }, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': '#/components/schemas/Dog' } }, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': None } }, UnsupportedPropertyError),

    ({ 'propertyName': 'petType' }, None),
    ({ 'propertyName': 'petType', 'mapping': { 'dog': '#/components/schemas/Dog' } }, None),
    ({ 'propertyName': 'petType', 'mapping': { 'dog': None } }, UnsupportedPropertyError)
])
def test_Discriminator_new_from_dict(value, error):
    if not error:
        result = Discriminator.new_from_dict(value)
        assert isinstance(result, Discriminator) is True
        assert result.property_name == value.get('property_name', None) or value.get('propertyName', None)

        if value.get('mapping', None):
            stringified_references = {}
            if result.mapping:
                for key in result.mapping:
                    assert isinstance(result.mapping[key], Reference)
                    stringified_references[key] = '#/' + result.mapping[key].explicit_path
                    print(result.mapping[key].explicit_path)

                assert checkers.are_dicts_equivalent(stringified_references, value.get('mapping', {}))

    else:
        with pytest.raises(error):
            result = Discriminator.new_from_dict(value)

@pytest.mark.parametrize('value, updated_value, error', [
    ({ 'property_name': 'petType' }, { 'property_name': 'newPetType' }, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': '#/components/schemas/Dog' }}, { 'mapping': { 'dog': '#/components/schemas/Dog', 'cat': '#/components/schemas/Cat' } }, None),
    ({ 'property_name': 'petType', 'mapping': { 'dog': '#/components/schemas/Dog' }}, { 'mapping': { 'dog': None, 'cat': '#/components/schemas/Cat' } }, UnsupportedPropertyError),

    ({ 'propertyName': 'petType' }, { 'property_name': 'newPetType' }, None),
])
def test_Discriminator_update_from_dict(value, updated_value, error):
    result = Discriminator.new_from_dict(value)
    if not error:
        assert isinstance(result, Discriminator) is True
        result.update_from_dict(updated_value)
        if updated_value.get('property_name', None) or updated_value.get('propertyName', None):
            assert result.property_name != value.get('property_name', None) or value.get('propertyName', None)
            assert result.property_name == updated_value.get('property_name', None) or updated_value.get('propertyName', None)
        if updated_value.get('mapping', None):
            assert len(result.mapping) == len(updated_value.get('mapping'))
            for key in updated_value.get('mapping'):
                assert key in result.mapping

    else:
        with pytest.raises(error):
            result.update_from_dict(updated_value)
