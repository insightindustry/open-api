# -*- coding: utf-8 -*-
"""Python Serialization and De-serialization for OpenAPI 3.0 documents
"""

import os

# Get the version number from the _version.py file
version_dict = {}
with open(os.path.join(os.path.dirname(__file__), '__version__.py')) as version_file:
    exec(version_file.read(), version_dict)                                     # pylint: disable=W0122

__version__ = version_dict.get('__version__')
