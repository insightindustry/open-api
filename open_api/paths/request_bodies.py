# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict
from open_api.paths.request_body import RequestBody
from open_api.utility_functions import validate_component_map_key

class RequestBodies(OpenAPIDict):
    """A container for generic :term:`request bodies <request body>` that can
    be reused across multiple operations.

    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key conforms to the Component
        Map Key regular expression defined in the OpenAPI Specification.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of the key.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validate_component_map_key(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`RequestBody`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`RequestBody` or :class:`Reference` object.
        :rtype: :class:`RequestBody` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = RequestBody.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a RequestBody instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('RequestBody', 'Reference')):
            raise ValueError('value must be a RequestBody instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
