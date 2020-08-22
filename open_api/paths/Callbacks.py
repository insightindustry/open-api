# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, OpenAPIDict
from open_api.utility_functions import validate_url, validate_runtime_expression
from open_api.paths.path_item import PathItem

class Callbacks(OpenAPIDict):
    """A container for the :term:`callbacks` supported by the API. The container
    maps a :class:`PathItem` definition to the specific :term:`Runtime Expression`.
    When the Runtime Expression is called on the API, the API then executes the
    operation implied by the callback.

    Each key in the :class:`Callbacks` container represents the
    :term:`Runtime Expression` that elicits the callback, while the value of the
    key must correspond to a :class:`PathItem` (or :class:`Reference` to a
    :class:`PathItem`) that models the opreation of the callback.

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
            raise ValueError('key must be a valid Runtime Expression. Was: %s' % key)

        if key.startswith('{'):
            key = key[1:]
        if key.endswith('}'):
            key = key[:-1]

        key = validate_runtime_expression(key)

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

    def to_dict(self, *args, **kwargs):
        """Output the contents of the object to a :class:`dict <python:dict>` object.

        :returns: :class:`dict <python:dict>` object whose keys conform to the
          Specification Extension pattern defined in the OpenAPI Specification
        :rtype: :class:`dict <python:dict>`

        """
        output = {}
        for key in self:
            value = self[key]
            if hasattr(value, 'to_json'):
                value = value.to_json(*args, **kwargs)

            output[key] = '{%s}' % value

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    def add_to_dict(self, obj, *args, **kwargs):
        """Serialize the collection and add its serialized keys to ``obj``.

        :param obj: The :class:`dict <python:dict>` to which the collection should be
          added.
        :type obj: :class:`dict <python:dict>`

        :returns: ``obj`` extended by serialized key/value pairs from the instance
        :rtype: :class:`dict <python:dict>`

        :raises ValueError: if ``obj`` is not a :class:`dict <python:dict>`
        """
        obj = validators.dict(obj, allow_empty = True)
        if not obj:
            obj = {}

        output = self.to_dict(*args, **kwargs)
        for key in output:
            new_key = '{%s}' % key
            obj[new_key] = output[key]

        return obj
