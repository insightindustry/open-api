# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from open_api.schemas.encoding import Encoding
from open_api.schemas.media_type import MediaType
from open_api.schemas.xml import XML
from open_api.schemas.discriminator import Discriminator
from open_api.schemas.schema import Schema
from open_api.schemas.schemas import Schemas

__all__ = [
    'Encoding',
    'MediaType',
    'XML',
    'Discriminator',
    'Schema',
    'Schemas'
]
