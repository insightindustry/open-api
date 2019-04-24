# -*- coding: utf-8 -*-

"""
***********************************
tests.test_ManagedList.py
***********************************

Tests for the :class:`ManagedList` utility class.

"""

import pytest

from validator_collection import checkers

from open_api.utility_classes import ManagedList

@pytest.mark.parametrize('value', [
    ([1, 2, 3]),
    ([]),
    ((1, 2, 3)),
    ('single item'),
])
def test_ManagedList__init__(value):
    obj = ManagedList(value)
    assert obj is not None
    assert len(obj) == len(value)
    for item in value:
        assert item in obj




@pytest.mark.parametrize('value, expected_result', [
    ([1, 2, 3], [(0, 1), (1, 2), (2, 3)]),
    ([], []),
    ((1, 2, 3), [(0, 1), (1, 2), (2, 3)]),
])
def test_ManagedList_to_indexed(value, expected_result):
    obj = ManagedList(value)
    assert obj is not None
    result = obj.to_indexed()
    assert isinstance(result, list) is True
    assert result == expected_result
    for item in result:
        assert isinstance(item, tuple) is True
        assert len(item) == 2
    for index, item in enumerate(result):
        assert result[index] == expected_result[index]


@pytest.mark.parametrize('value', [
    ([1, 2, 3]),
    ([]),
    ((1, 2, 3)),
    ('single item'),
])
def test_ManagedList_to_list(value):
    obj = ManagedList(value)
    assert obj is not None
    assert len(obj) == len(value)

    result = obj.to_list()
    assert isinstance(result, list) is True
    assert isinstance(result, ManagedList) is False
    for index, item in enumerate(value):
        assert value[index] == result[index]


@pytest.mark.parametrize('items, item, target_index, start, stop, error', [
    ([1, 2, 3], 1, 2, 0, None, None),
    ([1, 2, 3], 2, 1, 0, None, None),
    ([1, 2, 3], 3, 0, 0, None, None),

    ([1, 2, 3, 1, 2, 3], 2, 3, 0, None, None),
    ([1, 2, 3, 2, 3, 4], 2, 3, 3, 4, None),

    ([1, 2, 3], 4, 0, 0, None, ValueError),
    ([1, 2, 3], -1, 0, 0, None, ValueError),
    ([1, 2, 3, 2, 3, 4], 2, 8, 0, None, IndexError),
    ([1, 2, 3], 1, -2, 0, None, IndexError),
])
def test_ManagedList_move_to(items, item, target_index, start, stop, error):
    obj = ManagedList(items)
    if not error:
        if stop is not None:
            original_index = obj.index(item, start, stop)
        else:
            original_index = obj.index(item, start)
        obj.move_to(item, target_index, start, stop)
        if obj.count(item) == 1:
            assert obj.index(item) == target_index
        elif obj.count(item) > 1:
            assert obj.index(item, original_index - 1) == target_index
        if original_index != target_index:
            assert obj[original_index] != item
    else:
        with pytest.raises(error):
            obj.move_to(item, target_index, start, stop)


@pytest.mark.parametrize('items, item, steps, start, stop, expected_index', [
    ([1, 2, 3], 3, 1, 0, None, 1),
    ([1, 2, 3], 3, 2, 0, None, 0),
    ([1, 2, 3], 3, 1, 0, None, 1),

    ([1, 2, 3, 1, 2, 3], 3, 1, 0, None, 1),
    ([1, 2, 3, 2, 3, 4], 3, 1, 3, 5, 3),
    ([1, 2, 3, 2, 3, 4], 3, 2, 3, 5, 2),

])
def test_ManagedList_move_earlier(items, item, steps, start, stop, expected_index):
    obj = ManagedList(items)
    if isinstance(expected_index, int):
        if stop is not None:
            original_index = obj.index(item, start, stop)
        else:
            original_index = obj.index(item, start)
        obj.move_earlier(item, steps = steps, start = start, end = stop)
        if obj.count(item) == 1:
            assert obj.index(item) == original_index - steps
        elif obj.count(item) > 1:
            assert obj.index(item, original_index - steps) == original_index - steps
        if original_index != expected_index:
            assert obj[original_index] != item
    else:
        with pytest.raises(expected_index):
            obj.move_earlier(item, steps = steps, start = start, end = stop)


@pytest.mark.parametrize('items, item, steps, start, stop, expected_index', [
    ([1, 2, 3], 1, 1, 0, None, 1),
    ([1, 2, 3], 1, 2, 0, None, 2),
    ([1, 2, 3], 1, 1, 0, None, 1),

    ([1, 2, 3, 1, 2, 3], 1, 1, 0, None, 1),
    ([1, 2, 3, 1, 3, 4], 1, 1, 3, 5, 1),
    ([1, 2, 3, 2, 1, 4], 1, 1, 3, 5, 5),

])
def test_ManagedList_move_later(items, item, steps, start, stop, expected_index):
    obj = ManagedList(items)
    if isinstance(expected_index, int):
        if stop is not None:
            original_index = obj.index(item, start, stop)
        else:
            original_index = obj.index(item, start)
        obj.move_later(item, steps = steps, start = start, end = stop)
        if obj.count(item) == 1:
            assert obj.index(item) == original_index + steps
        elif obj.count(item) > 1:
            assert obj.index(item, original_index + steps) == original_index + steps
        if original_index != expected_index:
            assert obj[original_index] != item
    else:
        with pytest.raises(expected_index):
            obj.move_later(item, steps = steps, start = start, end = stop)
