# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.utility_functions import validate_url

class RequestBody(OpenAPIObject):
    """Object representation of a single request body used in making a request
    against the API.

    """

    def __init__(self, *args, **kwargs):
        self._required = False
        self._content = None

        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def required(self):
        """Determines whether this parameter is mandatory in API requests.
        Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._required

    @required.setter
    def required(self, value):
        self._required = bool(value)

    @property
    def content(self):
        """A :class:`Content` object (which is a subclass of
        :class:`dict <python:dict>`) containing the representations for the
        parameter.

        The key is the media type and the value describes it using either a
        :class:`str <python:str>` or :class:`MediaType` object.

        :rtype: :class:`Content <python:Content>` where keys are
          :class:`str <python:str>` and values are :class:`MediaType` /
          :obj:`None <python:None>`

        """
        return self._content

    @content.setter
    def content(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'Content'):
            value = validators.dict(value, allow_empty = False)
            value = Content.new_from_dict(value)

        self._content = value

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'description': self.description,
            'required': self.required,
            'content': None
        }
        if self.content:
            output['content'] = self.content.to_dict()

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`RequestBody` object from a
        :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Request Body
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`RequestBody` object
        :rtype: :class:`RequestBody`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        description = copied_obj.pop('description', None)
        required = copied_obj.pop('required', False)
        content = copied_obj.pop('content', None)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(description = description,
                     required = required,
                     content = content,
                     extensions = extensions)

        return output

    def update_from_dict(self, input_data):
        """Update the object representation based on the input data provided.

        :param input_data: Collection of extension keys to update on the object
          representation.
        :type input_data: :class:`dict <python:dict>`

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        input_data = validators.dict(input_data, allow_empty = True)
        copied_obj = {}
        for key in input_data:
            copied_obj[key] = input_data[key]

        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'required' in copied_obj:
            self.required = copied_obj.pop('required', False)
        if 'content' in copied_obj:
            self.content = copied_obj.pop('content', None)

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
        return self.content is not None
