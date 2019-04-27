# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import yaml
from validator_collection import validators, checkers

from open_api.ServerVariable import ServerVariable
from open_api.utility_classes import Markup, Extensions, ManagedList
from open_api.utility_functions import parse_json, parse_yaml, validate_url

class Server(object):
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
    def description(self):
        """A description of the :term:`Server`. Defaults to :obj:`None <python:None>`.

        Supports markup expressed in :term:`CommonMark` or :term:`ReStructuredText`.

        :rtype: :class:`Markup <open_api.utility_classes.Markup>` /
          :obj:`None <python:None>`
        """
        return self._description

    @description.setter
    def description(self, value):
        if checkers.is_type(value, str) and not checkers.is_type(value, Markup):
            value = Markup(value)

        if checkers.is_type(value, Markup):
            self._description = value
        else:
            raise ValueError('value must be either a string or a Markup object. '
                             'Was: {}'.format(value.__class__.__name__))

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


    @property
    def extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        :term:`Server`. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if checkers.is_type(value, 'Extensions'):
            self._extensions = value
        elif checkers.is_dict(value):
            value = Extensions.new_from_dict(value)
            self._extensions = Extensions.new_from_dict(value)
        else:
            try:
                value = parse_json(value)
            except ValueError:
                try:
                    value = parse_yaml(value)
                except ValueError:
                    raise ValueError('value is not a valid Specification Extensions '
                                     'object, compatible dict, JSON, or YAML. Was: %s'
                                     % value.__class__.__name__)

            self._extensions = Extensions.new_from_dict(value)

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

    def to_json(self, serialize_function = None, **kwargs):
        """Return a JSON string compliant with the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>`_

        :param serialize_function: Optionally override the default JSON serializer.
          Defaults to :obj:`None <python:None>`, which applies the default
          :ref:`ujson.dumps() <ujson:ujson.dumps>` and then falls back to the
          :doc:`simplejson <simplejson:index>` JSON serializer if unavailable, and then
          finally falls back to :ref:`json.dumps() <python:json.dumps>` if uJSON and
          simplejson are unavailable.

          .. note::

            Use the ``serialize_function`` parameter to override the default
            JSON serializer.

            A valid ``serialize_function`` is expected to accept a single
            :class:`dict <python:dict>` and return a :class:`str <python:str>`,
            similar to :func:`simplejson.dumps() <simplejson:simplejson.dumps>`.

            If you wish to pass additional arguments to your ``serialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type serialize_function: callable / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          JSON serializer function. By default, these are options which are passed
          to :func:`ujson.dumps() <ujson:ujson.dumps>`.
        :type kwargs: keyword arguments

        :returns: A :class:`str <python:str>` with the JSON representation of the
          object.
        :rtype: :class:`str <python:str>`
        """
        if serialize_function is None:
            serialize_function = json.dumps

        if not checkers.is_callable(serialize_function):
            raise ValueError(
                'serialize_function (%s) is not callable' % serialize_function
            )

        as_dict = self.to_dict(serialize_function = serialize_function, **kwargs)
        result = serialize_function(as_dict, **kwargs)

        return result

    def to_yaml(self, serialize_function = None, **kwargs):
        """Return a YAML string compliant with the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>`_

        :param serialize_function: Optionally override the default YAML serializer.
          Defaults to :obj:`None <python:None>`, which calls the default ``yaml.dump()``
          function from the `PyYAML <https://github.com/yaml/pyyaml>`_ library.

          .. note::

            Use the ``serialize_function`` parameter to override the default
            YAML serializer.

            A valid ``serialize_function`` is expected to
            accept a single :class:`dict <python:dict>` and return a
            :class:`str <python:str>`, similar to ``yaml.dump()``.

            If you wish to pass additional arguments to your ``serialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type serialize_function: callable / :obj:`None <python:None>`

        :param config_set: If not :obj:`None <python:None>`, the named configuration set
          to use. Defaults to :obj:`None <python:None>`.
        :type config_set: :class:`str <python:str>` / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          YAML serializer function. By default, these are options which are passed
          to ``yaml.dump()``.
        :type kwargs: keyword arguments

        :returns: A :class:`str <python:str>` with the YAML representation of the
          object.
        :rtype: :class:`str <python:str>`

        """
        if serialize_function is None:
            serialize_function = yaml.dump
        else:
            if checkers.is_callable(serialize_function) is False:
                raise ValueError(
                    'serialize_function (%s) is not callable' % serialize_function
                )

        as_dict = self.to_dict(serialize_function = None, **kwargs)
        result = serialize_function(as_dict, **kwargs)

        return result

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

    @classmethod
    def new_from_json(cls,
                      input_data,
                      deserialize_function = None,
                      **kwargs):
        """Create a new :class:`Extensions` object from a JSON string.

        :param input_data: The JSON data to de-serialize.
        :type input_data: :class:`str <python:str>`

        :param deserialize_function: Optionally override the default JSON deserializer.
          Defaults to :obj:`None <python:None>`, which first tries to use
          :ref:`ujson.loads() <ujson:ujson.loads>`, then falls back to
          :ref:`simplejson.loads() <simplejson:simplejson.loads>`, and finally defaults
          to the standard library's :ref:`json.loads() <python:json.loads>`
          function.

          .. note::

            Use the ``deserialize_function`` parameter to override the default
            JSON deserializer. A valid ``deserialize_function`` is expected to
            accept a single :class:`str <python:str>` and return a
            :class:`dict <python:dict>`, similar to
            :ref:`simplejson.loads() <simplejson:simplejson.loads>`

            If you wish to pass additional arguments to your ``deserialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type deserialize_function: callable / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          JSON deserializer function. By default, these are options which are passed
          to the de-serializer function (e.g.
          :ref:`simplejson.loads() <simplejson:simplejson.loads>`).
        :type kwargs: keyword arguments

        :returns: A :class:`ServerVariable` representation of ``input_data``.
        :rtype: :class:`ServerVariable`
        """
        dict_object = parse_json(input_data,
                                 deserialize_function = deserialize_function,
                                 **kwargs)

        output = cls.new_from_dict(dict_object)

        return output

    @classmethod
    def new_from_yaml(cls,
                      input_data,
                      deserialize_function = None,
                      **kwargs):
        """De-serialize YAML data into a :class:`ServerVariable` object.

        :param input_data: The YAML data to de-serialize.
        :type input_data: :class:`str <python:str>` / Path-like object

        :param deserialize_function: Optionally override the default YAML deserializer.
          Defaults to :obj:`None <python:None>`, which calls the default
          ``yaml.safe_load()`` function from the
          `PyYAML <https://github.com/yaml/pyyaml>`_ library.

          .. note::

            Use the ``deserialize_function`` parameter to override the default
            YAML deserializer. A valid ``deserialize_function`` is expected to
            accept a single :class:`str <python:str>` and return a
            :class:`dict <python:dict>`, similar to ``yaml.safe_load()``.

            If you wish to pass additional arguments to your ``deserialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type deserialize_function: callable / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          YAML deserializer function. By default, these are options which are passed
          to ``yaml.safe_load()``.
        :type kwargs: keyword arguments

        :returns: :class:`ServerVariable` representation of ``input_data``
        :rtype: :class:`ServerVariable`
        """
        dict_object = parse_yaml(input_data,
                                 deserialize_function = deserialize_function,
                                 **kwargs)

        output = cls.new_from_dict(dict_object)

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

    def update_from_json(self,
                         input_data,
                         deserialize_function = None,
                         **kwargs):
        """Update the instance based on ``input_data``.

        :param input_data: The JSON data to de-serialize.
        :type input_data: :class:`str <python:str>`

        :param deserialize_function: Optionally override the default JSON deserializer.
          Defaults to :obj:`None <python:None>`, which first tries to use
          :ref:`ujson.loads() <ujson:ujson.loads>`, then falls back to
          :ref:`simplejson.loads() <simplejson:simplejson.loads>`, and finally defaults
          to the standard library's :ref:`json.loads() <python:json.loads>`
          function.

          .. note::

            Use the ``deserialize_function`` parameter to override the default
            JSON deserializer. A valid ``deserialize_function`` is expected to
            accept a single :class:`str <python:str>` and return a
            :class:`dict <python:dict>`, similar to
            :ref:`simplejson.loads() <simplejson:simplejson.loads>`

            If you wish to pass additional arguments to your ``deserialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type deserialize_function: callable / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          JSON deserializer function. By default, these are options which are passed
          to the de-serializer function (e.g.
          :ref:`simplejson.loads() <simplejson:simplejson.loads>`).
        :type kwargs: keyword arguments

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        as_dict = parse_json(input_data,
                             deserialize_function = deserialize_function,
                             **kwargs)

        self.update_from_dict(as_dict)

    def update_from_yaml(self,
                         input_data,
                         deserialize_function = None,
                         **kwargs):
        """Update the instance based on ``input_data``.

        :param input_data: The YAML data to de-serialize.
        :type input_data: :class:`str <python:str>` / Path-like object

        :param deserialize_function: Optionally override the default YAML deserializer.
          Defaults to :obj:`None <python:None>`, which calls the default
          ``yaml.safe_load()`` function from the
          `PyYAML <https://github.com/yaml/pyyaml>`_ library.

          .. note::

            Use the ``deserialize_function`` parameter to override the default
            YAML deserializer. A valid ``deserialize_function`` is expected to
            accept a single :class:`str <python:str>` and return a
            :class:`dict <python:dict>`, similar to ``yaml.safe_load()``.

            If you wish to pass additional arguments to your ``deserialize_function``
            pass them as keyword arguments (in ``kwargs``).

        :type deserialize_function: callable / :obj:`None <python:None>`

        :param kwargs: Optional keyword parameters that are passed to the
          YAML deserializer function. By default, these are options which are passed
          to ``yaml.safe_load()``.
        :type kwargs: keyword arguments

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        as_dict = parse_yaml(input_data,
                             deserialize_function = deserialize_function,
                             **kwargs)

        self.update_from_dict(as_dict)

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
