# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.responses.Response import Response

class Responses(dict):
    """A container for the expected responses of an operation. The container
    maps a HTTP response code to the expected response.

    .. info::

      The documentation is not necessarily expected to cover all possible HTTP
      response codes because they may not be known in advance. However,
      documentation is expected to cover a successful operation response and any
      known errors.

    Holds the relative paths to the individual endpoints and their operations.
    The path is appended to the URL from the :class:`Server` Object in order to
    construct the full URL.

    .. tip::

      ``'default'`` may be used as a default response for all HTTP status codes
      not covered explicitly by the specification

    .. caution::

      Must contain at least one response code, and it should be a response code
      for a successful operation.

    """

    def __init__(self, *args, **kwargs):
        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def default(self):
        """The documentation of responses other than the ones declared for
        specific HTTP response codes. Use this field to cover undeclared
        responses.
        """
        return self.get('default', None)

    @default.setter
    def default(self, value):
        self['default'] = value

    def __getattr__(self, name):
        return super(Responses, self).__getattr__(name)

    def __delitem__(self, key):
        super(Responses, self).__delitem__(key)

    def __getitem__(self, name):
        if name.startswith('__') and name.endswith('__') and hasattr(self, name):
            return getattr(self, name)

        return super(Responses, self).__getitem__(name)

    def get(self, name, default = None):
        return self.__getitem__(name) or default

    def __setitem__(self, name, value):
        if name != 'default':
            if checkers.is_integer(name):
                name = validators.string(name,
                                         allow_empty = True,
                                         coerce_value = True)
            else:
                raise ValueError(
                    'key (%s) must either be "default" or an HTTP status code' % name)
        if value:
            if checkers.is_dict(value):
                try:
                    value = Response.new_from_dict(value)
                except ValueError:
                    try:
                        value = Reference.new_from_dict(value)
                    except ValueError:
                        raise ValueError('value must be a Response instance, '
                                         'Reference instance, or compatible dict '
                                         'but was: %s' % type(value))
            elif not checkers.is_type(value, ('Response', 'Reference')):
                raise ValueError('value must be a Response instance, '
                                 'Reference instance, or compatible dict '
                                 'but was: %s' % type(value))

        super(Responses, self).__setitem__(name, value)

    def __contains__(self, value):
        return super(Responses, self).__contains__(value)

    def to_dict(self, *args, **kwargs):
        """Output the contents of the object to a :class:`dict <python:dict>` object.

        :returns: :class:`dict <python:dict>` object whose keys conform to the
          Specification Extension pattern defined in the OpenAPI Specification
        :rtype: :class:`dict <python:dict>`

        """
        output = {}
        for key in self:
            value = self[key]
            if hasattr(value, 'to_json'):
                value = value.to_json(*args, **kwargs)

            output[key] = value

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    def add_to_dict(self, obj, *args, **kwargs):
        """Serialize the collection and add its serialized keys to ``obj``.

        :param obj: The :class:`dict <python:dict>` to which the collection should be
          added.
        :type obj: :class:`dict <python:dict>`

        :returns: ``obj`` extended by serialized key/value pairs from the instance
        :rtype: :class:`dict <python:dict>`

        :raises ValueError: if ``obj`` is not a :class:`dict <python:dict>`
        """
        obj = validators.dict(obj, allow_empty = True)
        if not obj:
            obj = {}

        output = self.to_dict(*args, **kwargs)
        for key in output:
            obj[key] = output[key]

        return obj

    def to_json(self, serialize_function = None, **kwargs):
        """Return a JSON representation of the object.

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

        dict_obj = self._to_dict()
        result = serialize_function(dict_obj, **kwargs)

        return result

    def to_yaml(self,
                serialize_function = None,
                **kwargs):
        """Return a YAML representation of the object.

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

        as_dict = self._to_dict()
        result = serialize_function(as_dict, **kwargs)

        return result

    @classmethod
    def new_from_dict(cls, dict_object):
        """Create a new :class:`Responses` object from a :class:`dict <python:dict>`.

        :param dict_object: A :class:`dict <python:dict>` that contains the extension
          properties.
        :type dict_object: :class:`dict <python:dict>`

        :returns: :class:`Responses` object
        :rtype: :class:`Responses`
        """
        copied_obj = validators.dict(dict_object, allow_empty = True)
        if not copied_obj:
            copied_obj = {}

        output = cls()
        for key in copied_obj:
            if key == 'extensions':
                output.extensions = Extensions.new_from_dict(copied_obj, **kwargs)
            else:
                value = copied_obj.pop(key, None)
                output[key] = value

        return output

    @classmethod
    def new_from_json(cls,
                      input_data,
                      deserialize_function = None,
                      **kwargs):
        """Create a new :class:`Responses` object from a JSON string.

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

        :returns: A :class:`Responses` representation of ``input_data``.
        :rtype: :class:`Responses`
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
        """De-serialize YAML data into a :class:`Responses` object

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

        :returns: :class:`Responses` representation of ``input_data``
        :rtype: :class:`Responses`
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
        copied_obj = validators.dict(input_data, allow_empty = True)
        if not copied_obj:
            copied_obj = {}

        for key in copied_obj:
            if key != 'extensions':
                value = copied_obj.pop(key)
                self[key] = value

        if copied_obj and self.extensions:
            self.extensions.update_from_dict(copied_obj)
        elif copied_obj:
            self.extensions = copied_obj

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


__all__ = [
    'Responses',
    'Response'
]
