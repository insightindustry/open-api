# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, OpenAPIDict, Reference
from open_api.link.Link import Link
from open_api.utility_functions import validate_component_map_key
from open_api.errors import InvalidRuntimeExpressionError

class Links(OpenAPIDict):
    """A container for generic named :class:`Link` instances that can be
    reused across multiple operations.
    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid key for the
        Components > Links map.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of the key.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validate_component_map_key(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`Link`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`Link` or :class:`Reference` object.
        :rtype: :class:`Link` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = Link.new_from_dict(value)
            except InvalidRuntimeExpressionError as error:
                raise error
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a Link instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('Link', 'Reference')):
            raise ValueError('value must be a Link instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
