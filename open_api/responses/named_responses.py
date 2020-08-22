# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict
from open_api.responses.response import Response
from open_api.utility_functions import validate_component_map_key

class NamedResponses(OpenAPIDict):
    """A container for generic named responses that can be reused across multiple
    operations.

    .. seealso::

      :class:`Responses`. The :class:`Namedresponses` class is distinct from the
      :class:`Responses` class, in that :class:`Responses` forces keys to map to
      HTTP status codes, while :class:`NamedResponses` maps values to named keys.

      :class:`NamedResponses` are used in the :class:`Components` section, while
      standard :class:`Responses` are used within :class:`PathItem` instances.

    """

    _HAS_DEFAULT_ATTRIBUTE = False

    def _validate_key(self, key):
        """Internal method that validates that a key is either a valid HTTP
        response code OR the value ``'default'``.

        :param key: The key value to validate.
        :type key: Any

        :returns: A :class:`str <python:str>` representation of an HTTP status
          code, or the value ``'default'``.
        :rtype: :class:`str <python:str>`

        :raises ValueError: if unable to validate

        """
        key = validate_component_map_key(key, allow_empty = False)

        return key

    def _validate_value(self, value):
        """Internal method that validates that a value is a valid :class:`Response`,
        :class:`Reference`, or compatible :class:`dict <python:dict>` object.

        :param value: The value to validate.

        :returns: A :class:`Response` or :class:`Reference` object.
        :rtype: :class:`Response` / :class:`Reference`

        :raises ValueError: if ``value`` is invalid

        """
        if checkers.is_dict(value):
            try:
                value = Response.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be a Response instance, '
                                     'Reference instance, or compatible dict '
                                     'but was: %s' % type(value))
        elif not checkers.is_type(value, ('Response', 'Reference')):
            raise ValueError('value must be a Response instance, '
                             'Reference instance, or compatible dict '
                             'but was: %s' % type(value))

        return value
