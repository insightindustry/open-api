# -*- coding: utf-8 -*-

"""
***********************************
tests.test_SecurityRequirement.py
***********************************

Tests for the :class:`SecurityRequirement` utility class.

"""

import pytest

from validator_collection import checkers

from open_api.security_scheme.SecurityRequirement import SecurityRequirement

@pytest.mark.parametrize('value, error', [
    (['1', '2', '3'], None),
    ('single item', None),
    ([], None),

    ([1, 2, 3], TypeError),
    ((1, 2, 3), TypeError),
])
def test_SecurityRequirement__init__(value, error):
    if not error:
        obj = SecurityRequirement(value)
        assert obj is not None
        assert len(obj) == len(value)
        for item in value:
            assert item in obj
    else:
        with pytest.raises(error):
            obj = SecurityRequirement(value)

@pytest.mark.parametrize('value, error', [
    ('4', None),
    ('single item', None),

    ('', ValueError),
    (1, TypeError),
    (None, ValueError),
])
def test_SecurityRequirement_append(value, error):
    obj = SecurityRequirement(['1', '2', '3'])
    assert obj is not None
    assert len(obj) == 3
    if not error:
        obj.append(value)
        assert len(obj) == 4
        assert value in obj
    else:
        with pytest.raises(error):
            obj.append(value)


@pytest.mark.parametrize('value, error', [
    (['4'], None),
    (['single item'], None),

    ([''], ValueError),
    ([1], TypeError),
    ([None], ValueError),
])
def test_SecurityRequirement_extend(value, error):
    obj = SecurityRequirement(['1', '2', '3'])
    assert obj is not None
    assert len(obj) == 3
    if not error:
        obj.extend(value)
        assert len(obj) == 3 + len(value)
        for item in value:
            assert item in obj
    else:
        with pytest.raises(error):
            obj.extend(value)

@pytest.mark.parametrize('value, error', [
    ('4', None),
    ('single item', None),

    ('', ValueError),
    (1, TypeError),
    (None, ValueError),
])
def test_SecurityRequirement_insert(value, error):
    obj = SecurityRequirement(['1', '2', '3'])
    assert obj is not None
    assert len(obj) == 3
    if not error:
        obj.insert(1, value)
        assert len(obj) == 4
        assert value in obj
        assert obj[1] == value
    else:
        with pytest.raises(error):
            obj.insert(1, value)
