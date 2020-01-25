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
        """A :class:`dict <python:dict>` containing the representations for the
        content of the request body.

        The key is the media type or media type range and the value describes
        that using media type's content as a :class:`MediaType` object.

        .. note::

          For requests that match multiple keys, only the most specific key is
          applicable. e.g. ``text/plain`` overrides ``text/*``

        :rtype: :class:`dict <python:dict>` where keys are
          :class:`str <python:str>` and values are :class:`MediaType` /
          :obj:`None <python:None>`
        """
        return self._content

    @content.setter
    def content(self, value):
        content_dict = {}
        value = validators.dict(value, allow_empty = True)
        if not value:
            self._content = None
        else:
            for key in value:
                if not checkers.is_string(key):
                    raise ValueError('content key (%s) must be a string' % key)
                elif checkers.is_dict(value[key]):
                    content_dict[key] = MediaType.new_from_dict(value[key])
                elif checkers.is_type(value[key], 'MediaType'):
                    content_dict[key] = value[key]
                else:
                    raise ValueError('value must be a MediaType or compatible '
                                     'dict. Was: %s' % type(value[key]))

            self._content = content_dict

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
            content_dict = {}
            for key in self.content:
                if not checkers.is_string(key):
                    raise ValueError('content key (%s) must be a string' % key)
                content_dict[key] = self.content[key].to_dict(**kwargs)
            output['content'] = content_dict

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

        if obj:
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
            content = copied_obj.pop('content', None)

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
