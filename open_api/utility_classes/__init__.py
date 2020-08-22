# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

import yaml
from validator_collection import validators, checkers
from validator_collection.errors import MaximumValueError, MinimumValueError
import pypandoc

from open_api.utility_classes.Extensions import Extensions
from open_api.utility_classes.ExternalDocumentation import ExternalDocumentation
from open_api.utility_classes.ManagedList import ManagedList
from open_api.utility_classes.Markup import Markup
from open_api.utility_classes.OpenAPIDict import OpenAPIDict
from open_api.utility_classes.OpenAPIObject import OpenAPIObject
from open_api.utility_classes.Reference import Reference

__all__ = [
    'Extensions',
    'ExternalDocumentation',
    'ManagedList',
    'Markup',
    'OpenAPIDict',
    'OpenAPIObject',
    'Reference'
]
