# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import OpenAPIDict
from open_api.schemas import MediaType

from open_api.utility_functions import validate_url, validate_mimetype


class Content(OpenAPIDict):
    """A container for a set of :class:`MediaType` objects supported by the API. The container
    maps a :class:`MediaType` definition to a MIME type.

    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid MIME type.

        :param key: The key value to validate.
        :type key: Any

        :returns: A valid path string.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        if not key:
            raise ValueError('key must be a valid path. Was: %s' % key)

        key = validate_mimetype(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`MediaType`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`MediaType` or :class:`Reference` object.
        :rtype: :class:`MediaType` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = MediaType.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a MediaType instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('MediaType', 'Reference')):
            raise ValueError('value must be an MediaType instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
