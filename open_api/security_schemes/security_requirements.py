# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import OpenAPIDict
from open_api.security_schemes.security_requirement import SecurityRequirement


class SecurityRequirements(OpenAPIDict):
    """A container for generic named :class:`SecurityRequirement` instances that can be
    reused across multiple operations.
    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid key for the
        Components > SecurityRequirements map.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of the key.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validators.string(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`SecurityRequirement`,
        or compatible iterable.

        :param value: The value to validate.
        :param type: :class:`SecurityRequirement` / iterable of
          :class:`str <python:str>` / :class:`str <python:str>`

        :returns: A :class:`SecurityRequirement` or iterable object.
        :rtype: :class:`SecurityRequirement`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_iterable(value) and not isinstance(value, SecurityRequirement):
            try:
                value = SecurityRequirement(value)
            except ValueError:
                raise ValueError('Security Requirement instances can only be '
                                 'composed of strings, but one value was: %s' % type(value))
        elif checkers.is_string(value):
            if not value:
                value = SecurityRequirement()
            else:
                value = SecurityRequirement().append(value)
        elif not isinstance(value, SecurityRequirement):
            raise ValueError('value must be a SecurityRequirement instance, '
                             'iterable of compatible strings, or a single string'
                             ' value, but was: %s' % type(value))

        return value
