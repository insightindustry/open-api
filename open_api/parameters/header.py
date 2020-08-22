# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.examples import Example
from open_api.utility_functions import validate_url

class Header(OpenAPIObject):
    """Object representation of a :term:`Header` component.

    """

    def __init__(self, *args, **kwargs):
        self._location = None
        self._description = None
        self._required = False
        self._deprecated = False
        self._allow_empty_value = False

        self._style = None
        self._explode = None
        self._allow_reserved_characters = False
        self._schema = None
        self._example = None
        self._examples = None

        self._content = None

        self.allow_empty_value = kwargs.pop('allow_empty_value', None) or \
                                 kwargs.pop('allowEmptyValue', None) or \
                                 False
        self.allow_reserved_characters = kwargs.pop('allow_reserved_characters', None) or \
                                         kwargs.pop('allowReservedCharacters', None) or \
                                         False

        super().__init__(*args, **kwargs)

    @property
    def location(self):
        """The location where the parameter is expected. **REQUIRED**

        .. caution::

          **ALWAYS** returns ``'header'``.

        .. note::

          Aliased by the ``Header.in`` property.

        :rtype: :class:`str <python:str>`
        """
        return 'header'

    @property
    def in_(self):
        """The location where the parameter is expected. **REQUIRED**

        .. caution::

          **ALWAYS** returns ``'header'``.

        .. note::

          Alias for the ``Header.location`` property.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self.location

    @property
    def required(self):
        """Determines whether this parameter is mandatory in API requests.
        Defaults to ``False``.

        .. note::

          If ``location`` is ``'path'``, will always return ``True``.

        :rtype: :class:`bool <python:bool>`
        """
        if self.location == 'path':
            return True

        return self._required

    @required.setter
    def required(self, value):
        self._required = bool(value)

    @property
    def deprecated(self):
        """Indicates that a parameter is deprecated and should be transitioned
        out of usage. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value):
        self._deprecated = bool(value)

    @property
    def allow_empty_value(self):
        """If ``True``, indicates that an empty value may be supplied for the
        parameter.

        .. error:

          Use of this property is **NOT RECOMMENDED**, as it is likely to be
          removed in a later revision.

        .. note::

          Will only be respected for parameters whose ``location`` is ``'query'``.

        :rtype: :class:`bool <python:bool>`
        """
        if self.location == 'query':
            return self._allow_empty_value

        return False

    @allow_empty_value.setter
    def allow_empty_value(self, value):
        self._allow_empty_value = bool(value)

    @property
    def style(self):
        """Describes how the parameter value will be serialized depending on the
        type of the parameter value.

        Default values are determined based on the value of the parameter's
        ``location``:

        .. list-table::
           :widths: 25 25
           :header-rows: 1

           * - ``location``
             - Default ``style``
           * - ``'query'``
             - ``'form'``
           * - ``'path'``
             - ``'simple'``
           * - ``'header'``
             - ``'simple'``
           * - ``'cookie'``
             - ``'form'``

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._style and self.location == 'query':
            return 'form'
        if not self._style and self.location == 'path':
            return 'simple'
        if not self._style and self.location == 'header':
            return 'simple'
        if not self._style and self.location == 'cookie':
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

          If the parameter's ``location`` is not ``'query'``, will always be
          ``True``.

        :rtype: :class:`bool <python:bool>`
        """
        if self.location != 'query':
            return True

        return self._allow_reserved_characters

    @allow_reserved_characters.setter
    def allow_reserved_characters(self, value):
        self._allow_reserved_characters = bool(value)

    @property
    def schema(self):
        """The schema defining the type used for the parameter.

        :rtype: :class:`Schema` / :class:`Reference` / :obj:`None <python:None>`
        """
        return self._schema

    @schema.setter
    def schema(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, ('Schema', 'Reference')):
            value = validators.dict(value, allow_empty = False)
            try:
                value = Schema.new_from_dict(value)
            except ValueError:
                try:
                    value = Reference.new_from_dict(value)
                except ValueError:
                    raise ValueError('Expects a Schema, Reference, or compatible'
                                     ' dict instance. Received: %s' % value)

        self._schema = value


    @property
    def example(self):
        """Example of the media type.

        The example should match the specified ``schema`` and encoding properties
        if present.

        .. note::

          The ``example`` field is mutually exclusive of the ``examples`` field.

        .. note::

          If referencing a ``schema`` which contains an example, the ``example``
          property will override the example provided by the ``schema``.

        To represent examples of media types that cannot naturally be
        represented in JSON or YAML, a string value can contain the example with
        escaping where necessary.

        :rtype: any / :obj:`None <python:None>`
        """
        return self._example

    @example.setter
    def example(self, value):
        self._example = value

    @property
    def examples(self):
        """Examples of the media type.

        The examples should match the specified ``schema`` and encoding properties
        if present.

        .. note::

          The ``examples`` field is mutually exclusive of the ``example`` field.

        .. note::

          If referencing a ``schema`` which contains an example, the ``examples``
          property will override the example provided by the ``schema``.

        :rtype: :class:`Examples <python:Examples>` where keys are :class:`str <python:str>`
          and values are :class:`Example` or :class:`Reference` /
          :obj:`None <python:None>`
        """
        return self._examples

    @examples.setter
    def examples(self, value):
        value = validators.dict(value, allow_empty = True)
        if not value:
            self._examples = None
        elif checkers.is_type(value, 'Examples'):
            self._examples = value
        else:
            self._examples = Examples.new_from_dict(value)

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
            'deprecated': self.deprecated,
            'allowEmptyValue': self.allow_empty_value,
            'style': self.style,
            'explode': self.explode,
            'allowReserved': self.allow_reserved_characters,
            'schema': None,
            'example': self.example,
            'examples': None,
            'content': None
        }
        if self.schema:
            output['schema'] = self.schema.to_dict(**kwargs)

        if self.examples:
            self.examples.to_dict(**kwargs)

        if self.content:
            output['content'] = self.content.to_dict(**kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Header` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Header
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Header` object
        :rtype: :class:`Header`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        description = copied_obj.pop('description', None)
        required = copied_obj.pop('required', False)
        deprecated = copied_obj.pop('deprecated', False)
        allow_empty_value = copied_obj.pop('allow_empty_value', False) or \
                            copied_obj.pop('allowEmptyValue', False)
        style = copied_obj.pop('style', None)
        explode = copied_obj.pop('explode', None)
        allow_reserved_characters = copied_obj.pop('allow_reserved_characters', False) or \
                                    copied_obj.pop('allowReserved', False)
        schema = copied_obj.pop('schema', None)
        example = copied_obj.pop('example', None)
        examples = copied_obj.pop('examples', None)
        content = copied_obj.pop('content', None)

        output = cls(description = description,
                     required = required,
                     deprecated = deprecated,
                     allow_empty_value = allow_empty_value,
                     style = style,
                     explode = explode,
                     allow_reserved_characters = allow_reserved_characters,
                     schema = schema,
                     example = example,
                     examples = examples,
                     content = content)

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

        if 'name' in copied_obj:
            self.name = copied_obj.pop('name')
        if 'location' in copied_obj or 'in' in copied_obj:
            self.location = copied_obj.pop('location', None) or \
                            copied_obj.pop('in', None)
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'required' in copied_obj:
            self.required = copied_obj.pop('required', False)
        if 'deprecated' in copied_obj:
            self.deprecated = copied_obj.pop('deprecated', False)
        if 'allow_empty_value' in copied_obj or 'allowEmptyValue' in copied_obj:
            self.allow_empty_value = copied_obj.pop('allow_empty_value', False) or \
                                     copied_obj.pop('allowEmptyValue', False)
        if 'style' in copied_obj:
            self.style = copied_obj.pop('style', None)

        if 'explode' in copied_obj:
            self.explode = copied_obj.pop('explode', None)

        if 'allow_reserved_characters' in copied_obj or 'allowReserved' in copied_obj:
            self.allow_reserved_characters = copied_obj.pop('allow_reserved_characters', False) or \
                                             copied_obj.pop('allowReserved', False)
        if 'schema' in copied_obj:
            self.schema = copied_obj.pop('schema', None)
        if 'example' in copied_obj:
            self.example = copied_obj.pop('example', None)
        if 'examples' in copied_obj:
            self.examples = copied_obj.pop('examples', None)
        if 'content' in copied_obj:
            self.content = copied_obj.pop('content', None)


    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        is_valid = self.location is not None and \
                   (self.schema is None or self.schema.is_valid)

        if not is_valid:
            return False

        if self.examples:
            for key in self.examples:
                is_valid = self.examples[key].is_valid
                if not is_valid:
                    return False

        if self.content:
            for key in self.content:
                is_valid = self.content[key].is_valid
                if not is_valid:
                    return False

        return is_valid
