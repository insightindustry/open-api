# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import yaml
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

from validator_collection import validators, checkers

from open_api.errors import DeserializationError

def parse_yaml(input_data,
               deserialize_function = None,
               **kwargs):
    """De-serialize YAML data into a Python :class:`dict <python:dict>` object.

    :param input_data: The YAML data to de-serialize.
    :type input_data: :class:`str <python:str>` / Path-like object

    :param deserialize_function: Optionally override the default YAML deserializer.
      Defaults to :obj:`None <python:None>`, which calls the default ``yaml.safe_load()``
      function from the `PyYAML <https://github.com/yaml/pyyaml>`_ library.

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

    :returns: A :class:`dict <python:dict>` representation of ``input_data``.
    :rtype: :class:`dict <python:dict>`
    """
    is_file = False
    if checkers.is_file(input_data):
        is_file = True

    if deserialize_function is None and not is_file:
        deserialize_function = yaml.safe_load
    elif deserialize_function is None and is_file:
        deserialize_function = yaml.safe_load
    else:
        if checkers.is_callable(deserialize_function) is False:
            raise ValueError(
                'deserialize_function (%s) is not callable' % deserialize_function
            )

    if not input_data:
        raise DeserializationError('input_data is empty')

    try:
        input_data = validators.string(input_data,
                                       allow_empty = False)
    except ValueError:
        raise DeserializationError('input_data is not a valid string')

    if not is_file:
        from_yaml = yaml.safe_load(input_data, **kwargs)
    else:
        with open(input_data, 'r') as input_file:
            from_yaml = yaml.safe_load(input_file, **kwargs)

    return from_yaml


def parse_json(input_data,
               deserialize_function = None,
               **kwargs):
    """De-serialize JSON data into a Python :class:`dict <python:dict>` object.

    :param input_data: The JSON data to de-serialize.
    :type input_data: :class:`str <python:str>` / Path-like object

    :param deserialize_function: Optionally override the default JSON deserializer.
      Defaults to :obj:`None <python:None>`, which first tries to use
      :ref:`ujson.loads() <ujson:ujson.loads>`, then falls back to
      :ref:`simplejson.loads() <simplejson:simplejson.loads>`, and finally defaults
      to the standard library's :ref:`json.loads() <python:json.loads>`
      function.

      .. note::

        Use the ``deserialize_function`` parameter to override the default
        YAML deserializer. A valid ``deserialize_function`` is expected to
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

    :returns: A :class:`dict <python:dict>` representation of ``input_data``.
    :rtype: :class:`dict <python:dict>`
    """
    is_file = False
    if checkers.is_file(input_data):
        is_file = True

    if deserialize_function is None and not is_file:
        deserialize_function = json.loads
    elif deserialize_function is None and is_file:
        deserialize_function = json.load
    else:
        if checkers.is_callable(deserialize_function) is False:
            raise ValueError(
                'deserialize_function (%s) is not callable' % deserialize_function
            )

    if not input_data:
        raise DeserializationError('input_data is empty')

    if not is_file:
        try:
            input_data = validators.string(input_data,
                                           allow_empty = False)
        except ValueError:
            raise DeserializationError('input_data is not a valid string')

        from_json = deserialize_function(input_data, **kwargs)
    else:
        with open(input_data, 'r') as input_file:
            from_json = deserialize_function(input_file, **kwargs)

    return from_json
