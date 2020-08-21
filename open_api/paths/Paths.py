# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict
from open_api.utility_functions import validate_url
from open_api.paths.RequestBody import RequestBody
from open_api.paths.Operation import Operation
from open_api.paths.PathItem import PathItem

class Paths(OpenAPIDict):
    """A container for the paths supported by the API. The container
    maps a :class:`PathItem` definition to the specific :term:`path` exposed by
    the API.

    Holds the relative paths to the individual endpoints and their operations.
    The path is appended to the URL from the :class:`Server` Object in order to
    construct the full URL.

    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid path.

        :param key: The key value to validate.
        :type key: Any

        :returns: A valid path string.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        if not key:
            raise ValueError('key must be a valid path. Was: %s' % key)

        key = validate_url(key)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`PathItem`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`PathItem` or :class:`Reference` object.
        :rtype: :class:`PathItem` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = PathItem.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a PathItem instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('PathItem', 'Reference')):
            raise ValueError('value must be a PathItem instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
