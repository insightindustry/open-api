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
from open_api.utility_classes import Markup, Extensions, ManagedList
from open_api.utility_functions import parse_json, parse_yaml

class OpenAPI(object):
    """Object representation of an :term:`OpenAPI` document."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required
        self._openapi_version = '3.0.2'
        self._info_title = None
        self._info_version = None

        # Not Required
        self._info_description = None
        self._info_terms_of_service = None

        self._info_contact_name = None
        self._info_contact_url = None
        self._info_contact_email = None
        self._info_contact_extensions = None

        self._info_license_name = None
        self._info_license_url = None
        self._info_license_extensions = None

        self._info_extensions = None

        self._servers = None

        self._external_documentation_description = None
        self._external_documentation_url = None
        self._external_documentation_extensions = None


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
        return self._info_title

    @title.setter
    def title(self, value):
        value = validators.string(value, allow_empty = True)
        self._info_title = value

    @property
    def description(self):
        """A description of the API. Defaults to :obj:`None <python:None>`.

        Supports markup expressed in :term:`CommonMark` or :term:`ReStructuredText`.

        :rtype: :class:`Markup <open_api.utility_classes.Markup>` /
          :obj:`None <python:None>`
        """
        return self._info_description

    @description.setter
    def description(self, value):
        if checkers.is_type(value, str) and not checkers.is_type(value, Markup):
            value = Markup(value)

        if checkers.is_type(value, Markup):
            self._info_description = value
        else:
            raise ValueError('value must be either a string or a Markup object. '
                             'Was: {}'.format(value.__class__.__name__))

    @property
    def terms_of_service(self):
        """URL to the :term:`Terms of Service` that apply to the API. Defaults to
        :obj:`None <python:None>`.

        .. note::

          Must be in the form of a URL.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_terms_of_service

    @terms_of_service.setter
    def terms_of_service(self, value):
        self._info_terms_of_service = validators.url(value,
                                                     allow_empty = True,
                                                     allow_special_ips = True)

    @property
    def contact_name(self):
        """The name of the contact person or organization for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_contact_name

    @contact_name.setter
    def contact_name(self, value):
        self._info_contact_name = validators.string(value, allow_empty = True)

    @property
    def contact_url(self):
        """URL pointing to the contact information for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_contact_url

    @contact_url.setter
    def contact_url(self, value):
        self._info_contact_url = validators.url(value,
                                                allow_empty = True,
                                                allow_special_ips = True)

    @property
    def contact_email(self):
        """The email address of the contact person/organization for the API. Defaults to
        :obj:`None <python:None>`

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_contact_email

    @contact_email.setter
    def contact_email(self, value):
        self._info_contact_email = validators.email(value, allow_empty = True)

    @property
    def contact_extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        contact information for the API. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._info_contact_extensions

    @contact_extensions.setter
    def contact_extensions(self, value):
        if checkers.is_type(value, 'Extensions'):
            self._info_contact_extensions = value
        elif checkers.is_dict(value):
            value = Extensions.new_from_dict(value)
            self._info_contact_extensions = Extensions.new_from_dict(value)
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

            self._info_contact_extensions = Extensions.new_from_dict(value)

    @property
    def license_name(self):
        """The name of the license applied to the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_license_name

    @license_name.setter
    def license_name(self, value):
        self._info_license_name = validators.string(value, allow_empty = True)

    @property
    def license_url(self):
        """URL pointing to the license information for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_license_url

    @license_url.setter
    def license_url(self, value):
        self._info_license_url = validators.url(value,
                                                allow_empty = True,
                                                allow_special_ips = True)

    @property
    def license_extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        license information for the API. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._info_license_extensions

    @license_extensions.setter
    def license_extensions(self, value):
        if checkers.is_type(value, 'Extensions'):
            self._info_license_extensions = value
        elif checkers.is_dict(value):
            value = Extensions.new_from_dict(value)
            self._info_license_extensions = Extensions.new_from_dict(value)
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

            self._info_license_extensions = Extensions.new_from_dict(value)

    @property
    def version(self):
        """The version of API that the document represents.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._info_version

    @version.setter
    def version(self, value):
        self._info_version = validators.string(value, allow_empty = True)

    @property
    def info_extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        ``info`` block information for the API. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._info_extensions

    @info_extensions.setter
    def info_extensions(self, value):
        if checkers.is_type(value, 'Extensions'):
            self._info_extensions = value
        elif checkers.is_dict(value):
            value = Extensions.new_from_dict(value)
            self._info_extensions = value
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

            value = Extensions.new_from_dict(value)

            self._info_extensions = value

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
    def external_documentation_description(self):
        """A short description of the external documentation.

        Supports markup expressed in :term:`CommonMark` or :term:`ReStructuredText`.

        :rtype: :class:`Markup <open_api.utility_classes.Markup>` /
          :obj:`None <python:None>`
        """
        return self._external_documentation_description

    @external_documentation_description.setter
    def external_documentation_description(self, value):
        if checkers.is_type(value, str) and not checkers.is_type(value, Markup):
            value = Markup(value)

        if checkers.is_type(value, Markup):
            self._external_documentation_url = value
        else:
            raise ValueError('value must be either a string or a Markup object. '
                             'Was: {}'.format(value.__class__.__name__))

    @property
    def external_documentation_url(self):
        """The URL where external documentation may be accessed.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._external_documentation_url

    @external_documentation_url.setter
    def external_documentation_url(self, value):
        self._external_documentation_url = validators.url(value, allow_empty = True)

    @property
    def external_documentation_extensions(self):
        """Collection of :term:`Specification Extensions` that have been applied to the
        ``external_documentation`` block for the API. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`Extensions` / :obj:`None <python:None>`
        """
        return self._external_documentation_extensions

    @external_documentation_extensions.setter
    def external_documentation_extensions(self, value):
        if checkers.is_type(value, 'Extensions'):
            self._external_documentation_extensions = value
        elif checkers.is_dict(value):
            value = Extensions.new_from_dict(value)
            self._external_documentation_extensions = value
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

            value = Extensions.new_from_dict(value)

            self._external_documentation_extensions = value



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
            'info': {
                'title': self.title,
                'description': self.description,
                'termsOfService': self.terms_of_service,
                'contact': {
                    'name': self.contact_name,
                    'url': self.contact_url,
                    'email': self.contact_email
                },
                'license': {
                    'name': self.license_name,
                    'url': self.license_url
                },
                'version': self.version
            },
            'externalDocs': {
                'description': self.external_documentation_description,
                'url': self.external_documentation_url
            }
        }

        if self.contact_extensions is not None:
            output['info']['contact'] = self.contact_extensions.add_to_dict(
                output['info']['contact'],
                *args,
                **kwargs
            )
        if not (self.contact_name and \
                self.contact_url and \
                self.contact_email and \
                self.contact_extensions):
            del output['info']['contact']

        if self.license_extensions is not None:
            output['info']['license'] = self.license_extensions.add_to_dict(
                output['info']['license'],
                *args,
                **kwargs
            )
        if not (self.license_name and self.license_url and self.license_extensions):
            del output['info']['license']

        if self.external_documentation_extensions is not None:
            output['externalDocs'] = self.external_documentation_extensions.add_to_dict(
                output['externalDocs'],
                *args,
                **kwargs
            )
        if not (self.external_documentation_description and \
                self.external_documentation_url and \
                self.external_documentation_extensions):
            del output['externalDocs']




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
