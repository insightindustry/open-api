# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators, checkers

from open_api.utility_classes import Extensions, ManagedList, OpenAPIDict, Reference
from open_api.security_schemes.security_scheme import SecurityScheme
from open_api.utility_functions import validate_component_map_key

class SecurityRequirement(ManagedList):
    """A :class:`ManagedList` that contains security scopes. Each member of the
    list **MUST** be a :class:`str <python:str>` that corresponds to a scope
    defined in a :class:`SecurityScheme`.

    .. note::

      If the security scheme is of type ``oauth2`` or ``openIdConnect``, then
      the value is a list of scope names required for the execution, and the
      list may be empty if authorization does not require a specified scope.
      For other security scheme types, the array **MUST** be empty.

    """
    def __init__(self, *args, **kwargs):
        arg = args[0]
        if arg:
            iterable = [validators.string(x, allow_empty = False) for x in arg]
        else:
            iterable = []

        super(SecurityRequirement, self).__init__(iterable, **kwargs)

    def append(self, value):
        value = validators.string(value, allow_empty = False)
        super(SecurityRequirement, self).append(value)

    def extend(self, values):
        values = [validators.string(x, allow_empty = False) for x in values]
        super(SecurityRequirement, self).extend(values)

    def insert(self, index, value):
        value = validators.string(value, allow_empty = False)
        super(SecurityRequirement, self).insert(index, value)
