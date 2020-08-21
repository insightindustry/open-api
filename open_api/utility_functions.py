# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

import string as string_
import yaml
from abnf import Rule as ABNFRule
from abnf import ParseError
from abnf.grammars.misc import load_grammar_rules
import re

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

from validator_collection import validators, checkers
from validator_collection import errors as validator_errors
from validator_collection._compat import basestring

from open_api.errors import DeserializationError, InvalidRuntimeExpressionError, InvalidKeyError

COMPONENT_MAP_KEY_REGEX = re.compile(r"^[a-zA-Z0-9\.\-_]+$")

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


def validate_url(value,
                 allow_empty = False,
                 allow_special_ips = False,
                 **kwargs):
    """Validate that ``value`` is a valid URL with bracketed variable names.

    .. note::

      URL validation is...complicated. The methodology that we have
      adopted here is *generally* compliant with
      `RFC 1738 <https://tools.ietf.org/html/rfc1738>`_,
      `RFC 6761 <https://tools.ietf.org/html/rfc6761>`_,
      `RFC 2181 <https://tools.ietf.org/html/rfc2181>`_  and uses a combination of
      string parsing and regular expressions,

      This approach ensures more complete coverage for unusual edge cases, while
      still letting us use regular expressions that perform quickly.

    :param value: The value to validate.
    :type value: :class:`str <python:str>` / :obj:`None <python:None>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :param allow_special_ips: If ``True``, will succeed when validating special IP
      addresses, such as loopback IPs like ``127.0.0.1`` or ``0.0.0.0``. If ``False``,
      will raise a :class:`InvalidURLError` if ``value`` is a special IP address. Defaults
      to ``False``.
    :type allow_special_ips: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises CannotCoerceError: if ``value`` is not a :class:`str <python:str>` or
      :obj:`None <python:None>`
    :raises InvalidURLError: if ``value`` is not a valid URL or
      empty with ``allow_empty`` set to ``True``

    """
    is_recursive = kwargs.pop('is_recursive', False)

    if value is not None:
        test_value = value.lower()
        test_value = test_value.replace(':{', '').replace('{', '').replace('}', '')
    else:
        test_value = None

    has_protocol = False
    for protocol in validators.URL_PROTOCOLS:
        try:
            if test_value.startswith(protocol):
                has_protocol = True
                break
        except AttributeError:
            break

    if not has_protocol and checkers.is_pathlike(test_value) and '://' not in test_value:
        return value

    test_value = validators.url(test_value,
                                allow_empty = allow_empty,
                                allow_special_ips = allow_special_ips,
                                is_recursive = is_recursive)

    if not test_value:
        return test_value

    return value


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


def traverse_dict(content, target, parent_list = None):
    """Traverse ``content`` looking for ``target``.

    :param content: The :class:`dict <python:dict>` to traverse looking for
      ``target``.
    :type content: :class:`dict <python:dict>`

    :param target: The :class:`dict <python:dict>` or the
      :class:`str <python:str>` key value to look for in ``content``.
    :type target: :class:`dict <python:dict>`

    :param parent_list: The list of path items that preceded ``content`` being
      evaluated. Defaults to :obj:`None <python:None>`
    :type parent_list: :class:`list <python:list>` of :class:`str <python:str>` /
      :obj:`None <python:None>`

    :returns: The list of path components to resolve ``target_object``.
    :rtype: :class:`list <python:list>` of :class:`str <python:str>`

    :raises ValueError: if ``content`` is not a :class:`dict <python:dict>`
    :raises ValueError: if ``target`` is not a :class:`dict <python:dict>`
    """
    if not checkers.is_dict(content):
        raise ValueError('content must be a dict. Was: %s' % type(content))
    if not checkers.is_dict(target) and not checkers.is_string(target):
        raise ValueError('target must be a dict or str. Was: %s' % type(target))

    path_list = []

    for key in content:
        path_item = key
        value = content[key]
        if path_item == target or checkers.are_equivalent(value, target):
            if parent_list:
                path_list.extend(parent_list)
            path_list.append(path_item)
            break

        if checkers.is_dict(value):
            if parent_list:
                parent_list.append(path_item)
            else:
                parent_list = [path_item]
            internal_path_list = traverse_dict(content = value,
                                               target = target,
                                               parent_list = parent_list)
            if internal_path_list:
                path_list.extend(internal_path_list)
                break

    return path_list


def validate_runtime_expression(value, allow_empty = False):
    """Validate ``value`` against the formal definition of an OpenAPI Specification
    :term:`Runtime Expression`.

    .. note::

      The following ABNF grammer is used to parse against:

      .. code-block:: ebnf

        expression = ( "$url" / "$method" / "$statusCode" / "$request." source / "$response." source )
        source = ( header-reference / query-reference / path-reference / body-reference )
        header-reference = "header." token
        query-reference = "query." name
        path-reference = "path." name
        body-reference = "body" ["#" json-pointer ]
        json-pointer    = *( "/" reference-token )
        reference-token = *( unescaped / escaped )
        unescaped       = %x00-2E / %x30-7D / %x7F-10FFFF
          ; %x2F ('/') and %x7E ('~') are excluded from 'unescaped'
        escaped         = "~" ( "0" / "1" )
          ; representing '~' and '/', respectively
        name = *( CHAR )
        token = 1*tchar
        tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "." /
          "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA

    :param value: The value to validate.
    :type value: :class:`str <python:str>`

    :param allow_empty: If ``True``, returns :obj:`None <python:None>` if
      ``value`` is empty. If ``False``, raises a
      :class:`EmptyValueError <validator_collection.errors.EmptyValueError>`
      if ``value`` is empty. Defaults to ``False``.
    :type allow_empty: :class:`bool <python:bool>`

    :returns: ``value`` / :obj:`None <python:None>`
    :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

    :raises EmptyValueError: if ``value`` is empty and ``allow_empty`` is ``False``
    :raises InvalidRuntimeExpressionError: if ``value`` is not a valid
      :term:`Runtime Expression` or empty with ``allow_empty`` set to ``True``

    """
    if not value and not allow_empty:
        raise errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    @load_grammar_rules()
    class RuntimeExpressionGrammar(ABNFRule):
        """ABNF Grammar for OpeNAPI :term:`Runtime Expressions <Runtime Expression>`.
        Defined as per: `https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#runtimeExpression`_
        """

        grammar = [
            'expression = ( "$url" / "$method" / "$statusCode" / "$request." source / "$response." source )',
            'source = ( header-reference / query-reference / path-reference / body-reference )',
            'header-reference = "header." token',
            'query-reference = "query." name',
            'path-reference = "path." name',
            'body-reference = "body" ["#" json-pointer ]',
            'json-pointer    = *( "/" reference-token )',
            'reference-token = *( unescaped / escaped )',
            'unescaped       = %x00-2E / %x30-7D / %x7F-10FFFF',
              # %x2F ('/') and %x7E ('~') are excluded from 'unescaped'
            'escaped         = "~" ( "0" / "1" )',
              # ; representing '~' and '/', respectively
            'name = *( CHAR )',
            'token = 1*tchar',
            'tchar = "!" / "#" / "$" / "%" / "&" / "\'" / "*" / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA'

        ]

    parser = RuntimeExpressionGrammar('expression')

    try:
        parser.parse_all(value)
    except ParseError as error:
        raise InvalidRuntimeExpressionError('expression (%s) is not a valid Runtime Expression' % value)

    return value


def validate_component_map_key(value, allow_empty = False):
    if not value and not allow_empty:
        raise validator_errors.EmptyValueError('value (%s) was empty' % value)
    elif not value:
        return None

    is_valid = COMPONENT_MAP_KEY_REGEX.fullmatch(value)

    if not is_valid:
        raise InvalidKeyError(
            'value (%s) is not a valid Component map key' % value
        )

    return value
