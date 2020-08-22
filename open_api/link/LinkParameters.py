# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import OpenAPIDict
from open_api.utility_functions import validate_runtime_expression

class LinkParameters(OpenAPIDict):
    """A container for the parameters to be supplied to a :class:`Link` object's
    targeted :class:`Operation`.

    Keys are the parameter names to be used, while values are expected to either
    be literal constants or a :term:`Runtime Expression` wrapped in ``{...}``.

    .. note::

      The parameter name can be qualified using the parameter location
      ``[{in}.]{name}`` for operations that use the same parameter name in
      different locations (e.g. ``path.id``).

    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is a valid key for the
        :class:`Link` ``parameters`` map.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of the key.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validators.variable_name(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is either a literal
        constant or a valid :term:`Runtime Expression` wrapped in ``{...}``.

        :param value: The value to validate.

        :returns: A validated :class:`str <python:str>` value
        :rtype: :class:`str <python:str>`

        :raises ValueError: if ``value`` is invalid

        """
        if not value:
            value = None
        elif checkers.is_string(value) and value.startswith('{') and value.endswith('}'):
            interim_value = value[1:-1]
            interim_value = validate_runtime_expression(interim_value, allow_empty = True)

        return value
