# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.paths.operation import Operation
from open_api.utility_classes import Extensions, ManagedList, ExternalDocumentation, Reference, OpenAPIObject
from open_api.utility_functions import validate_url

class PathItem(OpenAPIObject):
    """The Path Item Object describes the operations available on a single :term:`path`.

    .. caution::

      :class:`Paths` may be empty, due to ACL constraints.

    """

    def __init__(self, *args, **kwargs):
        self._summary = None
        self._get = None
        self._put = None
        self._post = None
        self._delete = None
        self._options = None
        self._head = None
        self._patch = None
        self._trace = None
        self._servers = None
        self._parameters = None
        self._reference = None
        self._extensions = None

        self.reference = kwargs.pop('$ref', None)
        self.get_ = kwargs.pop('get', None)

        super().__init__(*args, **kwargs)

    @property
    def summary(self):
        """String summary, intended to apply to all operations in this path

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = validators.string(value, allow_empty = True)

    @property
    def reference(self):
        """The :class:`Reference` object containing the definition of the
        :class:`PathItem`. Defaults to :obj:`None <python:None>`

        .. note::

          This property, when set, will override any other definition properties.

        :rtype: :class:`Reference` / :obj:`None <python:None>`

        """
        return self._reference

    @reference.setter
    def reference(self, value):
        if value and not checkers.is_type(value, ('Reference', str)):
            value = Reference.new_from_dict(value)
        elif isinstance(value, str):
            value = Reference(target = value)
        elif not value:
            value = None

        self._reference = value

    @property
    def is_reference(self):
        """Indicates whether the :class:`PathItem` definition is contained in
        a separate (referenced) item.

        :rtype: :class:`bool <python:bool>`
        """
        return self._reference is not None

    @property
    def get_(self):
        """Definition of the ``GET`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._get

    @get_.setter
    def get_(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._get = value

    @property
    def put(self):
        """Definition of the ``PUT`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._put

    @put.setter
    def put(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._put = value

    @property
    def post(self):
        """Definition of the ``POST`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._post

    @post.setter
    def post(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._post = value

    @property
    def delete(self):
        """Definition of the ``DELETE`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._delete

    @delete.setter
    def delete(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._delete = value

    @property
    def options(self):
        """Definition of the ``GET`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._options

    @options.setter
    def options(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._options = value


    @property
    def head(self):
        """Definition of the ``DELETE`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._head

    @head.setter
    def head(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._head = value

    @property
    def trace(self):
        """Definition of the ``DELETE`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._trace

    @trace.setter
    def trace(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._trace = value

    @property
    def patch(self):
        """Definition of the ``DELETE`` operation at this path.

        :rtype: :class:`Operation` / :obj:`None <python:None>`
        """
        return self._patch

    @patch.setter
    def patch(self, value):
        if not isinstance(value, Operation):
            value = Operation.new_from_dict(value)
        self._patch = value

    @property
    def servers(self):
        """An alternative array of :class:`Server` values that can service all
        operations for this path.

        :rtype: :class:`list <python:list>` of :class:`Server` objects

        """
        return self._servers

    @servers.setter
    def servers(self, value):
        items = ManagedList()
        if value:
            if checkers.is_type(value, list) and not checkers.is_type(value,
                                                                      'ManagedList'):
                items.extend(value)

            if not checkers.is_type(value, 'ManagedList'):
                raise ValueError('value must be a Server, list, or ManagedList. '
                                 'Was: %s' % value.__class__.__name__)

            for item in value:
                if not checkers.is_type(item, ('Server', 'dict')):
                    raise ValueError('items must be a Server object or '
                                     'compatible dict. Was: %s' % item.__class__.__name__)
                elif not checkers.is_type(item, 'Server'):
                    items.append(Server.new_from_dict(item))
                else:
                    items.append(item)

        self._servers = items

    @property
    def parameters(self):
        """A list of parameters that are applicable for all the operations
        described under this path.

        .. caution::

          These parameters can be overridden at the operation level, but cannot
          be removed there.

        :rtype: :class:`list <python:list>` of :class:`Parameter` or
          :class:`Reference` objects

        """
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        items = ManagedList()
        if value:
            if checkers.is_type(value, ('Parameter', 'Reference')):
                value = [value]

            if checkers.is_type(value, list) and not checkers.is_type(value,
                                                                      'ManagedList'):
                items.extend(value)

            if not checkers.is_type(value, 'ManagedList'):
                raise ValueError('value must be a Parameter, Reference, list, or ManagedList. '
                                 'Was: %s' % value.__class__.__name__)

            for item in value:
                if not checkers.is_type(item, ('Parameter', 'Reference', 'dict')):
                    raise ValueError('items must be a Parameter, Reference, or '
                                     'compatible dict object. Was: %s' % item.__class__.__name__)
                elif checkers.is_type(item, dict):
                    try:
                        new_item = Parameter.new_from_dict(item)
                    except (ValueError, TypeError):
                        try:
                            new_item = Reference.new_from_dict(item)
                        except (ValueError, TypeError):
                            raise ValueError('items must be a Parameter, Reference, or '
                                             'compatible dict object. Was: %s' % item.__class__.__name__)
                    items.append(new_item)

                else:
                    items.append(new_item)

        self._parameters = items

    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {}
        if self.is_reference:
            output['$ref'] = self.reference.json_reference
        else:
            output['summary'] = self.summary
            output['description'] = self.description

            if self.get_:
                output['get'] = self.get_.to_dict()
            else:
                output['get'] = None
            if self.put:
                output['put'] = self.put.to_dict()
            else:
                output['put'] = None
            if self.post:
                output['post'] = self.post.to_dict()
            else:
                output['post'] = None
            if self.delete:
                output['delete'] = self.delete.to_dict()
            else:
                output['delete'] = None
            if self.options:
                output['options'] = self.options.to_dict()
            else:
                output['options'] = None
            if self.head:
                output['head'] = self.head.to_dict()
            else:
                output['head'] = None
            if self.patch:
                output['patch'] = self.patch.to_dict()
            else:
                output['patch'] = None
            if self.trace:
                output['trace'] = self.trace.to_dict()
            else:
                output['trace'] = None

            if self.servers:
                output['servers'] = [x.to_dict() for x in self.servers]
            else:
                output['servers'] = []

            if self.parameters:
                output['parameters'] = [x.to_dict() for x in self.parameters]
            else:
                output['parameters'] = []

            if self.extensions is not None:
                output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`PathItem` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the :class:`PathItem`
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`PathItem` object
        :rtype: :class:`PathItem`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        reference = copied_obj.pop('$ref', None)

        summary = copied_obj.pop('summary', None)
        description = copied_obj.pop('description', None)

        get_ = copied_obj.pop('get', None)
        put = copied_obj.pop('put', None)
        post = copied_obj.pop('post', None)
        delete = copied_obj.pop('delete', None)
        options = copied_obj.pop('options', None)
        head = copied_obj.pop('head', None)
        patch = copied_obj.pop('patch', None)
        trace = copied_obj.pop('trace', None)
        servers = copied_obj.pop('servers', [])
        parameters = copied_obj.pop('parameters', [])

        if copied_obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        if reference:
            output = cls(reference = reference)
        else:
            output = cls(summary = summary,
                         description = description,
                         get_ = get_,
                         put = put,
                         post = post,
                         delete = delete,
                         options = options,
                         head = head,
                         patch = patch,
                         trace = trace,
                         servers = servers,
                         parameters = parameters,
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

        if self.reference:
            self.reference = copied_obj.pop('$ref', self.reference.json_reference)
        else:
            self.reference = copied_obj.pop('$ref', None)

        self.summary = copied_obj.pop('summary', self.summary)
        self.description = copied_obj.pop('description', self.description)

        self.get_ = copied_obj.pop('get', self.get_)
        self.put = copied_obj.pop('put', self.put)
        self.post = copied_obj.pop('post', self.post)
        self.delete = copied_obj.pop('delete', self.delete)
        self.options = copied_obj.pop('options', self.options)
        self.head = copied_obj.pop('head', self.head)
        self.patch = copied_obj.pop('patch', self.patch)
        self.trace = copied_obj.pop('trace', self.trace)
        self.servers = copied_obj.pop('servers', self.servers)
        self.parameters = copied_obj.pop('parameters', self.parameters)

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
        if self.is_reference:
            return True

        return self.get_ is not None or \
               self.put is not None or \
               self.post is not None or \
               self.delete is not None or \
               self.options is not None or \
               self.head is not None or \
               self.patch is not None
