# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, OpenAPIObject
from open_api.schema import Schemas
from open_api.responses import NamedResponses
from open_api.parameter import Parameters, Headers
from open_api.examples.Examples import Examples
from open_api.paths import RequestBodies, Callbacks
from open_api.security_scheme import SecuritySchemes
from open_api.link import Links

class Components(OpenAPIObject):
    """Holds a set of reusable objects for different aspects of the Specification.

    .. note::

      All objects defined within the components object will have no effect on
      the API unless they are explicitly referenced from properties outside the
      :class:`Components` object.

    """

    def __init__(self, *args, **kwargs):
        self._schemas = None
        self._responses = None
        self._parameters = None
        self._examples = None
        self._request_bodies = None
        self._headers = None
        self._security_schemes = None
        self._links = None
        self._callbacks = None

        self.request_bodies = kwargs.pop('request_bodies', None) or \
                              kwargs.pop('requestBodies', None)
        self.security_schemes = kwargs.pop('security_schemes', None) or \
                                kwargs.pop('securitySchemes', None)

        super().__init__(*args, **kwargs)

    @property
    def schemas(self):
        """Object to hold reusable :class:`Schema` definitions.

        :rtype: :class:`Schemas` / :obj:`None <python:None>`
        """
        return self._schemas

    @schemas.setter
    def schemas(self, value):
        if not value:
            value = None
        elif not isinstance(value, Schemas):
            value = validators.dict(value, allow_empty = False)
            value = Schemas.new_from_dict(value)

        self._schemas = value

    @property
    def responses(self):
        """Object to hold reusable :class:`Response` definitions.

        :rtype: :class:`Responses` / :obj:`None <python:None>`
        """
        return self._responses

    @responses.setter
    def responses(self, value):
        if not value:
            value = None
        elif not isinstance(value, NamedResponses):
            value = validators.dict(value, allow_empty = False)
            value = NamedResponses.new_from_dict(value)

        self._responses = value

    @property
    def parameters(self):
        """Object to hold reusable :class:`Parameter` definitions.

        :rtype: :class:`Parameters` / :obj:`None <python:None>`
        """
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if not value:
            value = None
        elif not isinstance(value, Parameters):
            value = validators.dict(value, allow_empty = False)
            value = Parameters.new_from_dict(value)

        self._parameters = value

    @property
    def examples(self):
        """Object to hold reusable :class:`Example` definitions.

        :rtype: :class:`Examples` / :obj:`None <python:None>`
        """
        return self._examples

    @examples.setter
    def examples(self, value):
        if not value:
            value = None
        elif not isinstance(value, Examples):
            value = validators.dict(value, allow_empty = False)
            value = Examples.new_from_dict(value)

        self._examples = value

    @property
    def request_bodies(self):
        """Object to hold reusable :class:`RequestBody` definitions.

        :rtype: :class:`RequestBodies` / :obj:`None <python:None>`
        """
        return self._request_bodies

    @request_bodies.setter
    def request_bodies(self, value):
        if not value:
            value = None
        elif not isinstance(value, RequestBodies):
            value = validators.dict(value, allow_empty = False)
            value = RequestBodies.new_from_dict(value)

        self._request_bodies = value

    @property
    def headers(self):
        """Object to hold reusable :class:`Header` definitions.

        :rtype: :class:`Headers` / :obj:`None <python:None>`
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        if not value:
            value = None
        elif not isinstance(value, Headers):
            value = validators.dict(value, allow_empty = False)
            value = Headers.new_from_dict(value)

        self._headers = value

    @property
    def security_schemes(self):
        """Object to hold reusable :class:`SecurityScheme` definitions.

        :rtype: :class:`SecuritySchemes` / :obj:`None <python:None>`
        """
        return self._security_schemes

    @security_schemes.setter
    def security_schemes(self, value):
        if not value:
            value = None
        elif not isinstance(value, SecuritySchemes):
            value = validators.dict(value, allow_empty = False)
            value = SecuritySchemes.new_from_dict(value)

        self._security_schemes = value

    @property
    def links(self):
        """Object to hold reusable :class:`Link` definitions.

        :rtype: :class:`Links` / :obj:`None <python:None>`
        """
        return self._links

    @links.setter
    def links(self, value):
        if not value:
            value = None
        elif not isinstance(value, Links):
            value = validators.dict(value, allow_empty = False)
            value = Links.new_from_dict(value)

        self._links = value

    @property
    def callbacks(self):
        """Object to hold reusable :class:`Callback` definitions.

        :rtype: :class:`Callbacks` / :obj:`None <python:None>`
        """
        return self._callbacks

    @callbacks.setter
    def callbacks(self, value):
        if not value:
            value = None
        elif not isinstance(value, Callbacks):
            value = validators.dict(value, allow_empty = False)
            value = Callbacks.new_from_dict(value)

        self._callbacks = value

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'schemas': None,
            'responses': None,
            'parameters': None,
            'examples': None,
            'requestBodies': None,
            'headers': None,
            'securitySchemes': None,
            'links': None,
            'callbacks': None
        }

        if self.schemas:
            output['schemas'] = self.schemas.to_dict()
        if self.responses:
            output['responses'] = self.responses.to_dict()
        if self.parameters:
            output['parameters'] = self.parameters.to_dict()
        if self.examples:
            output['examples'] = self.examples.to_dict()
        if self.request_bodies:
            output['requestBodies'] = self.request_bodies.to_dict()
        if self.headers:
            output['headers'] = self.headers.to_dict()
        if self.security_schemes:
            output['securitySchemes'] = self.security_schemes.to_dict()
        if self.links:
            output['links'] = self.links.to_dict()
        if self.callbacks:
            output['callbacks'] = self.callbacks.to_dict()

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Components` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Security Scheme
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Components` object
        :rtype: :class:`Components`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        schemas = copied_obj.pop('schemas', None)
        responses = copied_obj.pop('responses', None)
        parameters = copied_obj.pop('parameters', None)
        examples = copied_obj.pop('examples', None)
        request_bodies = copied_obj.pop('requestBodies', None) or \
                         copied_obj.pop('request_bodies', None)
        headers = copied_obj.pop('headers', None)
        security_schemes = copied_obj.pop('securitySchemes', None) or \
                           copied_obj.pop('security_schemes', None)
        links = copied_obj.pop('links', None)
        callbacks = copied_obj.pop('callbacks', None)

        if copied_obj:
            extensions = copied_obj
        else:
            extensions = None

        output = cls(schemas = schemas,
                     responses = responses,
                     parameters = parameters,
                     examples = examples,
                     request_bodies = request_bodies,
                     headers = headers,
                     security_schemes = security_schemes,
                     links = links,
                     callbacks = callbacks,
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

        if 'schemas' in copied_obj:
            self.schemas = copied_obj.pop('schemas', None)
        if 'responses' in copied_obj:
            self.responses = copied_obj.pop('responses', None)
        if 'parameters' in copied_obj:
            self.parameters = copied_obj.pop('parameters', None)
        if 'examples' in copied_obj:
            self.examples = copied_obj.pop('examples', None)
        if 'request_bodies' in copied_obj or 'requestBodies' in copied_obj:
            self.request_bodies = copied_obj.pop('requestBodies', None) or \
                                  copied_obj.pop('request_bodies', None)
        if 'headers' in copied_obj:
            self.headers = copied_obj.pop('headers', None)
        if 'security_schemes' in copied_obj or 'securitySchemes' in copied_obj:
            self.security_schemes = copied_obj.pop('securitySchemes', None) or \
                                    copied_obj.pop('security_schemes', None)
        if 'links' in copied_obj:
            self.links = copied_obj.pop('links', None)
        if 'callbacks' in copied_obj:
            self.callbacks = copied_obj.pop('callbacks', None)

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
