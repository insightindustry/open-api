# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIObject
from open_api.paths.RequestBody import RequestBody
from open_api.paths.Operation import Operation

class Paths(OpenAPIObject):
    """Object representation of a :term:`Paths` object.

    Holds the relative paths to the individual endpoints and their operations.
    The path is appended to the URL from the :class:`Server` Object in order to
    construct the full URL.

    .. caution::

      :class:`Paths` may be empty, due to ACL constraints.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'title': self.title,
            'description': self.description,
            'termsOfService': self.terms_of_service,
            'contact': None,
            'license': None,
            'version': self.version
        }
        if self.contact:
            output['contact'] = self.contact.to_dict()
        if self.license:
            output['license'] = self.license.to_dict()

        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Info` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the object
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Info` object
        :rtype: :class:`Info`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        title = copied_obj.pop('title', None)
        description = copied_obj.pop('description', None)
        terms_of_service = copied_obj.pop('terms_of_service', None) or \
                           copied_obj.pop('termsOfService', None)
        contact = copied_obj.pop('contact', None)
        license = copied_obj.pop('license', None)
        version = copied_obj.pop('version', None)
        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(title = title,
                     description = description,
                     terms_of_service = terms_of_service,
                     contact = contact,
                     license = license,
                     version = version,
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

        if 'title' in copied_obj:
            self.title = copied_obj.pop('title')
        if 'description' in copied_obj:
            self.description = copied_obj.pop('description')
        if 'terms_of_service' in copied_obj or 'termsOfService' in copied_obj:
            self.terms_of_service = copied_obj.pop('terms_of_service', None) or \
                                    copied_obj.pop('termsOfService', None)

        if 'contact' in copied_obj:
            self.contact = copied_obj.pop('contact')
        if 'license' in copied_obj:
            self.license = copied_obj.pop('license')
        if 'version' in copied_obj:
            self.version = copied_obj.pop('version')

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
        is_valid = self.title is not None and \
                   self.version is not None and \
                   (self.extensions is None or self.extensions.is_valid)

        return is_valid

__all__ = [
    'Paths',
    'RequestBody'
]
