# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.errors import UnsupportedPropertyError

from open_api.utility_classes import Extensions, ManagedList, Reference, OpenAPIObject
from open_api.utility_functions import validate_url

class Discriminator(OpenAPIObject):
    """A discriminator is a specific object in a :class:`Schema` which is used
    to inform the consumer of the specification of an alternative :class:`Schema`
    based on the value associated with it.

    .. hint::

      Think of a ``Discriminator`` as a way of saying "if the value of property
      ``X`` is equal to ``Y``, then the object should conform to the
      :class:`Schema` ``Q``, but if ``X`` is equal to ``Z``, then the object
      should conform to :class:`Schema` ``T``."

    """

    def __init__(self, *args, **kwargs):
        self._property_name = None
        self._mapping = None

        super().__init__(*args, **kwargs)

    @property
    def property_name(self):
        """The name of the property in the payload that will hold the
        discriminator value.

        .. hint::

          This is the name of the property whose value determines which
          :class:`Schema` should be applied to the mapped properties.

        :rtype: :class:`str <python:str>`

        """
        return self._property_name

    @property_name.setter
    def property_name(self, value):
        self._property_name = validators.string(value, allow_empty = True)

    @property
    def mapping(self):
        """A :class:`dict <python:dict>` which maps values of
        the property named in :attr:`property_name <Discriminator.property_name>`
        to the :class:`Schema` which should be applied.

        Keys in the :class:`dict <python:dict>` should represent the string
        values to apply within :attr:`property_name <Discriminator.property_name>`,
        while values should then be
        :class:`Reference <open_api.utility_classes.Reference>` objects pointing
        to the :class:`Schema` which should apply.

        :rtype: :class:`dict <python:dict>` where keys are strings and values are
          :class:`Reference <open_api.utility_classes.Reference>` objects /
          :obj:`None <python:None>`

        :raises UnsupportedPropertyError: when attempting to set a mapping value
          to :obj:`None <python:None>` or an improperly-formed :class:`Reference`
          (or string convertible into a :class:`Reference`).

        """
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        mapping_dict = {}
        if not value:
            self._mapping = None
        else:
            value = validators.dict(value)
            for key in value:
                key = validators.string(key, allow_empty = False)
                if value[key] and not checkers.is_type(value[key], 'Reference'):
                    item_dict = None
                    if checkers.is_dict(value[key]):
                        item_dict = value[key]
                    elif checkers.is_string(value[key]):
                        item_dict = {
                            '$ref': value[key]
                        }
                    else:
                        item_dict = None
                    if not item_dict:
                        raise UnsupportedPropertyError(
                            'Mapping for "{}" cannot be empty.'.format(key)
                        )

                    item_reference = Reference.new_from_dict(item_dict)

                    mapping_dict[key] = item_reference
                elif checkers.is_type(value[key], 'Reference'):
                    mapping_dict[key] = value[key]
                else:
                    raise UnsupportedPropertyError(
                        'Mapping for "{}" cannot be empty.'.format(key)
                    )

            self._mapping = mapping_dict


    def to_dict(self, *args, **kwargs):
        """Return a :class:`dict <python:dict>` representation of the object.

        :rtype: :class:`dict <python:dict>` / :obj:`None <python:None>`
        """
        output = {
            'propertyName': self.property_name,
        }

        if self.mapping:
            output['mapping'] = {}
            for key in self.mapping:
                if item.is_valid:
                    output['mapping'][key] = item.json_reference
                else:
                    output['mapping'][key] = item.target

        return output

    @classmethod
    def new_from_dict(cls, obj, **kwargs):
        """Create a new :class:`Discriminator` object from a :class:`dict <python:dict>`.

        :param obj: A :class:`dict <python:dict>` that contains the Discriminator
          properties.
        :type obj: :class:`dict <python:dict>`

        :returns: :class:`Discriminator` object
        :rtype: :class:`Discriminator`
        """
        obj = validators.dict(obj, allow_empty = True)
        copied_obj = {}
        for key in obj:
            copied_obj[key] = obj[key]

        property_name = copied_obj.pop('property_name', None) or \
                        copied_obj.pop('propertyName', None)

        mapping = copied_obj.pop('mapping', None)

        output = cls(property_name = property_name,
                     mapping = mapping)

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

        if 'property_name' in copied_obj or 'propertyName' in copied_obj:
            self.property_name = copied_obj.pop('property_name', None) or \
                                 copied_obj.pop('propertyName', None)
        if 'mapping' in copied_obj:
            self.mapping = copied_obj.get('mapping', None)

    @property
    def is_valid(self):
        """Returns ``True`` if the object is valid per the
        `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`_

        :rtype: :class:`bool <python:bool>`
        """
        return self.property_name is not None
