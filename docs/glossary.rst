**********
Glossary
**********

.. glossary::

  JavaScript Object Notation (JSON)
    A lightweight data-interchange format that has become the *de facto* standard
    for communication across internet-enabled APIs.

    For a formal definition, please see the
    `ECMA-404 Standard: JSON Data Interchange Syntax <http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf>`_

  De-serialization
    De-Serialization - as you can probably guess - is the reverse of
    :term:`serialization`. It's the process whereby data is received in one format
    (say a JSON string) and is converted into a Python object that you can more easily
    work with in your Python code.

    Think of it this way: A web app written in JavaScript needs to ask your Python
    code to register a user. Your Python code will need to know that user's details
    to register the user. So how does the web app deliver that information to your
    Python code? It'll most typically send JSON - but your Python code will need
    to then de-serialize (translate) it from JSON into an object representation
    (your ``User`` object) that it can work with.

  OpenAPI
    An OpenAPI document (which may be a single file or a collection of files) is a human
    and machine-readable formal description of a REST API that conforms to the
    `OpenAPI Specification v.3.0 <https://github.com/OAI/OpenAPI-Specification/>`_ or
    later.

    Per the `OpenAPI Initiative <https://www.openapis.org/>`_:

      The OpenAPI Specification (OAS) defines a standard, programming language-agnostic
      interface description for REST APIs, which allows both humans and computers to
      discover and understand the capabilities of a service without requiring access to
      source code, additional documentation, or inspection of network traffic.

      When properly defined via OpenAPI, a consumer can understand and interact with the
      remote service with a minimal amount of implementation logic. Similar to what
      interface descriptions have done for lower-level programming, the OpenAPI
      Specification removes guesswork in calling a service.

    The specification is a community-driven open source collaboration within the
    `OpenAPI Inititative <http://www.openapis.org>`_, a Linux Foundation Collaborative
    Project.

  Serialization
    Serialization is a process where a Python object is converted into a different format,
    typically more suited to transmission to or interpretation by some other program.

    Think of it this way: You've got a virtual representation of some information
    in your Python code. It's an object that you can work with in your Python code.
    But how do you give that information to some other application (like a web app)
    written in JavaScript? You serialize (translate) it into a format that other
    language can understand.

  Swagger
    Swagger was an earlier form of the
    `OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification/>`_ that was
    donated by SmartBear to the `OpenAPI Initiative <https://www.openapis.org/>`_ in
    2015. The Swagger v.2.0 format was formally re-named the OpenAPI Specification v.2.0
    and formed the basis for the development of the current
    `OpenAPI Specification v.3.0 <https://github.com/OAI/OpenAPI-Specification/>`_.

  YAML Ain't a Markup Language (YAML)
    YAML is a text-based data serialization format similar in some respects to
    :term:`JSON <JavaScript Object Notation (JSON)>`. For more information, please
    see the `YAML 1.2 (3rd Edition) Specification <http://yaml.org/spec/1.2/spec.html>`_.

    .. note::

      If we're being absolutely formal, JSON is actually a subset of YAML's syntax.
      But that's being needlessly formal.
