# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.schema.Schema import Schema
from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject, Example, Examples
from open_api.utility_functions import validate_url

class MediaType(OpenAPIObject):
    """Provides schema and examples for the media type identified by its key."""

    def __init__(self, *args, **kwargs):
        self._schema = None
        self._example = None
        self._examples = None
        self._encoding = None

        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def schema(self):
        """The schema defining the content of the request, response, or parameter.

        :rtype: :class:`Schema` / :class:`Reference` / :obj:`None <python:None>`
        """
        return self._schema

    @schema.setter
    def schema(self, value):
        if not value:
            self._schema = None
        else:
            if not checkers.is_type(value, ('Schema', 'Reference')):
                value = validators.dict(value, allow_empty = False)
                try:
                    value = Schema.new_from_dict(value)
                except ValueError:
                    try:
                        value = Reference.new_from_dict(value)
                    except ValueError:
                        raise ValueError('Expects a Schema, Reference, or '
                                         'compatible dict object. Received: %s' % type(value))

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

        :rtype: :class:`dict <python:dict>` where keys are :class:`str <python:str>`
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
    def encoding(self):
        """A :class:`dict <python:dict>` mapping a property to its encoding
        information.

        Keys are the names of properties which are expected to exist in the
        ``schema``. Values are expected to be :class:`Encoding` instances.

        :rtype: :class:`dict <python:dict>` with :class:`str <python:str>` keys
          and :class:`Encoding` values / :obj:`None <python:None>`
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        if not value:
            self._encoding = None
        else:
            encoding_dict = {}
            if checkers.is_dict(value):
                for key in value:
                    if not checkers.is_string(key):
                        raise ValueError('encoding key (%s) must be a string' % key)
                    elif checkers.is_dict(value[key]):
                        encoding_dict[key] = Encoding.new_from_dict(value[key])
                    elif checkers.is_type(value[key], 'Encoding'):
                        encoding_dict[key] = value[key]
                    else:
                        raise ValueError('value must be an Encoding instance or '
                                         'compatible dict. Was: %s' % type(value[key]))

                self._encoding = encoding_dict

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'schema': None,
            'example': self.example,
            'examples': None,
            'encoding': None
        }
        if self.schema:
            output['schema'] = self.schema.to_dict(**kwargs)

        if self.examples:
            examples_dict = {}
            for key in self.examples:
                if not checkers.is_string(key):
                    raise ValueError('examples key (%s) must be a string' % key)
                examples_dict[key] = self.examples[key].to_dict(**kwargs)
            output['examples'] = examples_dict

        if self.encoding:
            encoding_dict = {}
            for key in self.encoding:
                if not checkers.is_string(key):
                    raise ValueError('encoding key (%s) must be a string' % key)
                encoding_dict[key] = self.encoding[key].to_dict(**kwargs)

            output['encoding'] = encoding_dict

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Parameter` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the :class:`MediaType`
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Parameter` object
        :rtype: :class:`Parameter`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        schema = copied_obj.pop('schema', None)
        example = copied_obj.pop('example', None)
        examples = copied_obj.pop('examples', None)
        encoding = copied_obj.pop('encoding', None)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None


        output = cls(schema = schema,
                     example = example,
                     examples = examples,
                     encoding = encoding,
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

        if 'schema' in copied_obj:
            self.schema = copied_obj.pop('schema', None)
        if 'example' in copied_obj:
            self.example = copied_obj.pop('example', None)
        if 'examples' in copied_obj:
            self.examples = copied_obj.pop('examples', None)
        if 'encoding' in copied_obj:
            self.encoding = copied_obj.pop('encoding', None)

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
