# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.utility_functions import validate_url

class Encoding(OpenAPIObject):
    """A single encoding definition applied to a single schema property."""

    def __init__(self, *args, **kwargs):
        self._content_type = None
        self._headers = None
        self._style = None
        self._explode = None
        self._allow_reserved_characters = False

        super().__init__(*args, **kwargs)

    @property
    def content_type(self):
        """The ``Content-Type`` for encoding a specific property.

        The default value depends on the property type:

        .. list-table::
           :widths: 25 25
           :header-rows: 1

           * - Property Type
             - Default Content Type
           * - string (binary)
             - ``'application/octet-stream'``
           * - object
             - ``'application/json'``
           * - other primitive types
             - ``'text/plan'``
           * - array
             - based on inner type

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        value = validators.string(value, allow_empty = False)

    @property
    def headers(self):
        """A map allowing additional information to be provided as headers, for
        example ``Content-Disposition``.

        .. caution::

          ``Content-Type`` is described using the ``content_type`` property and
          will be ignored if provided in ``headers``.

        .. note::

          This property SHALL be ignored if the request body media type is not a
          ``multipart``.

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
    def style(self):
        """Describes how the header value will be serialized.

        Defaults to ``'form'``.

        .. note::

          This property will be ignored if the request body media type is not
          ``'application/x-www-form-urlencoded'``.

        :rtype: :class:`str <python:str>`
        """
        if not self._style:
            return 'form'

        return self._style

    @style.setter
    def style(self, value):
        value = validators.string(value, allow_empty = True)
        if not value:
            self._style = None
        else:
            value = value.lower().strip()
            if value not in ['matrix',
                             'label',
                             'form',
                             'simple',
                             'spaceDelimited',
                             'pipeDelimited',
                             'deepObject']:
                raise ValueError('value (%s) is not an acceptable style' % value)

            self._style = value

    @property
    def explode(self):
        """If ``True``, received parameter values of type ``array`` or ``object``
        will be divided into separate (new) parameters, where each value of the
        array or key-value pair of the object map becomes a new parameter.

        Assign value of :obj:`None <python:None>` to apply defaults. When
        ``style`` is ``'form'``, will default to ``True``. Otherwise will
        default to ``False``.

        .. note::

          This property will be ignored if the request body media type is not
          ``'application/x-www-form-urlencoded'``.

        :rtype: :class:`bool <python:bool>` / :obj:`None <python:None>`
        """
        if self._explode is None and self.style == 'form':
            return True
        elif self._explode is None:
            return False

        return self._explode

    @explode.setter
    def explode(self, value):
        if value is None:
            self._explode = None
        else:
            self._explode = bool(value)

    @property
    def allow_reserved_characters(self):
        """If ``True``, the parameter value should allow reserved characters as
        per :RFC:`3986` without percent-encoding. Defaults to ``False``.

        .. note::

          This property will be ignored if the request body media type is not
          ``'application/x-www-form-urlencoded'``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._allow_reserved_characters

    @allow_reserved_characters.setter
    def allow_reserved_characters(self, value):
        self._allow_reserved_characters = bool(value)

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'contentType': self.content_type,
            'headers': None,
            'style': self.style,
            'explode': self.explode,
            'allowReserved': self.allow_reserved_characters
        }

        if self.headers:
            headers_dict = {}
            for key in self.headers:
                if not checkers.is_string(key):
                    raise ValueError('headers key (%s) must be a string' % key)
                examples_dict[key] = self.headers[key].to_dict(**kwargs)
            output['headers'] = headers_dict

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Encoding` object from a :class:`dict <python:dict>`.

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

        content_type = copied_obj.pop('content_type', None) or \
                       copied_obj.pop('contentType', None)

        headers = copied_obj.pop('headers', None)
        style = copied_obj.pop('style', None)
        explode = copied_obj.pop('explode', None)
        allow_reserved_characters = copied_obj.pop('allow_reserved_characters', False) or \
                                    copied_obj.pop('allowReserved', False)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(content_type = content_type,
                     headers = headers,
                     style = style,
                     explode = explode,
                     allow_reserved_characters = allow_reserved_characters,
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

        if 'content_type' in copied_obj or 'contentType' in copied_obj:
            self.content_type = copied_obj.pop('content_type', None) or \
                                copied_obj.pop('contentType', None)
        if 'headers' in copied_obj:
            self.headers = copied_obj('headers', None)
        if 'style' in copied_obj:
            self.style = copied_obj.pop('style', None)
        if 'explode' in copied_obj:
            explode = copied_obj.pop('explode', None)
        if 'allow_reserved_characters' in copied_obj or 'allowReserved' in copied_obj:
            self.allow_reserved_characters = copied_obj.pop('allow_reserved_characters', False) or \
                                             copied_obj.pop('allowReserved', False)

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
