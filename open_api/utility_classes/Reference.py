# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes.OpenAPIObject import OpenAPIObject

class Reference(OpenAPIObject):
    """A simple object to allow referencing other components in the specification,
    internally and externally.

    """

    def __init__(self, *args, **kwargs):
        self._specification = None
        self._target = None
        self._external_reference = None

        if '$ref' in kwargs:
            kwargs['target'] = kwargs.pop('$ref')

        super().__init__(*args, **kwargs)

    @property
    def specification(self):
        """The :class:`OpenAPI` specification that the reference is attached
        to. Defaults to :obj:`None <python:None>`.

        If :obj:`None <python:None>`, then expects a :class:`str <python:str>`
        value.

        :rtype: :class:`OpenAPI` / :obj:`None <python:None>`
        """
        return self._specification

    @specification.setter
    def specification(self, value):
        if not checkers.is_type(value, 'OpenAPI'):
            raise ValueError('value must be an OpenAPI object. '
                             'Was: %s' % type(value))

        self._specification = value

    @property
    def target(self):
        """The object or object key name that should be referenced.

        :rtype: :class:`OpenAPIObject` / :class:`str <python:str>` /
          :obj:`None <python:None>`

        """
        return self._target

    @target.setter
    def target(self, value):
        if checkers.is_type(value, 'OpenAPIObject'):
            self._target = value
            self.external_reference = None
        elif checkers.is_string(value):
            self._target = value
            self.external_reference = None
        elif not value:
            self._target = None
        else:
            raise ValueError('target must be an OpenAPIObject, a string, or None.'
                             ' Was: %s' % type(value))

    @property
    def external_reference(self):
        """The string of a reference that is external to the OpenAPI Specification.

        Expects a file path, a URL, or :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._external_reference

    @external_reference.setter
    def external_reference(self, value):
        if not value:
            self._external_reference = None
        else:
            try:
                value = validators.url(value, allow_empty = False)
            except ValueError:
                try:
                    value = validators.path(value, allow_empty = False)
                except ValueError:
                    raise ValueError('value (%s) is not None, a valid URL, or '
                                     'a plausible path' % value)

            self._external_reference = value
            self.target = None

    @property
    def is_external(self):
        """Returns ``True`` if the reference points to an externally-defined
        object, otherwise ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._external_reference is not None

    @property
    def reference_path(self):
        """A list of the path components for ``target``.

        .. note::

          Returns :obj:`None <python:None>` if the object is an
          :term:`external reference`.

        :rtype: :class:`list <python:list>` of :class:`str <python:str>` /
          :obj:`None <python:None>`

        :raises ValueError: if ``specification`` is not a :class:`OpenAPI`
        :raises ValueError: if ``target`` is not a :class:`OpenAPIObject`
        :raises ValueError: if ``target`` is not found in ``specification``
        """
        if self.is_external:
            return None

        if not self.specification:
            raise ValueError('no specification assigned')
        if not checkers.is_type(self.target, ('OpenAPIObject', 'str')):
            raise ValueError('target_object must be an OpenAPIObject instance or '
                             'str. Was: %s' % type(target_object))

        try:
            target = self.target.to_dict()
        except AttributeError:
            target = self.target

        content = self.specification.to_dict()

        path_list = traverse_dict(content = content,
                                  target = target)

        if not path_list:
            raise ValueError('target_object was not found in specification')

        return path_list

    @property
    def json_reference(self):
        """Retrieve the JSON Reference string for the object. If not valid, will
        return :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self.is_valid:
            return None

        if self.is_external:
            return self.external_reference

        path_list = self.reference_path
        path_string = '/'.join(path_list)
        path_string = '#/' + path_string + '/'

        return path_string

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>`
        """
        output = { '$ref': self.json_reference }

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Reference` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` representation of the License.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Reference` object
        :rtype: :class:`Reference`
        """
        copied_obj = validators.dict(obj, allow_empty = True)
        path_string = copied_obj.get('$ref') or copied_obj.get('target')
        target = None
        external_reference = None

        if not path_string:
            target = None
            external_reference = None
        elif checkers.is_url(path_string) or checkers.is_pathlike(path_string):
            target = None
            external_reference = path_string
        else:
            if path_string.startswith('#'):
                path_string = path_string[2:]
            if path_string.endswidth('/'):
                path_string = path_string[:-1]
            path_list = path_string.split('/')
            target = path_list[-1]
            external_reference = None

        try:
            output = cls(target = target,
                         external_reference = external_reference)
        except TypeError:
            output = cls(target = external_reference,
                         external_reference = None)

        return output

    def update_from_dict(self, obj):
        """Update the object representation based on the input data provided.

        :param obj: Collection of properties to update on the object.
        :type obj: :class:`dict <python:dict>`

        .. note::

          If a key is present in the instance, but is not included in ``input_data``, that
          key on the instance will *not* be affected by this method.

        """
        copied_obj = validators.dict(obj, allow_empty = True)
        path_string = copied_obj.get('$ref') or copied_obj.get('target')
        target = None
        external_reference = None

        if not path_string:
            target = None
            external_reference = None
        elif checkers.is_url(path_string) or checkers.is_pathlike(path_string):
            target = None
            external_reference = path_string
        else:
            if path_string.startswith('#'):
                path_string = path_string[2:]
            if path_string.endswidth('/'):
                path_string = path_string[:-1]
            path_list = path_string.split('/')
            target = path_list[-1]
            external_reference = None

        try:
            self.target = target
            self.external_reference = external_reference
        except TypeError:
            self.target = external_reference
            self.external_reference = None

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        if not self.specification:
            return False

        if not self.target and not self.external_reference:
            return False

        return True
