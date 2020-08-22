# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.utility_functions import validate_url

from open_api.errors import TooLongParameterContentError

class OAuthFlow(OpenAPIObject):
    """Configuration details for a supported OAuth Flow.
    """

    def __init__(self, *args, **kwargs):
        self._authorization_url = None
        self._token_url = None
        self._refresh_url = None
        self.scopes = None

        self.authorization_url = kwargs.pop('authorizationUrl', None) or \
                                 kwargs.pop('authorization_url', None)
        self.token_url = kwargs.pop('tokenUrl', None) or \
                         kwargs.pop('token_url', None)
        self.refresh_url = kwargs.pop('refreshUrl', None) or \
                           kwargs.pop('refresh_url', None)
        self.scopes = kwargs.pop('scopes', None)

        super().__init__(*args, **kwargs)

    @property
    def authorization_url(self):
        """The authorization URL to be used for this flow. **REQUIRED**

        .. note::

          This URL applies to the ``oauth2`` :attr:`SecurityScheme.type_``, and
          to the ``implicit`` and ``authorization_code`` flows defined for the
          :class:`SecurityScheme``.

        .. caution::

          This **MUST** be in the form of a URL.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        """
        return self._authorization_url

    @authorization_url.setter
    def authorization_url(self, value):
        self._authorization_url = validators.url(value,
                                                 allow_empty = True,
                                                 allow_special_ips = True)

    @property
    def token_url(self):
        """The token URL to be used for this flow. **REQUIRED**

        .. note::

          This URL applies to the ``oauth2`` :attr:`SecurityScheme.type_``, and
          to the ``password``, ``client_credentials``, and ``authorization_code``
          flows defined for the :class:`SecurityScheme``.

        .. caution::

          This **MUST** be in the form of a URL.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        """
        return self._token_url

    @token_url.setter
    def token_url(self, value):
        self._token_url = validators.url(value,
                                         allow_empty = True,
                                         allow_special_ips = True)

    @property
    def refresh_url(self):
        """The URL to be used for obtaining refresh tokens.

        .. note::

          This URL applies to the ``oauth2`` :attr:`SecurityScheme.type_``.

        .. caution::

          This **MUST** be in the form of a URL.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        """
        return self._refresh_url

    @refresh_url.setter
    def refresh_url(self, value):
        self._refresh_url = validators.url(value,
                                           allow_empty = True,
                                           allow_special_ips = True)

    @property
    def scopes(self):
        """A map (:class:`dict <python:dict>`) of the available scopes for the
        OAuth2 :class:`SecurityScheme`.

        Keys represent the naem of the scope, represented as
        :class:`str <python:str>` objects. Values are a short description of the
        scope, also represented as :class:`str <python:str>`.

        :rtype: :class:`dict <python:dict>` with :class:`str <python:str>` keys
          and :class:`str <python:dict>` values / :obj:`None <python:None>`

        """
        return self._scopes

    @scopes.setter
    def scopes(self, value):
        value = validators.dict(value, allow_empty = True)
        interim_dict = {}
        if value:
            for key in value:
                item_key = validators.string(key, allow_empty = False)
                item_value = validators.string(value[key], allow_empty = True)

                interim_dict[item_key] = item_value

        self._scopes = interim_dict

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'authorizationUrl': self.authorization_url,
            'tokenUrl': self.token_url,
            'refreshUrl': self.refresh_url,
            'scopes': {}
        }

        if self.scopes:
            output['scopes'] = self.scopes

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`OauthFlow` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Oauth Flow
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`OAuthFlow` object
        :rtype: :class:`OAuthFlow`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        authorization_url = copied_obj.pop('authorizationUrl', None) or \
                            copied_obj.pop('authorization_url', None)
        token_url = copied_obj.pop('tokenUrl', None) or \
                    copied_obj.pop('token_url', None)
        refresh_url = copied_obj.pop('refreshUrl', None) or \
                      copied_obj.pop('refresh_url', None)
        scopes = copied_obj.pop('scopes', None)

        output = cls(authorization_url = authorization_url,
                     token_url = token_url,
                     refresh_url = refresh_url,
                     scopes = scopes)

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

        if 'authorizationUrl' in copied_obj or 'authorization_url' in copied_obj:
            self.authorization_url = copied_obj.pop('authorizationUrl', None) or \
                                     copied_obj.pop('authorization_url', None)
        if 'tokenUrl' in copied_obj or 'token_url' in copied_obj:
            self.token_url = copied_obj.pop('tokenUrl', None) or \
                             copied_obj.pop('token_url', None)
        if 'refreshUrl' in copied_obj or 'refresh_url' in copied_obj:
            self.refresh_url = copied_obj.pop('refreshUrl', None) or \
                               copied_obj.pop('refresh_url', None)
        if 'scopes' in copied_obj:
            self.scopes = copied_obj.pop('scopes', None)

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        is_valid = self.authorization_url is not None and \
                   self.token_url is not None

        if not is_valid:
            return False

        return is_valid
