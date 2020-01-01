# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject

class ServerVariable(OpenAPIObject):
    """Object representation of a :term:`Server Variable` object."""

    def __init__(self, *args, **kwargs):
        # Required
        self._default = None
        self._name = None

        # Not Required
        self._enum = None
        self._description = None
        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def name(self):
        """The name given to the server variable.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validators.string(value, allow_empty = True)

    @property
    def default(self):
        """The default value to use for substitution.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._default

    @default.setter
    def default(self, value):
        self._default = validators.string(value, allow_empty = True)

    @property
    def enum(self):
        """A collection of string values that can be used for substitution if options are
        limited by the API.

        :rtype: :class:`ManagedList` (subclass of :class:`list <python:list>`) of
          :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._enum

    @enum.setter
    def enum(self, value):
        if not value:
            value = None
        else:
            if checkers.is_string(value):
                value = [value]
            if checkers.is_type(value, list) and not checkers.is_type(value,
                                                                      'ManagedList'):
                value = [validators.string(x, allow_empty = False, coerce_value = True)
                         for x in value]
                value = ManagedList(*value)

            if not checkers.is_type(value, 'ManagedList'):
                raise ValueError('value must be a str, list, or ManagedList. Was: %s' %
                                 value.__class__.__name__)

        self._enum = value

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'default': self.default,
            'description': self.description,
            'enum': self.enum
        }
        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`ServerVariable` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the extension
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`ServerVariable` object
        :rtype: :class:`ServerVariable`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        name = copied_obj.pop('name', None)
        default = copied_obj.pop('default', None)
        description = copied_obj.pop('description', None)
        enum = copied_obj.pop('enum', None)
        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(name = name,
                     default = default,
                     description = description,
                     enum = enum,
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
        copied_input_data = {}
        for key in input_data:
            copied_input_data[key] = input_data[key]

        if 'name' in copied_input_data:
            self.name = copied_input_data.get('name')
        if 'default' in copied_input_data:
            self.default = copied_input_data.get('default')
        if 'description' in copied_input_data:
            self.description = copied_input_data.get('description')
        if 'enum' in copied_input_data:
            self.enum = copied_input_data.get('enum')

        if copied_input_data and self.extensions:
            self.extensions.update_from_dict(copied_input_data)
        elif input_data:
            self.extensions = copied_input_data

    def add_to_dict(self, obj, **kwargs):
        """Add a :class:`dict <python:dict>` representation of the :class:`ServerVariable`
        to ``obj``.

        :param obj: The :class:`dict <python:dict>` to which the :class:`ServerVariable`
          will be added.
        :type obj: :class:`dict <python:dict>`

        :returns: ``obj`` with the :class:`dict <python:dict>` representation of the
          :class:`ServerVariable` instance as a key/value pair
        :rtype: :class:`dict <python:dict>`

        :raises ValueError: if ``obj`` is not a :class:`dict <python:dict>`
        """
        obj = validators.dict(obj, allow_empty = True)
        if not obj:
            obj = {}

        obj[self.name] = self.to_dict(**kwargs)

        return obj

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        if not self.default:
            return False

        return True
