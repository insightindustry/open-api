# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes.Extensions import Extensions
from open_api.utility_classes.Example import Example
from open_api.utility_classes.OpenAPIDict import OpenAPIDict

from open_api.utility_functions import validate_url, validate_component_map_key


class Examples(OpenAPIDict):
    """A container for a set of Examples supported by the API. The container
    maps a :class:`Example` definition to a named example in the specification.

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

        key = validate_component_map_key(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`Example`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`Example` or :class:`Reference` object.
        :rtype: :class:`Example` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = Example.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be an Example instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('Example', 'Reference')):
            raise ValueError('value must be an Example instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
