# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, OpenAPIObject
from open_api.utility_functions import validate_url, validate_runtime_expression
from open_api.link.LinkParameters import LinkParameters
from open_api.server.Server import Server

class Link(OpenAPIObject):
    """Object representation of a design-time link for a response.

    .. caution::

      The presence of a :class:`Link` does not guarantee the caller's ability to
      successfully invoke it, rather it provides a known relationship and
      traversal mechanism between responses and other operations.

      Unlike *dynamic* links (i.e. links created at runtime and provided **in**
      the response), the OAS :class:`Link` does not imply or require linking
      information be included in the runtime response itself.

    .. hint::

      In order to compute the link itself and provide execution instructions,
      the :class:`Link` object relies on either constants expressed in the
      specification or on :term:`Runtime Expressions <Runtime Expression>`.

    """

    def __init__(self, *args, **kwargs):
        self._description = None
        self._operation_ref = None
        self._operation_id = None
        self._parameters = None
        self._request_body = None
        self._server = None

        self.operation_ref = kwargs.pop('operation_ref', None) or \
                             kwargs.pop('operationRef', None)
        self.operation_id = kwargs.pop('operation_id', None) or \
                            kwargs.pop('operationId', None)
        self.request_body = kwargs.pop('request_body', None) or \
                            kwargs.pop('requestBody', None)

        super().__init__(*args, **kwargs)

    @property
    def operation_ref(self):
        """A relative or absolute URI reference to an OpenAPI operation.

        .. warning::

          This field is mutually exclusive of the :meth:`Link.operation_id` field
          and **MUST** point to a resolvable :class:`Operation` object within
          the specification.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._operation_ref

    @operation_ref.setter
    def operation_ref(self, value):
        self._operation_ref = validate_url(value, allow_empty = True)

    @property
    def operation_id(self):
        """The ``operation_id`` of an *existing* and resolvable :class:`Operation`
        defined within the OpenAPI specification.

        .. warning::

          This field is mutually exclusive of the :meth:`Link.operation_id` field
          and **MUST** point to a resolvable :class:`Operation` object within
          the specification.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = validators.variable_name(value, allow_empty = True)

    @property
    def parameters(self):
        """A :class:`dict <python:dict>` representing parameters to pass to the
        :class:`Operation` indicated by :meth:`operation_id <Link.operation_id>`
        or :meth:`operation_ref <Link.operation_ref>`.

        The key is the parameter name to be used, whereas the value can be a
        constant or a :term:`runtime expression <Runtime Expression>` to be
        evaluated and passed to the linked operation.

        .. note::

          The parameter name can be qualified using the parameter location
          ``[{in}.]{name}`` for operations that use the same parameter name in
          different locations (e.g. ``path.id``).

        :rtype: :class:`LinkParameters` object (a subclass of
          :class:`dict <python:dict>`)
        """
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'LinkParameters'):
            value = validators.dict(value, allow_empty = True)
            value = LinkParameters.new_from_dict(value)

        self._parameters = value

    @property
    def request_body(self):
        """A literal value or :term:`Runtime Expression` to use as a request
        body when calling the target :class:`Operation`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        :raises InvalidRuntimeExpressionError: if the value is a
          :term:`Runtime Expression` (wrapped in ``{...}``) but does not use
          valid Runtime Expression Syntax.

        """
        return self._request_body

    @request_body.setter
    def request_body(self, value):
        value = validators.string(value, allow_empty = True, coerce_value = True)
        if not value:
            if value.startswith('{') and value.endswith('}'):
                value = validate_runtime_expression(value, allow_empty = False)

        self._request_body = value

    @property
    def server(self):
        """A :class:`Server` to be used by the target :class:`Operation`.

        :rtype: :class:`Server` / :obj:`None <python:None>`
        """
        return self._server

    @server.setter
    def server(self, value):
        if not value:
            value = None
        elif not checkers.is_type(value, 'Server'):
            value = validators.dict(value, allow_empty = False)
            value = Server.new_from_dict(value)

        self._server = value


    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'operationRef': self.operation_ref,
            'operationId': self.operation_id,
            'parameters': None,
            'requestBody': self.request_body,
            'description': self.description,
            'server': None
        }

        if self.parameters:
            output['parameters'] = self.parameters.to_dict(**kwargs)

        if self.server:
            output['server'] = self.server.to_dict(**kwargs)

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Link` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Security Scheme
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Link` object
        :rtype: :class:`Link`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        operation_ref = copied_obj.pop('operation_ref', None) or \
                        copied_obj.pop('operationRef', None)
        operation_id = copied_obj.pop('operation_id', None) or \
                       copied_obj.pop('operationId', None)
        request_body = copied_obj.pop('request_body', None) or \
                       copied_obj.pop('requestBody', None)
        description = copied_obj.pop('description', None)
        parameters = copied_obj.pop('parameters', None)
        server = copied_obj.pop('server', None)

        if copied_obj:
            extensions = copied_obj
        else:
            extensions = None

        output = cls(operation_ref = operation_ref,
                     operation_id = operation_id,
                     request_body = request_body,
                     description = description,
                     parameters = parameters,
                     server = server,
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

        if 'operation_ref' in copied_obj or 'operationRef' in copied_obj:
            self.operation_ref = copied_obj.pop('operation_ref', None) or \
                                 copied_obj.pop('operationRef', None)
        if 'operation_id' in copied_obj or 'operationId' in copied_obj:
            self.operation_id = copied_obj.pop('operation_id', None) or \
                                copied_obj.pop('operationId', None)
        if 'request_body' in copied_obj or 'requestBody' in copied_obj:
            self.request_body = copied_obj.pop('request_body', None) or \
                                copied_obj.pop('requestBody', None)
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description', None)
        if 'parameters' in copied_obj:
            self.parameters = copied_obj.pop('parameters', None)
        if 'server' in copied_obj:
            self.server = copied_obj.pop('server', None)

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
        is_valid = (self.operation_ref is None and self.operation_id is not None) or \
                   (self.operation_ref is not None and self.operation_id is None)

        if not is_valid:
            return False

        if self.server and not self.server.is_valid:
            return False

        return is_valid
