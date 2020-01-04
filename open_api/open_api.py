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

from open_api.Server import Server
from open_api.info import Info, License, Contact
from open_api.utility_classes import Markup, Extensions, ManagedList
from open_api.utility_functions import parse_json, parse_yaml

class OpenAPI(object):
    """Object representation of an :term:`OpenAPI` document."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required
        self._openapi_version = '3.0.2'
        self._info = None

        self._servers = None

        self._external_documentation = None

    @property
    def openapi_version(self):
        """The `semantic version number <https://semver.org/spec/v2.0.0.html>`_ of the
        OpenAPI Specification that is used for the document. Defaults to ``'3.0.2'``.

        :rtype: :class:`str <python:str>`
        """
        return self._openapi_version

    @openapi_version.setter
    def openapi_version(self, value):
        value = validators.string(value, allow_empty = False)
        version_parts = value.split('.')
        if len(version_parts) != 3:
            raise ValueError('value must be a three-part semantic version number using '
                             'the format MAJOR.MINOR.PATCH. Received: {}'.format(value))

        major_version = validators.integer(version_parts[0])
        if major_version < 3:
            raise ValueError('OpenAPI for Python only supports OpenAPI v.3.0 and higher')

        self._openapi_version = value

    @property
    def title(self):
        """The title (name) given to the API. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info:
            return None

        return self._info.title

    @title.setter
    def title(self, value):
        if not self._info:
            self._info = Info(title = value)
        else:
            self._info.title = value

    @property
    def description(self):
        """A description of the API. Defaults to :obj:`None <python:None>`.

        Supports markup expressed in :term:`CommonMark` or :term:`ReStructuredText`.

        :rtype: :class:`Markup <open_api.utility_classes.Markup>` /
          :obj:`None <python:None>`
        """
        if not self._info:
            return None

        return self._info.description

    @description.setter
    def description(self, value):
        if not self._info:
            self._info = Info(description = value)
        else:
            self._info.description = value

    @property
    def terms_of_service(self):
        """URL to the :term:`Terms of Service` that apply to the API. Defaults to
        :obj:`None <python:None>`.

        .. note::

          Must be in the form of a URL.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info:
            return None

        return self._info.terms_of_service

    @terms_of_service.setter
    def terms_of_service(self, value):
        if not self._info:
            self._info = Info(terms_of_service = value)
        else:
            self._info.terms_of_service = value

    @property
    def contact_name(self):
        """The name of the contact person or organization for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info or not self._info.contact:
            return None

        return self._info.contact.name

    @contact_name.setter
    def contact_name(self, value):
        if not self._info or not self._info.contact:
            self._info = Info(contact = Contact(name = value))
        elif not self._info.contact:
            self._info.contact = Contact(name = value)
        else:
            self._info.contact.name = value

    @property
    def contact_url(self):
        """URL pointing to the contact information for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info or not self._info.contact:
            return None

        return self._info.contact.url

    @contact_url.setter
    def contact_url(self, value):
        if not self._info or not self._info.contact:
            self._info = Info(contact = Contact(url = value))
        elif not self._info.contact:
            self._info.contact = Contact(url = value)
        else:
            self._info.contact.url = value

    @property
    def contact_email(self):
        """The email address of the contact person/organization for the API. Defaults to
        :obj:`None <python:None>`

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info or not self._info.contact:
            return None

        return self._info.contact.email

    @contact_email.setter
    def contact_email(self, value):
        if not self._info or not self._info.contact:
            self._info = Info(contact = Contact(email = value))
        elif not self._info.contact:
            self._info.contact = Contact(email = value)
        else:
            self._info.contact.email = value


    @property
    def license_name(self):
        """The name of the license applied to the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info or not self._info.license:
            return None

        return self._info.license.name

    @license_name.setter
    def license_name(self, value):
        if not self._info or not self._info.license:
            self._info = Info(license = Licese(name = value))
        elif not self._info.license:
            self._info.license = License(name = value)
        else:
            self._info.license.name = value

    @property
    def license_url(self):
        """URL pointing to the license information for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info or not self._info.license:
            return None

        return self._info.license.url

    @license_url.setter
    def license_url(self, value):
        if not self._info or not self._info.license:
            self._info = Info(license = Licese(url = value))
        elif not self._info.license:
            self._info.license = License(url = value)
        else:
            self._info.license.url = value

    @property
    def version(self):
        """The version of API that the document represents.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self._info:
            return None

        return self._info.version

    @version.setter
    def version(self, value):
        if not self._info or not self._info:
            self._info = Info(version = value)
        else:
            self._info.version = value

    @property
    def servers(self):
        """Collection of :class:`Server` objects which provide connectivity information to
        the API.

        .. note::

          If no ``servers`` are specified, the default value would be a :class:`Server`
          with a URL value of ``/``.

        :rtype: :class:`ManagedList` of :class:`Server` objects
        """
        if not self._servers:
            return ManagedList(Server(url = '/'))

        return self._servers

    @servers.setter
    def servers(self, value):
        if not value:
            self._servers = None
            return

        if value and checkers.is_dict(value):
            value = [Server.new_from_dict(value)]
        elif value and checkers.is_iterable(value):
            new_iterable = []
            for item in value:
                if checkers.is_type(value, 'Server'):
                    new_iterable.append(item)
                elif checkers.is_dict(value):
                    new_iterable.append(Server.new_from_dict(item))
                else:
                    raise ValueError('value expected to be a Server object, compatible '
                                     'dict, or a list of Server objects or compatible '
                                     'dicts. Was: %s' % item.__class__.__name__)

            value = [x for x in new_iterable]
        elif value and checkers.is_type(value, Server):
            value = [value]

        self._servers = ManagedList(*value)

    @property
    def external_documentation(self):
        """A reference to external documentation for the API.

        :rtype: :class:`ExternalDocumentation` / :obj:`None <python:None>`
        """
        return self._external_documentation

    @external_documentation.setter
    def external_documentation(self, value):
        if not value:
            self._external_documentation = None
        else:
            if not checkers.is_type(value, 'ExternalDocumentation'):
                try:
                    value = ExternalDocumentation.new_from_dict(value)
                except ValueError:
                    raise ValueError('value must be an ExternalDocumentation object'
                                     ' or compatible dict, but was: %s' % value)

            self._external_documentation = value



    @property
    def is_valid(self):
        """``True`` if the object is valid per the OpenAPI Specification.
        Othwerise, ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        is_valid = True

        # Operation objects:
        ## TODO: Check Operation objects to see if they are valid.
        ## TODO: Check Operation objects to see if they have unique operation_id values
        ## TODO: Check each Operation object to see if it contains duplicate Parameters

        return is_valid


    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the OpenAPI object
        compliant with the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>`_.

        :returns: A :class:`dict <python:dict>` representation of the OpenAPI object
          compliant with the
          `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>`_
        :rtype: :class:`dict <python:dict>`
        """
        output = {
            'openapi': self.openapi_version,
            'info': None,
            'externalDocs': None
        }

        if self.info is not None:
            output['info'] = self._info.to_dict(*args, **kwargs)

        if self.external_documentation is not None:
            output['externalDocs'] = self.external_documentation.to_dict(*args,
                                                                         **kwargs)

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
