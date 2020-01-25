# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject, Reference, ExternalDocumentation
from open_api.parameter import Parameter
from open_api.paths import RequestBody
from open_api.responses import Responses
from open_api.server import Server

class Operation(OpenAPIObject):
    """Describes a single API operation on a path."""

    def __init__(self, *args, **kwargs):
        self._tags = None
        self._summary = None
        self._external_documentation = None
        self._operation_id = None
        self._parameters = None
        self._request_body = None
        self._responses = None
        self._callbacks = None
        self._deprecated = False
        self._security = None
        self._servers = None

        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def tags(self):
        """A :class:`ManagedList` of tags for API documentation control.

        Tags can be used for logical grouping of operations by resources or any
        other qualifier.

        :rtype: :class:`ManagedList` / :obj:`None <python:None>`
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        if not value:
            self._tags = None
        else:
            if not isinstance(value, ManagedList) and checkers.is_iterable(value):
                new_value = ManagedList(value)
            else:
                new_value = ManagedList()
                new_value.append(value)

            self._tags = new_value

    @property
    def summary(self):
        """A short summary of what the operation does.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = validators.string(value, allow_empty = True)

    @property
    def external_documentation(self):
        """Additional external documentation for this operation.

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
    def operation_id(self):
        """Unique string used to identify the operation.

        .. note::

          The ``operation_id`` is **case-sensitive**.

        .. caution::

          Typical programming naming conventions are enforced. An
          :exc:`ValueError` will be raised if you supply a value that does not
          conform to typical variable naming.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        :raises ValueError: if an assigned value does not conform to common
          programming language naming conventions
        """
        return self._operation_id

    @operation_id.setter
    def operation_id(self, value):
        self._operation_id = validators.variable_name(value, allow_empty = True)

    @property
    def parameters(self):
        """A :class:`ManagedList` of parameters that are applicable for this
        operation.

        .. note::

          If a parameter is already defined at the :class:`PathItem`, the new
          definition will override it but can never remove it.

        :rtype: :class:`ManagedList` of :class:`Parameter` or :class:`Reference`
          instances / :obj:`None <python:None>`

        """
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if not value:
            self._parameters = None
        else:
            new_value = ManagedList()

            if not checkers.is_iterable(value):
                value = [value]

            for parameter in value:
                if not checkers.is_type(parameter, ('Parameter', 'Reference')):
                    try:
                        parameter = Parameter.new_from_dict(parameter)
                    except ValueError:
                        try:
                            parameter = Reference.new_from_dict(parameter)
                        except ValueError:
                            raise ValueError('Parameter expected to be a '
                                             'Parameter or Reference instance '
                                             ' or compatible dict. Was: %s' % type(parameter))

                new_value.append(parameter)

            self._parameters = new_value

    @property
    def request_body(self):
        """The request body applicable for this operation.

        :rtype: :class:`RequestBody` or :class:`Reference` / :obj:`None <python:None>`
        """
        return self._request_body

    @request_body.setter
    def request_body(self, value):
        if not value:
            self._request_body = None
        else:
            if not checkers.is_type(value, ('RequestBody', 'Reference')):
                try:
                    value = RequestBody.new_from_dict(value)
                except ValueError:
                    try:
                        value = Reference.new_from_dict(value)
                    except ValueError:
                        raise ValueError('Expects a RequestBody or Reference '
                                         'instance, or a compatible dict. Was: %s' % type(value))
            self._request_body = value

    @property
    def responses(self):
        """Collection of possible responses this operation may return.
        **REQUIRED**

        :rtype: :class:`Responses` / :obj:`None <python:None>`
        """
        return self._responses

    @responses.setter
    def responses(self, value):
        if not value:
            self._responses = None
        else:
            if not checkers.is_type(value, 'Responses'):
                try:
                    value = Responses.new_from_dict(value)
                except ValueError:
                    raise ValueError('Expected a Responses instance or '
                                     'compatible dict. Received: %s' % type(value))

            self._responses = value

    @property
    def callbacks(self):
        """A :class:`dict <python:dict>` of possible out-of band
        :term:`callbacks <callback>` related to the operation.

        Each key is a runtime expression that determines a unique name for a
        given callback. Values are either a :class:`Callback` instance or
        :class:`Reference` to one that describes
        a request that may be initiated by the API provider and the expected
        responses.

        :rtype: :class:`dict <python:dict>` of :class:`Callback` or
          :class:`Reference` instances / :obj:`None <python:None>`
        """
        return self._callbacks

    @callbacks.setter
    def callbacks(self, value):
        if not value:
            self._callbacks = None
        else:
            if checkers.is_dict(value):
                for key in value:
                    if not checkers.is_string(key):
                        raise ValueError('Key (%s) must be a string runtime expression.')
                    callback = value[key]
                    if not checkers.is_type(callback, ('Callback', 'Reference')):
                        try:
                            value[key] = Callback.new_from_dict(callback)
                        except ValueError:
                            try:
                                value[key] = Reference.new_from_dict(callback)
                            except ValueError:
                                raise ValueError(
                                    'Value expects a Callback or Reference '
                                    'instance, or a compatible dict. Received: '
                                    '%s' % type(value[key])
                                )
                self._callbacks = value
            else:
                raise ValueError('expected a dict, but received: %s' % type(value))

    @property
    def deprecated(self):
        """Declares this operation to be deprecated. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value):
        self._deprecated = bool(value)

    @property
    def security(self):
        """:class:`ManagedList` of security mechanisms that can be used for this
        operation.

        Only one of the security requirement objects needs to be satisfied to
        authorize a request.

        .. tip::

          This property overrides any top-level security properties applied to
          the API. A value of :obj:`None <python:None>` means that whatever
          top-level security requirements are applied to the API also apply to
          this operation, with no additional alternative mechanisms.

          You can remove a top-level security mechanism from this
          operation, submit an empty :class:`list <python:list>` or
          :class:`ManagedList`.

        :rtype: :class:`ManagedList` of :class:`SecurityRequirement` instances /
          :obj:`list <python:list>`
        """
        return self._security

    @security.setter
    def security(self, value):
        if value is None:
            self._security = None
        elif not value:
            self._security = ManagedList()
        else:
            new_value = ManagedList()
            if not checkers.is_iterable(value):
                value = [value]

            for requirement in value:
                if not checkers.is_type(requirement, 'SecurityRequirement'):
                    try:
                        requirement = SecurityRequirement.new_from_dict(requirement)
                    except ValueError:
                        raise ValueError('Requirement expected to be a '
                                         'SecurityRequirement instance '
                                         ' or compatible dict. Was: %s' % type(requirement))

                new_value.append(requirement)

            self._security = new_value

    @property
    def servers(self):
        """A collection of alternative :class:`Servers <Server>` that will service
        this operation.

        .. caution::

          If a different :class:`Server` is specified at the :class:`PathItem`
          or root level, it will be overridden by this value.

        :rtype: :class:`ManagedList` of :class:`Server` instances /
          :obj:`None <python:None>`
        """
        return self._servers

    @servers.setter
    def servers(self, value):
        if not value:
            self._servers = None
        else:
            new_value = ManagedList()

            if not checkers.is_iterable(value):
                value = [value]

            for item in value:
                if not checkers.is_type(item, 'Server'):
                    try:
                        item = Server.new_from_dict(item)
                    except ValueError:
                        raise ValueError('Expected a Server instance or '
                                         'compatible dict. Received: %s' % type(item))

                new_value.append(item)

            self._servers = new_value


    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>`
        """
        output = {
            'tags': self.tags,
            'summary': self.summary,
            'description': self.description,
            'externalDocs': None,
            'operationId': self.operation_id,
            'parameters': None,
            'requestBody': None,
            'responses': None,
            'callbacks': None,
            'deprecated': self.deprecated,
            'security': None,
            'servers': None
        }

        if self.external_documentation:
            output['externalDocs'] = self.external_documentation.to_dict(**kwargs)
        if self.parameters:
            output['parameters'] = [x.to_dict(**kwargs) for x in self.parameters]
        if self.request_body:
            output['requestBody'] = self.request_body.to_dict(**kwargs)
        if self.responses:
            output['responses'] = self.responses.to_dict(**kwargs)
        if self.callbacks:
            output['callbacks'] = {}
            for key in callbacks:
                output['callbacks'][key] = callbacks[key].to_dict(**kwargs)
        if self.security is not None:
            output['security'] = [x.to_dict(**kwargs) for x in self.security]
        if self.servers is not None:
            output['servers'] = [x.to_dict(**kwargs) for x in self.servers]

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Contact` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` representation of the Contact.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Contact` object
        :rtype: :class:`Contact`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        tags = copied_obj.pop('tags', None)
        summary = copied_obj.pop('summary', None)
        description = copied_obj.pop('description', None)
        external_documentation = copied_obj.pop('external_documentation', None) or \
                                 copied_obj.pop('externalDocs', None)
        operation_id = copied_obj.pop('operation_id', None) or \
                       copied_obj.pop('operationId', None)
        parameters = copied_obj.pop('parameters', None)
        request_body = copied_obj.pop('request_body', None) or \
                       copied_obj.pop('requestBody', None)
        responses = copied_obj.pop('responses', None)
        callbacks = copied_obj.pop('callbacks', None)
        deprecated = copied_obj.pop('deprecated', False)
        security = copied_obj.pop('security', None)
        servers = copied_obj.pop('servers', None)

        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(tags = tags,
                     summary = summary,
                     description = description,
                     external_documentation = external_documentation,
                     operation_id = operation_id,
                     parameters = parameters,
                     request_body = request_body,
                     responses = responses,
                     callbacks = callbacks,
                     deprecated = deprecated,
                     security = security,
                     servers = servers,
                     extensions = extensions)

        return output

    def update_from_dict(self, input_data):
        """Update the object representation based on the input data provided.

        :param input_data: Collection of properties to update on the object.
        :type input_data: :class:`dict <python:dict>`

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        input_data = validators.dict(input_data, allow_empty = True)
        copied_obj = {}
        for key in input_data:
            copied_obj[key] = input_data[key]

        if 'tags' in copied_obj:
            self.tags = copied_obj.pop('tags')
        if 'summary' in copied_obj:
            self.summary = copied_obj.pop('summary')
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'external_documentation' in copied_obj or 'externalDocs' in copied_obj:
            self.external_documentation = copied_obj.pop('external_documentation',
                                                         None) or \
                                          copied_obj.pop('externalDocs',
                                                         None)
        if 'operation_id' in copied_obj or 'operationId' in copied_obj:
            self.operation_id = copied_obj.pop('operation_id', None) or \
                                copied_obj.pop('operationId', None)
        if 'parameters' in copied_obj:
            self.parameters = copied_obj.pop('parameters', None)
        if 'request_body' in copied_obj or 'requestBody' in copied_obj:
            self.request_body = copied_obj.pop('request_body', None) or \
                                copied_obj.pop('requestBody', None)
        if 'responses' in copied_obj:
            self.responses = copied_obj.pop('responses', None)
        if 'callbacks' in copied_obj:
            self.callbacks = copied_obj.pop('callbacks', None)
        if 'deprecated' in copied_obj:
            self.deprecated = copied_obj.pop('deprecated', False)
        if 'security' in copied_obj:
            self.security = copied_obj.pop('security', None)
        if 'servers' in copied_obj:
            self.servers = copied_obj.pop('servers', None)

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
        if not self.responses:
            return False

        if self.parameters:
            count_dict = {}
            for index, parameter in enumerate(self.parameters):
                count_dict[index] = parameter
                for key in count_dict:
                    if key == index:
                        continue
                    if count_dict[key] == parameter:
                        return False

        return True
