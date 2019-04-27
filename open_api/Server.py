# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api._object_metaclass import OpenAPIObject
from open_api.server_variable import ServerVariable
from open_api.utility_classes import Extensions, ManagedList
from open_api.utility_functions import validate_url

class Server(OpenAPIObject):
    """Object representation of a single :term:`Server`."""

    def __init__(self, *args, **kwargs):
        self._url = None
        self._description = None
        self._variables = None
        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def url(self):
        """A URL to the target host.

        .. note::

          Supports :term:`Server Variables` and may be relative, to indicate that the host
          location is relative to the location where the OpenAPI document is being served.
          Variable substitutions will be made when a variable is named in ``{`` brackets
          ``}``.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._url

    @url.setter
    def url(self, value):
        self._url = validate_url(value, allow_empty = True, allow_special_ips = True)

    @property
    def variables(self):
        """A collection of :class:`ServerVariable` objects that are used as substition
        values within the object's URL.

        :rtype: :class:`ManagedList` (subclass of :class:`list <python:list>`) of
          :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._variables

    @variables.setter
    def variables(self, value):
        if not value:
            value = None
        else:
            if checkers.is_type(value, 'ServerVariable'):
                value = [value]
            if checkers.is_type(value, list) and not checkers.is_type(value,
                                                                      'ManagedList'):
                value = ManagedList(*value)

            if not checkers.is_type(value, 'ManagedList'):
                raise ValueError('value must be a ServerVariable, list, or ManagedList. '
                                 'Was: %s' % value.__class__.__name__)

            for item in value:
                if not checkers.is_type(item, 'ServerVariable'):
                    raise ValueError('items must be a ServerVariable object. Was: %s'
                                     % item.__class__.__name__)

        self._variables = value

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'url': self.url,
            'description': self.description,
            'variables': None
        }
        if self.variables is not None:
            output['variables'] = self.variables.add_to_dict(output['variables'],
                                                             **kwargs)
        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Server` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the extension
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Server` object
        :rtype: :class:`Server`
        """
        obj = validators.dict(obj, allow_empty = True)
        if not obj:
            obj = {}

        url = obj.pop('url', None)
        description = obj.pop('description', None)
        variables = obj.pop('variables', None)
        variable_list = []
        if variables:
            for key in variables:
                variable = ServerVariable.new_from_dict(variables[key], **kwargs)
                variable.name = key
                variable_list.append(variable)
        if obj:
            extensions = Extensions.new_from_dict(obj, **kwargs)
        else:
            extensions = None

        output = cls(url = url,
                     description = description,
                     variables = variable_list,
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
        if not input_data:
            input_data = {}

        if 'url' in input_data:
            self.url = input_data.pop('url')
        if 'description' in input_data:
            self.description = input_data.pop('description')
        if input_data and 'variables' in input_data:
            variables = input_data.pop('variables', {})
            for key in variables:
                selected_variable = variables.pop(key)
                for item in self.variables:
                    if item.name == key:
                        item.update_from_dict(selected_variable)
            self.variables.extend([ServerVariable.new_from_dict(x) for x in variables])

        if input_data and self.extensions:
            self.extensions.update_from_dict(input_data)
        elif input_data:
            self.extensions = input_data

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        is_valid = self.url is not None and \
                   (self.extensions is None or self.extensions.is_valid)

        if not is_valid:
            return False

        if self.variables:
            for variable in self.variables:
                if not variable.is_valid:
                    return False

        return is_valid
