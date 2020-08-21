# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member class documentation is automatically incorporated
# there as needed.

class OpenAPIError(ValueError):
    """Base error that all other errors inherit from.

    **INHERITS FROM:** :exc:`ValueError <python:ValueError>`
    """
    pass

class DeserializationError(OpenAPIError):
    """Exception raised when :term:`de-serialization` fails.

    **INHERITS FROM:** :class:`ValueError <python:ValueError>`

    """
    pass

class UnsupportedPropertyError(OpenAPIError):
    """Exception raised when the user attempts to access (or set) a property on an OpenAPI
    object that is not supported per the
    `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md>`_.

    """
    pass

class InvalidRuntimeExpressionError(OpenAPIError):
    """Exception raised when validating a :term:`Runtime Expression` fails because it does not conform
    to the ABNF grammar.

    """
    pass
