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
import pypandoc

from open_api.utility_functions import parse_json, parse_yaml

SUPPORTED_FORMATS = [
    'commonmark',
    'rst',
    'gfm'
]

class Markup(str):
    """A :class:`str <python:str>` subclass that has methods to convert its content to
    other markup :class:`str <python:str>` formats."""

    _markup_format = None

    def __new__(cls, content, **kwargs):
        if '\r\n' in content:
            content = content.replace('\r\n', '\n')

        str_obj = super(Markup, cls).__new__(cls, content)
        str_obj.markup_format = kwargs.pop('markup_format', 'commonmark')

        return str_obj

    def __getattribute__(self, name):
        if name in dir(str):
            def method(self, *args, **kwargs):
                value = getattr(super(), name)(*args, **kwargs)
                if isinstance(value, str):
                    return type(self)(value,
                                      markup_format = self.markup_format)
                if isinstance(value, list):
                    return [type(self)(x,
                                       markup_format = self.markup_format) for x in value]
                if isinstance(value, tuple):
                    return (type(self)(x,
                                       markup_format = self.markup_format) for x in value)

                return value
            return method.__get__(self)

        return super().__getattribute__(name)

    @property
    def markup_format(self):
        """The format in which the string content is stored. Either ``'commonmark'``,
        ``'gfm'``, or ``'rst'``. Defaults to ``'commonmark'``.

        :rtype: :class:`str <python:str>`
        """
        if not self._markup_format:
            return 'commonmark'

        return self._markup_format

    @markup_format.setter
    def markup_format(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.lower()
            if value not in SUPPORTED_FORMATS:
                raise ValueError('value ("{}") is not a recognized format'.format(value))

        self._markup_format = value

    def _to_format(self, target, trim = True):
        """Convert the content to the specified target format.

        :param target: The target format to convert the content to.
        :type target: :class:`str <python:str>`

        :param trim: If ``True``, trim whitespace from either end of the resulting string.
          Defaults to ``True``.
        :type trim: :class:`bool <python:bool>`

        :returns: The converted content.
        :rtype: :class:`Markup`
        """
        if self.markup_format == target and trim:
            return self.strip()
        if self.markup_format == target:
            return self

        converted_text = pypandoc.convert_text(self, target, self.markup_format).strip()
        if '\r\n' in converted_text:
            converted_text = converted_text.replace('\r\n', '\n')

        result = Markup(converted_text, markup_format = target)

        return result

    def to_markdown(self, github_flavor = False):
        """Convert the content into :term:`Markdown`.

        :param github_flavor: If ``True``, converts to
          `Github-flavored Markdown <https://help.github.com/articles/github-flavored-markdown/>`_.
          If ``False``, converts to `Commonmark <http://commonmark.org/>`_. Defaults to
          ``False``.
        :type github_flavor: :class:`bool <python:bool>`

        :returns: The content converted into :term:`Markdown`.
        :rtype: :class:`Markup`

        """
        if github_flavor:
            target = 'gfm'
        else:
            target = 'commonmark'

        return self._to_format(target = target)

    def to_rst(self):
        """Convert the content into :term:`ReStructuredText`.

        :returns: The content converted into :term:`ReStructuredText`.
        :rtype: :class:`Markup`
        """
        return self._to_format(target = 'rst')


class Extensions(dict):
    """Collection of :term:`Specification Extensions`.

    Implemented as a subclass of :class:`dict <python:dict>`, and serializes using the
    ``x-<extension-name>`` pattern defined by the OpenAPI Specification.
    """

    def __getattribute__(self, name):
        if name.startswith('x-'):
            return self[name[2:]]

        return self[name]

    def __setattr__(self, name, value):
        if name.startswith('x-'):
            self[name[2:]] = value
        else:
            self[name] = value

    def __delitem__(self, key):
        if key.startswith('x-'):
            super(Extensions, self).__delitem__(key[2:])
        else:
            super(Extensions, self).__delitem__(key)

    def __getitem__(self, name):
        if name.startswith('x-'):
            return self[name[2:]]

        return self[name]

    def __setitem__(self, name, value):
        if name.startswith('x-'):
            super(Extensions, self).__setitem__(name[2:], value)
        else:
            super(Extensions, self).__setitem__(name, value)

    def __contains__(self, value):
        if value.startswith('x-'):
            return super(Extensions, self).__contains__(value[2:])

        return super(Extensions, self).__contains__(value)

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

            output['x-{}'.format(key)] = value

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

    def to_json(self,
                serialize_function = None,
                **kwargs):
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
        """Create a new :class:`Extensions` object from a :class:`dict <python:dict>`.

        :param dict_object: A :class:`dict <python:dict>` that contains the extension
          properties.
        :type dict_object: :class:`dict <python:dict>`

        :returns: :class:`Extensions` object
        :rtype: :class:`Extensions`
        """
        dict_object = validators.dict(dict_object, allow_empty = True)
        if not dict_object:
            dict_object = {}

        output = cls()
        for key in dict_object:
            value = dict_object[key]
            if key.startswith('x-'):
                key = key[2:]
            output[key] = value

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

        :returns: A :class:`Extensions` representation of ``input_data``.
        :rtype: :class:`Extensions`
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
        """De-serialize YAML data into a :class:`Extensions` object

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

        :returns: :class:`Extensions` representation of ``input_data``
        :rtype: :class:`Extensions`
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

        for key in input_data:
            value = input_data[key]
            if key.startswith('x-'):
                self[key[2:]] = value
            else:
                self[key] = value

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
