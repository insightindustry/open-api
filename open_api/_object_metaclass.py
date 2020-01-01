# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import abc

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import yaml
from validator_collection import validators, checkers

from open_api.utility_classes import Markup, Extensions
from open_api.utility_functions import parse_json, parse_yaml, add_metaclass

@add_metaclass(abc.ABCMeta)
class OpenAPIObject(object):
    """A metaclass that is used to define the standard methods required by OpenAPI
    objects."""

    def __init__(self, *args, **kwargs):

        self._description = None
        self._extensions = None

        for key in kwargs:
            setattr(self, key, kwargs[key])

        super(OpenAPIObject, self).__init__(*args)


    @property
    def description(self):
        """A description of the object. Defaults to :obj:`None <python:None>`.

        Supports markup expressed in :term:`CommonMark` or :term:`ReStructuredText`.

        .. tip::

          If an OpenAPI object does not have a ``description`` property, then this should
          always raise :exc:`UnsupportedOpenAPIPropertyError`.

        :rtype: :class:`Markup <open_api.utility_classes.Markup>` /
          :obj:`None <python:None>`
        """
        return self._description

    @description.setter
    def description(self, value):
        if checkers.is_type(value, str) and not isinstance(value, Markup):
            value = Markup(value)

        if isinstance(value, (Markup, None.__class__)):
            self._description = value
        else:
            raise ValueError('value must be either a string, a Markup object, or None. '
                             'Was: {}'.format(value.__class__.__name__))

    @property
    def extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        object. Defaults to :obj:`None <python:None>`.

        .. tip::

          If an OpenAPI object does not have a ``description`` property, then this should
          always raise :exc:`UnsupportedOpenAPIPropertyError`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if not value:
            self._extensions = None
        elif checkers.is_type(value, 'Extensions'):
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

    @abc.abstractmethod
    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        An example implementation is shown below:

        .. code-block:: python

          output = {
              'default': self.default,
              'description': self.description,
              'enum': self.enum
          }
          try:
              if self.extensions is not None:
                  output = self.extensions.add_to_dict(output, **kwargs)
          except UnsupportedPropertyError:
              pass

          return output

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        raise NotImplementedError()

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
    @abc.abstractmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the extension
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`ServerVariable` object
        :rtype: :class:`ServerVariable`
        """
        raise NotImplementedError()

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

    @abc.abstractmethod
    def update_from_dict(self, input_data):
        """Update the object representation based on the input data provided.

        :param input_data: Collection of extension keys to update on the object
          representation.
        :type input_data: :class:`dict <python:dict>`

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        raise NotImplementedError()

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

        try:
            obj[getattr(self, 'name')] = self.to_dict(**kwargs)
        except AttributeError:
            pass

        return obj
