# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.utility_functions import validate_url

class Response(OpenAPIObject):
    """Describes a single response from an API Operation, including design-time,
    static links to operations based on the response."""

    def __init__(self, *args, **kwargs):
        self._headers = None
        self._content = None
        self._links = None

        super().__init__(*args, **kwargs)

    @property
    def headers(self):
        """A map allowing additional information to be returned as headers.

        .. caution::

          ``Content-Type`` will be ignored if provided in ``headers``.

        :rtype: :class:`dict <python:dict>` with :class:`str <python:str>` keys
          and :class:`Header` or :class:`Reference` instance values /
          :obj:`None <python:None>`
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        if not value:
            self._headers = None
        else:
            header_dict = {}
            if not checkers.is_dict(value):
                raise ValueError('value must be a dict, but was: %s' % type(value))
            else:
                for key in value:
                    if not checkers.is_string(key):
                        raise ValueError('key must be string, but was: %s' % type(key))
                    if checkers.is_type(value[key], ('Header', 'Reference')):
                        header_dict[key] = value[key]
                    elif checkers.is_dict(value[key]):
                        try:
                            header_dict[key] = Header.new_from_dict(value[key])
                        except ValueError:
                            try:
                                header_dict[key] = Reference.new_from_dict(value[key])
                            except ValueError:
                                raise ValueError('value expects a Header instance, '
                                                 'Reference instance, or compatible '
                                                 'dict. Was: %s' % type(value[key]))
                self._headers = header_dict

    @property
    def content(self):
        """A :class:`dict <python:dict>` containing the representations for the
        content of the response.

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
                    content_dict[key] = value[]
                else:
                    raise ValueError('value must be a MediaType or compatible '
                                     'dict. Was: %s' % type(value[key]))

            self._content = content_dict

    @property
    def links(self):
        """A map of operations links that can be followed from the response.

        The keys of the map are short names for the link.

        :rtype: :class:`dict <python:dict>` with :class:`str <python:str>` keys
          and :class:`Link` or :class:`Reference` instance values /
          :obj:`None <python:None>`
        """
        return self._links

    @links.setter
    def links(self, value):
        if not value:
            self._links = None
        else:
            links_dict = {}
            if not checkers.is_dict(value):
                raise ValueError('value must be a dict, but was: %s' % type(value))
            else:
                for key in value:
                    if not checkers.is_string(key):
                        raise ValueError('key must be string, but was: %s' % type(key))
                    if checkers.is_type(value[key], ('Link', 'Reference')):
                        links_dict[key] = value[key]
                    elif checkers.is_dict(value[key]):
                        try:
                            links_dict[key] = Link.new_from_dict(value[key])
                        except ValueError:
                            try:
                                links_dict[key] = Reference.new_from_dict(value[key])
                            except ValueError:
                                raise ValueError('value expects a Link instance, '
                                                 'Reference instance, or compatible '
                                                 'dict. Was: %s' % type(value[key]))
                self._links = links_dict


    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'description': self.description,
            'headers': None,
            'content': None,
            'links': None
        }

        if self.headers:
            headers_dict = {}
            for key in self.headers:
                if not checkers.is_string(key):
                    raise ValueError('headers key (%s) must be a string' % key)
                headers_dict[key] = self.headers[key].to_dict(**kwargs)
            output['headers'] = headers_dict

        if self.content:
            content_dict = {}
            for key in self.content:
                if not checkers.is_string(key):
                    raise ValueError('content key (%s) must be a string' % key)
                content_dict[key] = self.content[key].to_dict(**kwargs)

        if self.links:
            links_dict = {}
            for key in self.links:
                if not checkers.is_string(key):
                    raise ValueError('links key (%s) must be a string' % key)
                links_dict[key] = self.links[key].to_dict(**kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Response` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Encoding
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Encoding` object
        :rtype: :class:`Encoding`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        description = copied_obj.pop('description', None)
        headers = copied_obj.pop('headers', None)
        content = copied_obj.pop('content', None)
        links = copied_obj.pop('links', None)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(description = description,
                     headers = headers,
                     content = content,
                     links = links,
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
            self.description = copied_obj.pop('description', None)
        if 'headers' in copied_obj:
            self.headers = copied_obj.pop('headers', None)
        if 'content' in copied_obj:
            self.style = copied_obj.pop('content', None)
        if 'links' in copied_obj:
            self.links = copied_obj.pop('links', None)

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
        if not self.description:
            return False

        return True
