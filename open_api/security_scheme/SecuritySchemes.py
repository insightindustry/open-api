# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict, Reference
from open_api.security_scheme.SecurityScheme import SecurityScheme
from open_api.utility_functions import validate_component_map_key

class SecuritySchemes(OpenAPIDict):
    """A container for generic named :class:`SecurityScheme` instances that can be
    reused across multiple operations.
    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid key for the
        Components > SecuritySchemes map.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of the key.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validate_component_map_key(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`SecurityScheme`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`SecurityScheme` or :class:`Reference` object.
        :rtype: :class:`SecurityScheme` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = SecurityScheme.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a SecurityScheme instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('SecurityScheme', 'Reference')):
            raise ValueError('value must be a SecurityScheme instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
