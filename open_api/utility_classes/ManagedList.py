# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import yaml
from validator_collection import validators, checkers
from validator_collection.errors import MaximumValueError, MinimumValueError
import pypandoc

from open_api.utility_functions import parse_json, parse_yaml

SUPPORTED_FORMATS = [
    'commonmark',
    'rst',
    'gfm'
]

class ManagedList(list):
    """Subclass of :class:`list <python:list> that adds methods for position management.
    """

    def to_indexed(self):
        """Return a version of the object as a :class:`list <python:list>` of
        2-member :class:`tuple <python:tuple>` objects where the first member is the
        item's index and the second member is the item's value.

        :rtype: :class:`list <python:list>` of 2-member :class:`tuple <python:tuple>`
          objects
        """
        output = [(self.index(x), x) for x in self]
        return output

    def move_to(self,
                x,
                target_index,
                start = 0,
                end = None):
        """Moves the item ``x`` to the ``index`` indicated.

        :param x: The item in the :class:`list <python:list>` to be moved. Will select the
          first item in the collection found between ``start`` and ``end``.

        :param target_index: The targeted position in the collection to which ``x`` should
          be moved. Will always be interpreted relative to the whole collection, not a
          slice defined by ``start`` and ``end``.
        :type target_index: :class:`int <python:int>`

        :param start: The starting index at which to begin searching for the first value
          of ``x``. Defaults to ``0``.
        :type start: :class:`int <python:int>`

        :param end: The last index at which to search for the first value of ``x``. If
          :obj:`None <python:None>` will search to the end of the collection. Defaults to
          :obj:`None <python:None>`.
        :type end: :class:`int <python:int>` / :obj:`None <python:None>`

        :raises ValueError: if ``x`` is not found in the collection
        :raises ValueError: if ``target_index`` is not an :class:`int <python:int>`
        :raises IndexError: if ``index`` is out of bounds of the collection
        :raises ValueError: if ``start`` is not an :class:`int <python:int>`
        :raises ValueError: if ``end`` is not an :class:`int <python:int>` and not
          :obj:`None <python:None>`
        :raises MinimumValueError: if ``end`` is less than ``start``
        """
        max_index = max(len(self) - 1, 0)
        start = validators.integer(start, allow_empty = False)
        end = validators.integer(end, allow_empty = True, minimum = start)
        if end is None:
            end = len(self)

        try:
            target_index = validators.integer(target_index,
                                              allow_empty = False,
                                              minimum = 0,
                                              maximum = max_index)
        except (MaximumValueError, MinimumValueError):
            raise IndexError('target_index (%s) out of bounds' % target_index)

        if x not in self:
            raise ValueError('%s not present in collection' % x)

        current_index = self.index(x, start, end)
        if current_index > target_index < len(self):
            target_index = max(target_index, 0)
        self.pop(current_index)
        self.insert(target_index, x)

    def move_earlier(self,
                     x,
                     steps = 1,
                     start = 0,
                     end = None):
        """Moves the item ``x`` to a lower-indexed (earlier) position in the collection.

        :param x: The item in the :class:`list <python:list>` to be moved. Will select the
          first item in the collection found between ``start`` and ``end``.

        :param steps: The number of positions to move the item. Defaults to ``1``.
        :type steps: :class:`int <python:int>`

        :param start: The starting index at which to begin searching for the first value
          of ``x``. Defaults to ``0``.
        :type start: :class:`int <python:int>`

        :param end: The last index at which to search for the first value of ``x``. If
          :obj:`None <python:None>` will search to the end of the collection. Defaults to
          :obj:`None <python:None>`.
        :type end: :class:`int <python:int>` / :obj:`None <python:None>`

        :raises ValueError: if ``x`` is not found in the collection
        :raises ValueError: if ``steps`` is not an :class:`int <python:int>`
        :raises ValueError: if ``start`` is not an :class:`int <python:int>`
        :raises ValueError: if ``end`` is not an :class:`int <python:int>` and not
          :obj:`None <python:None>`
        :raises MinimumValueError: if ``end`` is less than ``start``
        """
        steps = validators.integer(steps, allow_empty = False, minimum = 1)
        if end is not None:
            current_index = self.index(x, start, end)
        else:
            current_index = self.index(x, start)

        target_index = current_index - steps
        self.move_to(x, target_index, start, end)

    def move_later(self,
                   x,
                   steps = 1,
                   start = 0,
                   end = None):
        """Moves the item ``x`` to a higher-indexed (later) position in the collection.

        :param x: The item in the :class:`list <python:list>` to be moved. Will select the
          first item in the collection found between ``start`` and ``end``.

        :param steps: The number of positions to move the item. Defaults to ``1``.
        :type steps: :class:`int <python:int>`

        :param start: The starting index at which to begin searching for the first value
          of ``x``. Defaults to ``0``.
        :type start: :class:`int <python:int>`

        :param end: The last index at which to search for the first value of ``x``. If
          :obj:`None <python:None>` will search to the end of the collection. Defaults to
          :obj:`None <python:None>`.
        :type end: :class:`int <python:int>` / :obj:`None <python:None>`

        :raises ValueError: if ``x`` is not found in the collection
        :raises ValueError: if ``steps`` is not an :class:`int <python:int>`
        :raises ValueError: if ``start`` is not an :class:`int <python:int>`
        :raises ValueError: if ``end`` is not an :class:`int <python:int>` and not
          :obj:`None <python:None>`
        :raises MinimumValueError: if ``end`` is less than ``start``
        """
        steps = validators.integer(steps, allow_empty = False, minimum = 1)
        if end is not None:
            current_index = self.index(x, start, end)
        else:
            current_index = self.index(x, start)

        target_index = current_index + steps
        self.move_to(x, target_index, start, end)

    def to_list(self):
        """Return a :class:`list <python:list>` representation of the object.

        :rtype: :class:`list <python:list>`
        """
        return [x for x in self]
