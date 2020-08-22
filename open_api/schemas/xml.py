# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions
from open_api.utility_classes import OpenAPIObject

class XML(OpenAPIObject):
    """Object representation of an XML object used for more fine-tuned XML model
       definitions within an API :class:`Schema` object."""

    def __init__(self, *args, **kwargs):
        self._name = None
        self._namespace = None
        self._prefix = None
        self._attribute = False
        self._wrapped = False

        super().__init__(*args, **kwargs)

    @property
    def name(self):
        """The the value that overrides the name of the element/attribute used
        for the described schema property.

        .. note::

          When applied within ``items``, it will affect the name of the
          individual XML elements within the list.

          When applied alongside ``type`` being ``array`` (outside ``items``),
          it will affect the wrapping element and only if ``wrapped`` is ``True``.
          If ``wrapped`` is ``False``, it will be ignored.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validators.string(value, allow_empty = True)

    @property
    def namespace(self):
        """The URI of the namespace definition.

        .. note::

          Value MUST be in the form of an absolute URI.

        .. caution::

          This property will **NOT** validate whether the namespace is a valid
          absolute URI. Use with caution.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`

        """
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = validators.string(value, allow_empty = True)


    @property
    def prefix(self):
        """The prefix to be used in the XML representation of the element.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = validators.string(value, allow_empty = True)

    @property
    def attribute(self):
        """Indicates whether the property definition translates to an attribute
        (``True``) or an element (``False``). Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`

        """
        return self._attribute

    @attribute.setter
    def attribute(self, value):
        self._attribute = bool(value)

    @property
    def wrapped(self):
        """Indicates whether the array is wrapped (``True``, e.g.
        ``<books><book/><book/></books>``) or unwrapped (``False``, e.g.
        ``<book/><book/>``). Defaults to ``False``.

        .. note::

          The property only has an effect if used when ``type`` is ``array``
          (outside ``items``).

        :rtype: :class:`bool <python:bool>`

        """
        return self._wrapped

    @wrapped.setter
    def wrapped(self, value):
        self._wrapped = bool(value)

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>`
        """
        output = {
            'name': self.name,
            'description': self.description,
            'namespace': self.namespace,
            'prefix': self.prefix,
            'attribute': self.attribute,
            'wrapped': self.wrapped
        }
        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`XML` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` representation of the XML
          object.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`XML` object
        :rtype: :class:`XML`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        name = copied_obj.pop('name', None)
        description = copied_obj.pop('description', None)
        namespace = copied_obj.pop('namespace', None)
        prefix = copied_obj.pop('prefix', None)
        attribute = copied_obj.pop('attribute', False)
        wrapped = copied_obj.pop('wrapped', False)

        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(name = name,
                     description = description,
                     namespace = namespace,
                     prefix = prefix,
                     attribute = attribute,
                     wrapped = wrapped,
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

        if 'name' in copied_obj:
            self.name = copied_obj.pop('name')
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'namespace' in copied_obj:
            self.namespace = copied_obj.pop('namespace')
        if 'prefix' in copied_obj:
            self.prefix = copied_obj.pop('prefix')
        if 'attribute' in copied_obj:
            self.attribute = copied_obj.pop('attribute')
        if 'wrapped' in copied_obj:
            self.wrapped = copied_obj.pop('wrapped')

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
