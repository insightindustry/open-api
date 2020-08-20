# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.schema.XML import XML
from open_api.schema.Discriminator import Discriminator
from open_api.utility_classes import Extensions, ManagedList, ExternalDocumentation, Reference, OpenAPIObject
from open_api.utility_functions import validate_url

SUPPORTED_TYPES = ('null',
                   'boolean',
                   'object',
                   'array',
                   'number',
                   'string',
                   'integer')

class Schema(OpenAPIObject):
    """The Schema Object allows the definition of input and output data types.

    These types can be objects, but also primitives and arrays. This object is
    an extended subset of the
    `JSON Schema Specification Wright Draft 00 <http://json-schema.org/>`_.

    """

    def __init__(self, *args, **kwargs):
        self._title = None
        self._type = None
        self._default = None

        self._XML = None

        self._external_documentation = None
        self._example = None

        self._discriminator = None

        self._all_of = []
        self._one_of = []
        self._any_of = []

        self._multiple_of = 1
        self._maximum = None
        self._exclusive_maximum = False
        self._minimum = None
        self._exclusive_minimum = False

        self._max_length = None
        self._min_length = None
        self._pattern = None

        self._max_items = None
        self._min_items = None
        self._unique_items = False
        self._items = None


        self._max_properties = None
        self._min_properties = None
        self._required = []
        self._properties = {}
        self._additional_properties = True

        self._enum = []
        self._format = None

        self._nullable = False
        self._deprecated = False
        self._read_only = False
        self._write_only = False

        self.not_ = kwargs.pop('not', None)

        external_documentation = kwargs.pop('external_documentation', None) or \
                                 kwargs.pop('externalDocs', None)
        self.external_documentation = external_documentation

        self.any_of = kwargs.pop('any_of', None) or kwargs.pop('anyOf', None)
        self.all_of = kwargs.pop('all_of', None) or kwargs.pop('allOf', None)
        self.one_of = kwargs.pop('one_of', None) or kwargs.pop('oneOf', None)
        self.unique_items = kwargs.pop('unique_items', None) or \
                            kwargs.pop('uniqueItems', None)
        self.multiple_of = kwargs.pop('multiple_of', None) or kwargs.pop('multipleOf', None)
        self.exclusive_maximum = kwargs.pop('exclusive_maximum', False) or \
                                 kwargs.pop('exclusiveMaximum', False)
        self.exclusive_minimum = kwargs.pop('exclusive_minimum', False) or \
                                 kwargs.pop('exclusiveMinimum', False)
        self.max_items = kwargs.pop('max_items', None) or kwargs.pop('maxItems', None)
        self.min_items = kwargs.pop('min_items', None) or kwargs.pop('minItems', None)
        self.max_properties = kwargs.pop('max_properties', None) or \
                              kwargs.pop('maxProperties', None)
        self.min_properties = kwargs.pop('min_properties', None) or \
                              kwargs.pop('minProperties', None)
        self.additional_properties = kwargs.pop('additional_properties', None) or \
                                     kwargs.pop('additionalProperties', None)
        self.read_only = kwargs.pop('read_only', False) or kwargs.pop('readOnly', False)
        self.write_only = kwargs.pop('write_only', False) or kwargs.pop('writeOnly', False)

        super().__init__(*args, **kwargs)

    @property
    def title(self):
        """The title of the object.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = validators.string(value, allow_empty = True)

    @property
    def type(self):
        """The primitive type expected for an object validating against this
        schema.

        Must be one of six supported values:

          * ``null``
          * ``boolean``
          * ``object``
          * ``array``
          * ``number``
          * ``string``
          * ``integer``

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        :raises ValueError: if assigning an unsupported value
        """
        return self._type

    @type.setter
    def type(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.lower()

        if value and value not in SUPPORTED_TYPES:
            raise ValueError('value ({}) not a supported value'.format(value))

        self._type = value

    @property
    def default(self):
        """The default value that should be assumed for an object that validates
        to this Schema.
        """
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def XML(self):
        """A metadata object that allows for more fine-tuned XML model
        definitions.

        :rtype: :class:`XML` / :obj:`None <python:None>`
        """
        return self._XML

    @XML.setter
    def XML(self, value):
        if not value:
            self._XML = None
        else:
            if not checkers.is_type(value, 'XML'):
                try:
                    self._XML = XML.new_from_dict(value)
                except (ValueError, TypeError):
                    raise ValueError('XML expects an XML object or compatible dict')
            else:
                self._XML = value

    @property
    def external_documentation(self):
        """Additional external documentation for this operation.

        :rtype: :class:`ExternalDocumentation` / :obj:`None <python:None>`
        """
        return self._external_documentation

    @external_documentation.setter
    def external_documentation(self, value):
        if not value:
            self._external_documentation = None
        else:
            print('setting External Documentation with:')
            print(value)
            if not checkers.is_type(value, 'ExternalDocumentation'):
                try:
                    value = ExternalDocumentation.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be an ExternalDocumentation object'
                                     ' or compatible dict, but was: %s' % value)

            self._external_documentation = value

    @property
    def example(self):
        """Example of an object that validates against the :class:`Schema`.

        .. note::

          The ``example`` field is mutually exclusive of the ``examples`` field.

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
    def discriminator(self):
        """The discriminator is a specific object in a schema which is used to
        inform the consumer of the specification of an alternative schema based
        on the value associated with it.

        .. tip::

          Think of the ``discriminator`` property as a way of systematically
          hinting which sub-schema applies to the object.

        :rtype: :class:`Discriminator` / :obj:`None <python:None>`
        """
        return self._discriminator

    @discriminator.setter
    def discriminator(self, value):
        if not value:
            self._discriminator = None
        else:
            if not checkers.is_type(value, 'Discriminator'):
                try:
                    self._discriminator = Discriminator.new_from_dict(value)
                except (ValueError, TypeError):
                    raise ValueError('expected a Discriminator or compatible dict')
            else:
                self._discriminator = value

    # OBJECT VALIDATION

    @property
    def all_of(self):
        """To validate against this schema, an object must validate against all
        of the :class:`Schema` or :class:`Reference` objects included in this
        property.

        :rtype: :class:`list <python:list>` of :class:`Schema` or :class:`Reference`
        """
        return self._all_of

    @all_of.setter
    def all_of(self, value):
        if not value:
            self._all_of = []
        else:
            clean_list = []
            if not checkers.is_iterable(value):
                value = [value]
            for item in value:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    dict_obj = validators.dict(item, allow_empty = False)
                    try:
                        new_item = self.__class__.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        try:
                            new_item = Reference.new_from_dict(dict_obj)
                        except (ValueError, TypeError):
                            raise ValueError('value expects an iterable of '
                                             'Schema, Reference, or compatible '
                                             'dict objects')
                else:
                    new_item = item

                clean_list.append(new_item)

            self._all_of = [x for x in clean_list]

    @property
    def one_of(self):
        """To validate against this schema, an objet must validate successfully
        against exactly one of the :class:`Schema` or :class:`Reference` objects
        included in this property.

        :rtype: :class:`list <python:list>` of :class:`Schema` or :class:`Reference`
        """
        return self._one_of

    @one_of.setter
    def one_of(self, value):
        if not value:
            self._one_of = []
        else:
            clean_list = []
            if not checkers.is_iterable(value):
                value = [value]
            for item in value:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    dict_obj = validators.dict(item, allow_empty = False)
                    try:
                        new_item = self.__class__.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        try:
                            new_item = Reference.new_from_dict(dict_obj)
                        except (ValueError, TypeError):
                            raise ValueError('value expects an iterable of '
                                             'Schema, Reference, or compatible '
                                             'dict objects')
                else:
                    new_item = item

                clean_list.append(new_item)

            self._one_of = [x for x in clean_list]

    @property
    def any_of(self):
        """To validate against this schema, an objet must validate against one or
        more of the :class:`Schema` or :class:`Reference` objects included in this
        property.

        :rtype: :class:`list <python:list>` of :class:`Schema` or :class:`Reference`
        """
        return self._any_of

    @any_of.setter
    def any_of(self, value):
        if not value:
            self._any_of = []
        else:
            clean_list = []
            if not checkers.is_iterable(value):
                value = [value]
            for item in value:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    dict_obj = validators.dict(item, allow_empty = False)
                    try:
                        new_item = self.__class__.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        try:
                            new_item = Reference.new_from_dict(dict_obj)
                        except (ValueError, TypeError):
                            raise ValueError('value expects an iterable of '
                                             'Schema, Reference, or compatible '
                                             'dict objects')
                else:
                    new_item = item

                clean_list.append(new_item)

            self._any_of = [x for x in clean_list]

    @property
    def not_(self):
        """To validate against this schema, an objet must *not* validate against
        the :class:`Schema` or :class:`Reference` object in this
        property.

        :rtype: :class:`Schema` / :class:`Reference` / :obj:`None <python:None>`
        """
        return self._not

    @not_.setter
    def not_(self, value):
        if not value:
            self._not = None
        else:
            if not checkers.is_type(value, ('Schema', 'Reference')):
                dict_obj = validators.dict(value, allow_empty = False)
                try:
                    new_item = self.__class__.new_from_dict(dict_obj)
                except (ValueError, TypeError):
                    try:
                        new_item = Reference.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        raise ValueError('value expects an iterable of '
                                         'Schema, Reference, or compatible '
                                         'dict objects')

            self._not = new_item

    # NUMERIC VALIDATION

    @property
    def multiple_of(self):
        """Indicates that the object must be a multiple of a numerical value.

        Defaults to ``1``.

        :rtype: :class:`int <python:int>`
        """
        return self._multiple_of

    @multiple_of.setter
    def multiple_of(self, value):
        value = validators.integer(value,
                                   allow_empty = True)
        if value is None:
            self._multiple_of = 1
        else:
            self._multiple_of = value

    @property
    def maximum(self):
        """The inclusive maximum value considered valid.

        :rtype: numeric / :obj:`None <python:None>`
        """
        return self._maximum

    @maximum.setter
    def maximum(self, value):
        self._maximum = validators.numeric(value, allow_empty = True)

    @property
    def exclusive_maximum(self):
        """Indicates the exclusive maximum value considered valid.

        If the instance is a number, then the instance is valid only if it has
        a value strictly less than (not equal to) the exclusive maximum.

        .. caution::

          To conform to OpenAPI v3.0, ``exclusive_maximum`` is automatically
          returned as a :class:`bool <python:bool>`. However, this
          behavior will be deprecated in OpenAPI v.3.1 to conform to the most-
          recent JSON Schema draft behavior, where ``exclusiveMaximum`` expects
          a numerical value.

        .. tip::

          To future-proof your Python implementations against the impending
          change to OpenAPI v3.1, assign numerical values to this property.
          The Python library will automatically convert them to
          :class:`bool <python:bool>` as appropriate.

        :rtype: :class:`bool <python:bool>` or numeric
        """
        return bool(self._exclusive_maximum)

    @exclusive_maximum.setter
    def exclusive_maximum(self, value):
        if isinstance(value, bool):
            self._exclusive_maximum = value
        else:
            value = validators.numeric(value, allow_empty = True)
            if value and self.maximum and value >= self.maximum:
                raise ValueError('exclusive maximum ({}) cannot be greater than'
                                 ' or equal to maximum ({})'.format(value,
                                                                    self.maximum))
            self._exclusive_maximum = validators.numeric(value,
                                                         allow_empty = True)

    @property
    def minimum(self):
        """The inclusive minimum value considered valid.

        :rtype: numeric / :obj:`None <python:None>`
        """
        return self._minimum

    @minimum.setter
    def minimum(self, value):
        self._minimum = validators.numeric(value, allow_empty = True)

    @property
    def exclusive_minimum(self):
        """Indicates the exclusive minimum value considered valid.

        If the instance is a number, then the instance is valid only if it has
        a value strictly greater than (not equal to) the exclusive minimum.

        .. caution::

          To conform to OpenAPI v3.0, ``exclusive_minimum`` is automatically
          returned as a :class:`bool <python:bool>`. However, this
          behavior will be deprecated in OpenAPI v.3.1 to conform to the most-
          recent JSON Schema draft behavior, where ``exclusiveMinimum`` expects
          a numerical value.

        .. tip::

          To future-proof your Python implementations against the impending
          change to OpenAPI v3.1, assign numerical values to this property.
          The Python library will automatically convert them to
          :class:`bool <python:bool>` as appropriate.

        :rtype: :class:`bool <python:bool>` or numeric
        """
        return bool(self._exclusive_minimum)

    @exclusive_minimum.setter
    def exclusive_minimum(self, value):
        if isinstance(value, bool):
            self._exclusive_minimum = value
        else:
            self._exclusive_minimum = validators.numeric(value,
                                                         allow_empty = True)

    # STRING VALIDATION

    @property
    def max_length(self):
        """A string instance is valid if its length is less than, or equal to,
        this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`

        :raises ValueError: if the value is less than 0 or not an integer
        """
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        self._max_length = validators.integer(value,
                                              allow_empty = True,
                                              minimum = 0)

    @property
    def min_length(self):
        """A string instance is valid if its length is greater than, or equal to,
        this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`

        :raises ValueError: if the value is less than 0 or not an integer
        """
        return self._min_length

    @min_length.setter
    def min_length(self, value):
        self._min_length = validators.integer(value,
                                              allow_empty = True,
                                              minimum = 0)

    @property
    def pattern(self):
        """A string instance is considered valid if it matches the regular expression
        stored in this property.

        .. note::

          The value of this keyword *must* be a string. This string SHOULD be a
          valid regular expression, according to the
          `ECMA 262 regular expression <https://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf>`_
          dialect.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = validators.string(value, allow_empty = True)


    # ARRAY VALIDATION

    @property
    def max_items(self):
        """An array instance is valid if its size is less than, or equal to, the
        value of this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._max_items

    @max_items.setter
    def max_items(self, value):
        self._max_items = validators.integer(value,
                                             allow_empty = True,
                                             minimum = 0)

    @property
    def min_items(self):
        """An array instance is valid if its size is greater than, or equal to, the
        value of this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._min_items

    @min_items.setter
    def min_items(self, value):
        self._min_items = validators.integer(value,
                                             allow_empty = True,
                                             minimum = 0)

    @property
    def unique_items(self):
        """If ``True``, an instance will only validate if the members of the array
        are all unique. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._unique_items

    @unique_items.setter
    def unique_items(self, value):
        self._unique_items = bool(value)

    @property
    def items(self):
        """A single object that provides the schema that members of the array
        should validate against.

        :rtype: :class:`Schema` / :class:`Reference` / :obj:`None <python:None>`
        """
        return self._items

    @items.setter
    def items(self, value):
        if not value:
            self._items = None
        else:
            if not checkers.is_type(value, ('Schema', 'Reference')):
                dict_obj = validators.dict(value, allow_empty = False)
                try:
                    new_item = self.__class__.new_from_dict(dict_obj)
                except (ValueError, TypeError):
                    try:
                        new_item = Reference.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        raise ValueError('value expects an iterable of '
                                         'Schema, Reference, or compatible '
                                         'dict objects')

            self._items = new_item

    # OBJECT VALIDATION

    @property
    def max_properties(self):
        """An object instance is valid if its number of properties is less than,
        or equal to, the value of this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._max_properties

    @max_properties.setter
    def max_properties(self, value):
        self._max_properties = validators.integer(value,
                                                  allow_empty = True,
                                                  minimum = 0)

    @property
    def min_properties(self):
        """An object instance is valid if its number of properties is greater
        than, or equal to, the value of this property.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._min_properties

    @min_properties.setter
    def min_properties(self, value):
        self._min_properties = validators.integer(value,
                                                  allow_empty = True,
                                                  minimum = 0)

    @property
    def required(self):
        """Array that indicates which properties are required for an object to
        validate successfully against this :class:`Schema`.

        :rtype: :class:`list <python:list>` of :class:`str <python:str>`
        """
        return self._required

    @required.setter
    def required(self, value):
        if not value:
            self._required = []
        else:
            if not checkers.is_iterable(value) and not checkers.is_string(value):
                value = [value]

            self._required = [validators.string(x) for x in value]

    @property
    def properties(self):
        """:class:`dict <python:dict>` providing the :class:`Schema` for each
        property of an ``object`` to validate against.

        :rtype: :class:`dict <python:dict>` with :class:`str <python:str>` keys
          and :class:`Schema` or :class:`Reference` values
        """
        return self._properties

    @properties.setter
    def properties(self, value):
        value = validators.dict(value, allow_empty = True)

        if not value:
            self._properties = {}
        else:
            new_properties = {}
            for key in value:
                key = validators.string(key, allow_empty = False)
                if not checkers.is_type(value[key], ('Schema', 'Reference')):
                    item = validators.dict(value[key], allow_empty = False)
                    try:
                        new_item = self.__class__.new_from_dict(value[key])
                    except (ValueError, TypeError):
                        try:
                            new_item = Reference.new_from_dict(value[key])
                        except (ValueError, TypeError):
                            raise ValueError('value expects a dict whose keys '
                                             'are strings and values are either'
                                             ' Schema objects, Reference objects,'
                                             ' or compatible dicts. Received '
                                             'an incompatible dict.')
                    new_properties[key] = new_item

            self._properties = new_properties

    @property
    def additional_properties(self):
        """Controls how the :class:`Schema` validates an object with properties
        not defined in the :ref:`properties <Schema.properties>` property.

        If a :class:`Schema` or :class:`Reference` object, any additional
        property not defined in the :ref:`properties <Schema.properties>`
        property must validate against that schema.

        If a :class:`bool <python:bool>` and ``True``, then any additional
        properties of any construction are allowed. If a :class:`bool <python:bool>`
        and ``False``, then *no* additional properties of any kind are allowed.

        Defaults to ``True``.

        :rtype: :class:`bool <python:bool>` / :class:`Schema` /
          :class:`Reference`
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, value):
        if isinstance(value, bool) or not value:
            self._additional_properties = value
        else:
            if not checkers.is_type(value, ('Schema', 'Reference')):
                dict_obj = validators.dict(value, allow_empty = False)
                try:
                    new_item = self.__class__.new_from_dict(dict_obj)
                except (ValueError, TypeError):
                    try:
                        new_item = Reference.new_from_dict(dict_obj)
                    except (ValueError, TypeError):
                        raise ValueError('value expects an iterable of '
                                         'Schema, Reference, or compatible '
                                         'dict objects')

            self._additional_properties = new_item


    @property
    def enum(self):
        """A restricted set of allowed values.

        :rtype: :class:`list`
        """
        return self._enum

    @enum.setter
    def enum(self, value):
        if not value:
            self._enum = []
        else:
            if not checkers.is_iterable(value):
                value = [value]

            self._enum = [x for x in value]

    @property
    def format(self):
        """The arbitrary string definition of the format to validate the value
        against.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._format

    @format.setter
    def format(self, value):
        self._format = validators.string(value, allow_empty = True)


    @property
    def nullable(self):
        """If ``True``, a value of :obj:`None <python:None>` (or ``null`` in JSON)
        is considered valid for this :class:`Schema`. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._nullable

    @nullable.setter
    def nullable(self, value):
        self._nullable = bool(value)

    @property
    def read_only(self):
        """If ``True``, the property will only be returned in responses and cannot
        be mutated through requests. Defaults to ``False``.

        .. note::

          This property is only relevant for :ref:`properties <Schema.properties>`
          within a :class:`Schema`.

        :rtype: :class:`bool <python:bool>`
        """
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        self._read_only = bool(value)

    @property
    def write_only(self):
        """If ``True``, the property will not be returned in responses and can only
        be written through requests. Defaults to ``False``.

        .. note::

          This property is only relevant for :ref:`properties <Schema.properties>`
          within a :class:`Schema`.

        :rtype: :class:`bool <python:bool>`
        """
        return self._write_only

    @write_only.setter
    def write_only(self, value):
        self._write_only = bool(value)

    @property
    def deprecated(self):
        """If ``True``, the property is planned to be deprecated and should be
        phased out of usage. Defaults to ``False``.

        .. note::

          This property is only relevant for :ref:`properties <Schema.properties>`
          within a :class:`Schema`.

        :rtype: :class:`bool <python:bool>`
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value):
        self._deprecated = bool(value)



    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "nullable": self.nullable,
            "readOnly": self.read_only,
            "writeOnly": self.write_only,
            "deprecated": self.deprecated
        }

        if self.default:
            output['default'] = self.default
        if self.XML:
            output['xml'] = self.XML.to_dict(*args, **kwargs)
        if self.discriminator:
            output['discriminator'] = self.discriminator.to_dict(*args, **kwargs)
        if self.external_documentation:
            output['externalDocs'] = self.external_documentation.to_dict(*args,
                                                                         **kwargs)
        if self.example:
            if hasattr(self.example, 'to_dict'):
                output['example'] = self.example.to_dict(*args, **kwargs)
            else:
                output['example'] = self.example

        if self.format:
            output['format'] = self.format

        if self.enum:
            output['enum'] = self.enum

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        if self.all_of:
            output['allOf'] = [x.to_dict(*args, **kwargs) for x in self.all_of]
        if self.any_of:
            output['anyOf'] = [x.to_dict(*args, **kwargs) for x in self.any_of]
        if self.one_of:
            output['oneOf'] = [x.to_dict(*args, **kwargs) for x in self.one_of]
        if self.not_:
            output['not'] = self.not_.to_dict(*args, **kwargs)

        if self.type == 'number' or self.type == 'integer':
            output['multipleOf'] = self.multiple_of

            if self.maximum is not None:
                output['maximum'] = self.maximum
            output['exclusiveMaximum'] = self.exclusive_maximum

            if self.minimum is not None:
                output['minimum'] = self.minimum
            output['exclusiveMinimum'] = self.exclusive_minimum

        elif self.type == 'string':
            if self.max_length is not None:
                output['maxLength'] = self.max_length
            if self.min_length is not None:
                output['minLength'] = self.min_length
            if self.pattern is not None:
                output['pattern'] = self.pattern

        elif self.type == 'array':
            if self.max_items is not None:
                output['maxItems'] = self.max_items

            if self.min_items is not None:
                output['minItems'] = self.min_items

            output['uniqueItems'] = self.unique_items

            if self.items:
                output['items'] = self.items.to_dict(*args, **kwargs)
        elif self.type == 'object':
            if self.max_properties is not None:
                output['maxProperties'] = self.max_properties

            if self.min_properties is not None:
                output['minProperties'] = self.min_properties

            if self.required:
                output['required'] = self.required

            if self.properties:
                output['properties'] = {}
                for key in self.properties:
                    if hasattr(self.properties[key], 'to_dict'):
                        output['properties'][key] = self.properties[key].to_dict(*args, **kwargs)
                    else:
                        output['properties'][key] = self.properties[key]

            if not isinstance(self.additional_properties, bool):
                output['additionalProperties'] = self.additional_properties.to_dict(*args, *kwargs)
            else:
                output['additionalProperties'] = self.additional_properties

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Schema` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Schema
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Schema` object
        :rtype: :class:`Encoding`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        title = copied_obj.pop('title', None)
        description = copied_obj.pop('description', None)
        type_ = copied_obj.pop('type', None)
        default = copied_obj.pop('default', None)
        XML = copied_obj.pop('xml', None) or copied_obj.pop('XML', None)

        external_documentation = copied_obj.pop('externalDocs', None) or \
                                 copied_obj.pop('external_documentation', None)

        example = copied_obj.pop('example', None)

        discriminator = copied_obj.pop('discriminator', None)

        all_of = copied_obj.pop('allOf', []) or copied_obj.pop('all_of', [])
        any_of = copied_obj.pop('anyOf', []) or copied_obj.pop('any_of', [])
        one_of = copied_obj.pop('oneOf', []) or copied_obj.pop('one_of', [])
        not_ = copied_obj.pop('not', None)

        multiple_of = copied_obj.pop('multipleOf', 1) or \
                      copied_obj.pop('multiple_of', 1)

        maximum = copied_obj.pop('maximum', None)
        exclusive_maximum = copied_obj.pop('exclusiveMaximum', None) or \
                            copied_obj.pop('exclusive_maximum', None)
        minimum = copied_obj.pop('minimum', None)
        exclusive_minimum = copied_obj.pop('exclusiveMinimum', None) or \
                            copied_obj.pop('exclusive_minimum', None)

        max_length = copied_obj.pop('maxLength', None) or \
                     copied_obj.pop('max_length', None)
        min_length = copied_obj.pop('minLength', None) or \
                     copied_obj.pop('min_length', None)
        pattern = copied_obj.pop('pattern', None)

        max_items = copied_obj.pop('maxItems', None) or copied_obj.pop('max_items',
                                                                       None)
        min_items = copied_obj.pop('minItems', None) or copied_obj.pop('min_items',
                                                                       None)
        unique_items = copied_obj.pop('uniqueItems', False) or \
                       copied_obj.pop('unique_items', False)
        items = copied_obj.pop('items', None)

        max_properties = copied_obj.pop('maxProperties', None) or \
                         copied_obj.pop('max_properties', None)
        min_properties = copied_obj.pop('minProperties', None) or \
                         copied_obj.pop('min_properties', None)

        required = copied_obj.pop('required', [])
        properties = copied_obj.pop('properties', {})
        additional_properties = copied_obj.pop('additionalProperties', True) or \
                                copied_obj.pop('additional_properties', True)

        enum = copied_obj.pop('enum', [])
        format_ = copied_obj.pop('format', None)
        nullable = copied_obj.pop('nullable', False)
        deprecated = copied_obj.pop('deprecated', False)
        read_only = copied_obj.pop('readOnly', False) or \
                    copied_obj.pop('read_only', False)
        write_only = copied_obj.pop('writeOnly', False) or \
                     copied_obj.pop('write_only', False)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(title = title,
                     description = description,
                     type = type_,
                     default = default,
                     XML = XML,
                     external_documentation = external_documentation,
                     example = example,
                     discriminator = discriminator,
                     all_of = all_of,
                     any_of = any_of,
                     one_of = one_of,
                     not_ = not_,
                     multiple_of = multiple_of,
                     maximum = maximum,
                     exclusive_maximum = exclusive_maximum,
                     minimum = minimum,
                     exclusive_minimum = exclusive_minimum,
                     max_length = max_length,
                     min_length = min_length,
                     pattern = pattern,
                     max_items = max_items,
                     min_items = min_items,
                     unique_items = unique_items,
                     items = items,
                     max_properties = max_properties,
                     min_properties = min_properties,
                     required = required,
                     properties = properties,
                     additional_properties = additional_properties,
                     enum = enum,
                     format = format_,
                     nullable = nullable,
                     deprecated = deprecated,
                     read_only = read_only,
                     write_only = write_only,
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

        self.title = copied_obj.pop('title', self.title)
        self.description = copied_obj.pop('description', self.description)
        self.type = copied_obj.pop('type', self.type)
        self.default = copied_obj.pop('default', self.default)
        self.XML = copied_obj.pop('XML', None) or copied_obj.pop('xml', self.XML)
        if 'externalDocs' in copied_obj:
            self.external_documentation = copied_obj.pop('externalDocs')
        elif 'external_documentation' in copied_obj:
            self.external_documentation = copied_obj.pop('external_documentation')

        self.example = copied_obj.pop('example', self.example)

        self.discriminator = copied_obj.pop('discriminator', self.discriminator)

        if 'allOf' in copied_obj:
            self.all_of = copied_obj.pop('allOf', self.all_of)
        elif 'all_of' in copied_obj:
            self.all_of = copied_obj.pop('all_of', self.all_of)
        if 'anyOf' in copied_obj:
            self.any_of = copied_obj.pop('anyOf', self.any_of)
        elif 'any_of' in copied_obj:
            self.any_of = copied_obj.pop('any_of', self.any_of)
        if 'oneOf' in copied_obj:
            self.one_of = copied_obj.pop('oneOf', self.one_of)
        elif 'one_of' in copied_obj:
            self.one_of = copied_obj.pop('one_of', self.one_of)
        self.not_ = copied_obj.pop('not', self.not_)

        self.multiple_of = copied_obj.pop('multipleOf', self.multiple_of) or \
                           copied_obj.pop('multiple_of', self.multiple_of)

        self.maximum = copied_obj.pop('maximum', self.maximum)
        self.exclusive_maximum = copied_obj.pop('exclusiveMaximum',
                                                self.exclusive_maximum) or \
                                 copied_obj.pop('exclusive_maximum',
                                                self.exclusive_maximum)
        self.minimum = copied_obj.pop('minimum', self.minimum)
        self.exclusive_minimum = copied_obj.pop('exclusiveMinimum',
                                                self.exclusive_minimum) or \
                                 copied_obj.pop('exclusive_minimum',
                                                self.exclusive_minimum)

        self.max_length = copied_obj.pop('maxLength', self.max_length) or \
                          copied_obj.pop('max_length', self.max_length)
        self.min_length = copied_obj.pop('minLength', self.min_length) or \
                          copied_obj.pop('min_length', self.min_length)
        self.pattern = copied_obj.pop('pattern', self.pattern)

        self.max_items = copied_obj.pop('maxItems', self.max_items) or \
                         copied_obj.pop('max_items', self.max_items)
        self.min_items = copied_obj.pop('minItems', self.min_items) or \
                         copied_obj.pop('min_items', self.min_items)
        self.unique_items = copied_obj.pop('uniqueItems', None) or \
                            copied_obj.pop('unique_items', self.unique_items)
        self.items = copied_obj.pop('items', self.items)

        self.max_properties = copied_obj.pop('maxProperties', None) or \
                              copied_obj.pop('max_properties', self.max_properties)
        self.min_properties = copied_obj.pop('minProperties', None) or \
                              copied_obj.pop('min_properties', self.min_properties)

        self.required = copied_obj.pop('required', self.required)
        self.properties = copied_obj.pop('properties', self.properties)
        self.additional_properties = copied_obj.pop('additionalProperties',
                                                    None) or \
                                     copied_obj.pop('additional_properties',
                                                    self.additional_properties)

        self.enum = copied_obj.pop('enum', self.enum)
        self.format_ = copied_obj.pop('format', self.format)
        self.nullable = copied_obj.pop('nullable', self.nullable)
        self.deprecated = copied_obj.pop('deprecated', self.deprecated)
        self.read_only = copied_obj.pop('readOnly', None) or \
                         copied_obj.pop('read_only', self.read_only)
        self.write_only = copied_obj.pop('writeOnly', None) or \
                          copied_obj.pop('write_only', self.write_only)

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
        if not checkers.is_string(self.type):
            return False
        if self.all_of:
            for item in self.all_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    return False
        if self.any_of:
            for item in self.any_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    return False
        if self.one_of:
            for item in self.one_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    return False
        if self.not_ and not checkers.is_type(self.not_, ('Schema', 'Reference')):
            return False
        if self.type == 'array' and not self.items:
            return False
        if self.items and not checkers.is_type(self.items, ('Schema', 'Reference')):
            return False
        if self.properties:
            for key in self.properties:
                if not checkers.is_type(self.properties[key], ('Schema', 'Reference')):
                    return False
        if self.additional_properties and not isinstance(self.additional_properties, bool):
            if not checkers.is_type(self.additional_properties, ('Schema', 'Reference')):
                return False

        if self.discriminator and not self.one_of and not self.any_of and not self.all_of:
            return False

        return True

    @property
    def validity_message(self):
        """Human-readable message that provides a diagnosis of the object's
        validity. If valid, will return "Object is valid." If not valid, will
        provide a series of diagnostic messages.

        .. note::

          This property is **NOT** meant to be machine-readable. It is included
          for diagnostic purposes and to provide easier debugging of your
          applications.

        :rtype: :class:`str <python:str>`

        """
        if self.is_valid:
            return "Object is valid."

        output = 'OBJECT IS INVALID. Reasons are:'

        if not checkers.is_string(self.type):
            output += '\n\n* type property is not a string.'

        if self.all_of:
            all_of_count = 0
            for item in self.all_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    all_of_count += 1
            if all_of_count > 0:
                output += '\n\n* {} items in all_of are not Schema or Reference objects'.format(all_of_count)

        if self.any_of:
            any_of_count = 0
            for item in self.any_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    any_of_count += 1

            if any_of_count > 0:
                output += '\n\n* {} items in any_of are not Schema or Reference objects'.format(any_of_count)

        if self.one_of:
            one_of_count = 0
            for item in self.one_of:
                if not checkers.is_type(item, ('Schema', 'Reference')):
                    one_of_count += 1

            if one_of_count > 0:
                output += '\n\n* {} items in one_of are not Schema or Reference objects'.format(one_of_count)

        if self.not_ and not checkers.is_type(self.not_, ('Schema', 'Reference')):
            output += '\n\n* not_ is not a Schema or Reference object'

        if self.type == 'array' and not self.items:
            output += '\n\n* type is set to "array", but items is empty'

        if self.items and not checkers.is_type(self.items, ('Schema', 'Reference')):
            output += '\n\n* items is not a Schema or Reference object'

        if self.properties:
            for key in self.properties:
                if not checkers.is_type(self.properties[key], ('Schema', 'Reference')):
                    output += '\n\n* properties.{} is not a Schema or Reference object'.format(key)

        if self.additional_properties and not isinstance(self.additional_properties, bool):
            if not checkers.is_type(self.additional_properties, ('Schema', 'Reference')):
                output += '\n\n* additional_properties is not a bool, Schem,a or Reference object'

        if self.discriminator and not self.one_of and not self.any_of and not self.all_of:
            output += '\n\n* discriminator can only be set if one_of, any_of, or all_of are used'

        return output
