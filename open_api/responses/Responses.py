# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict
from open_api.responses.Response import Response

class Responses(OpenAPIDict):
    """A container for the expected responses of an operation. The container
    maps a HTTP response code to the expected response.

    .. info::

      The documentation is not necessarily expected to cover all possible HTTP
      response codes because they may not be known in advance. However,
      documentation is expected to cover a successful operation response and any
      known errors.

    Holds the relative paths to the individual endpoints and their operations.
    The path is appended to the URL from the :class:`Server` Object in order to
    construct the full URL.

    .. tip::

      ``'default'`` may be used as a default response for all HTTP status codes
      not covered explicitly by the specification

    .. caution::

      Must contain at least one response code, and it should be a response code
      for a successful operation.

    """

    _HAS_DEFAULT_ATTRIBUTE = True

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
        if key != 'default' and checkers.is_integer(key):
            key = validators.string(key,
                                    allow_empty = False,
                                    coerce_value = True)
        elif key != 'default':
            raise ValueError(
                'key (%s) must either be "default" or an HTTP status code' % key)

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

    @property
    def default(self):
        """The documentation of responses other than the ones declared for
        specific HTTP response codes. Use this field to cover undeclared
        responses.
        """
        return self.get('default', None)

    @default.setter
    def default(self, value):
        self['default'] = value
