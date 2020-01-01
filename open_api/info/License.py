# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api._object_metaclass import OpenAPIObject
from open_api.utility_classes import Extensions, ManagedList

class License(OpenAPIObject):
    """Object representation of the license used for the API."""

    def __init__(self, *args, **kwargs):
        self._name = None
        self._url = None
        self._extensions = None

        super().__init__(*args, **kwargs)

    @property
    def name(self):
        """The license name used for the API. **REQUIRED**

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validators.string(value, allow_empty = True)


    @property
    def url(self):
        """The URL pointing to the text of the license.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._url

    @url.setter
    def url(self, value):
        self._url = validators.url(value,
                                   allow_empty = True,
                                   allow_special_ips = True)

    def to_dict(self, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>`
        """
        output = {
            'name': self.name,
            'url': self.url
        }
        if self.extensions is not None:
            output = self.extensions.add_to_dict(output, **kwargs)

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`License` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` representation of the License.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`License` object
        :rtype: :class:`License`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        name = copied_obj.pop('name', None)
        url = copied_obj.pop('url', None)
        if obj:
            extensions = Extensions.new_from_dict(copied_obj, **kwargs)
        else:
            extensions = None

        output = cls(name = name,
                     url = url,
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
        if 'url' in copied_obj:
            self.url = copied_obj.pop('url')

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
        return self.name is not None
