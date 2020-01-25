# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes.ManagedList import ManagedList
from open_api.utility_classes.OpenAPIObject import OpenAPIObject

class Example(OpenAPIObject):
    """Object representation of an Example of a request or response from the API."""

    def __init__(self, *args, **kwargs):
        self._summary = None
        self._value = None
        self._external_value = None
        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def summary(self):
        """Short description for the example.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = validators.string(value, allow_empty = True)

    @property
    def value(self):
        """Embedded literal example.

        .. tip::

          To represent examples of media types that cannot naturally represented
          in JSON or YAML, use a string value to contain the example, escaping
          where necessary.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = validators.string(value, allow_empty = True)


    @property
    def external_value(self):
        """URL or path that points to a literal example contained in a separate
        location/file.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._external_value

    @external_value.setter
    def external_value(self, value):
        try:
            self._external_value = validators.path(value, allow_empty = True)
        except ValueError:
            self._external_value = validators.url(value,
                                                  allow_empty = True,
                                                  allow_special_ips = True)

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>`
        """
        output = {
            'summary': self.summary,
            'description': self.description,
            'value': self.value,
            'externalValue': self.external_value
        }
        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Example` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` representation of the Example.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Example` object
        :rtype: :class:`Example`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        summary = copied_obj.pop('summary', None)
        description = copied_obj.pop('description', None)
        value = copied_obj.pop('value', None)
        external_value = copied_obj.pop('external_value', None) or \
                         copied_obj.pop('externalValue', None)

        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(summary = summary,
                     description = description,
                     value = value,
                     external_value = external_value,
                     extensions = extensions)

        return output

    def update_from_dict(self, input_data):
        """Update the object representation based on the input data provided.

        :param input_data: Collection of properties to update on the object.
        :type input_data: :class:`dict <python:dict>`

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        input_data = validators.dict(input_data, allow_empty = True)
        copied_obj = {}
        for key in input_data:
            copied_obj[key] = input_data[key]

        if 'summary' in copied_obj:
            self.summary = copied_obj.pop('summary')
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'value' in copied_obj:
            self.value = copied_obj.pop('value')
        if 'external_value' in copied_obj or 'externalValue' in copied_obj:
            self.external_value = copied_obj.pop('external_value') or \
                                  copied_obj.pop('externalValue')

        if copied_obj and self.extensions:
            self.extensions.update_from_dict(copied_obj)
        elif copied_obj:
            self.extensions = copied_obj

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        return True
