# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.security_scheme.OAuthFlow import OAuthFlow
from open_api.utility_classes import Extensions, OpenAPIObject

class OAuthFlows(OpenAPIObject):
    """Collection of configuration details for different OAuth Flow modalities.
    """

    def __init__(self, *args, **kwargs):
        self._implicit = None
        self._password = None
        self._client_credentials = None
        self._authorization_code = None

        self.client_credentials = kwargs.pop('client_credentials', None) or \
                                  kwargs.pop('clientCredentials', None)
        self.authorization_code = kwargs.pop('authorization_code', None) or \
                                  kwargs.pop('authorizationCode', None)

        super().__init__(*args, **kwargs)

    @property
    def implicit(self):
        """Configuration for the OAuth Implicit flow.

        :rtype: :class:`OAuthFlow`

        """
        return self._implicit

    @implicit.setter
    def implicit(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'OAuthFlow'):
            value = validators.dict(value, allow_empty = False)
            value = OAuthFlow.new_from_dict(value)

        self._implicit = value

    @property
    def password(self):
        """Configuration for the OAuth Password flow.

        :rtype: :class:`OAuthFlow`

        """
        return self._password

    @password.setter
    def password(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'OAuthFlow'):
            value = validators.dict(value, allow_empty = False)
            value = OAuthFlow.new_from_dict(value)

        self._password = value

    @property
    def client_credentials(self):
        """Configuration for the OAuth Client Credentials flow.

        .. note::

          Previously called ``application`` in OpenAPI 2.0 (a.k.a. Swagger).

        :rtype: :class:`OAuthFlow`

        """
        return self._client_credentials

    @client_credentials.setter
    def client_credentials(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'OAuthFlow'):
            value = validators.dict(value, allow_empty = False)
            value = OAuthFlow.new_from_dict(value)

        self._client_credentials = value

    @property
    def authorization_code(self):
        """Configuration for the OAuth Authorization Code flow.

        .. note::

          Previously called ``accessCode`` in OpenAPI 2.0 (a.k.a. Swagger)

        :rtype: :class:`OAuthFlow`

        """
        return self._authorization_code

    @authorization_code.setter
    def authorization_code(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'OAuthFlow'):
            value = validators.dict(value, allow_empty = False)
            value = OAuthFlow.new_from_dict(value)

        self._authorization_code = value

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'implicit': None,
            'password': None,
            'clientCredentials': None,
            'authorizationCode': None
        }

        if self.implicit:
            output['implicit'] = self.implicit.to_dict(**kwargs)
        if self.password:
            output['password'] = self.password.to_dict(**kwargs)
        if self.client_credentials:
            output['clientCredentials'] = self.client_credentials.to_dict(**kwargs)
        if self.authorization_code:
            output['authorizationCode'] = self.authorization_code.to_dict(**kwargs)

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`OauthFlows` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Oauth Flow
          configurations.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`OAuthFlows` object
        :rtype: :class:`OAuthFlows`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        implicit = copied_obj.pop('implicit', None)
        password = copied_obj.pop('password', None)
        client_credentials = copied_obj.pop('client_credentials', None) or \
                             copied_obj.pop('clientCredentials', None)
        authorization_code = copied_obj.pop('authorization_code', None) or \
                             copied_obj.pop('authorizationCode', None)

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(implicit = implicit,
                     password = password,
                     client_credentials = client_credentials,
                     authorization_code = authorization_code,
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
        copied_obj = {}
        for key in input_data:
            copied_obj[key] = input_data[key]

        if 'implicit' in copied_obj:
            self.implicit = copied_obj.pop('implicit', None)
        if 'password' in copied_obj:
            self.password = copied_obj.pop('password', None)
        if 'client_credentials' in copied_obj or 'clientCredentials' in copied_obj:
            self.client_credentials = copied_obj.pop('client_credentials', None) or \
                                      copied_obj.pop('clientCredentials', None)
        if 'authorization_code' in copied_obj or 'authorizationCode' in copied_obj:
            self.authorization_code = copied_obj.pop('authorization_code', None) or \
                                      copied_obj.pop('authorizationCode', None)

        if copied_obj and self.extensions:
            self.extensions.update_from_dict(copied_obj)
        elif copied_obj:
            self.extensions = copied_obj

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        return True
