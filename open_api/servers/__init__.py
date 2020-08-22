# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from open_api.servers.server_variable import ServerVariable
from open_api.servers.server import Server

__all__ = [
    'Server',
    'ServerVariable'
]
