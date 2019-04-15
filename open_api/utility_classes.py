# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member function documentation is automatically incorporated
# there as needed.

from validator_collection import validators
import pypandoc

SUPPORTED_FORMATS = [
    'commonmark',
    'rst',
    'gfm'
]

class Markup(str):
    """A :class:`str <python:str>` subclass that has methods to convert its content to
    other markup :class:`str <python:str>` formats."""

    _markup_format = None

    def __new__(cls, content, **kwargs):
        str_obj = super(Markup, cls).__new__(cls, content)
        str_obj.markup_format = kwargs.pop('markup_format', 'commonmark')

        return str_obj

    def __getattribute__(self, name):
        if name in dir(str):
            def method(self, *args, **kwargs):
                value = getattr(super(), name)(*args, **kwargs)
                if isinstance(value, str):
                    return type(self)(value, markup_format = self.markup_format)
                elif isinstance(value, list):
                    return [type(self)(x, markup_format = self.markup_format) for x in value]
                elif isinstance(value, tuple):
                    return (type(self)(x, markup_format = self.markup_format) for x in value)
                else:
                    return value
            return method.__get__(self)
        else:
            return super().__getattribute__(name)

    @property
    def markup_format(self):
        """The format in which the string content is stored. Either ``'commonmark'``,
        ``'gfm'``, or ``'rst'``. Defaults to ``'commonmark'``.

        :rtype: :class:`str <python:str>`
        """
        if not self._markup_format:
            return 'commonmark'

        return self._markup_format

    @markup_format.setter
    def markup_format(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.lower()
            if value not in SUPPORTED_FORMATS:
                raise ValueError('value ("{}") is not a recognized format'.format(value))

        self._markup_format = value

    def _to_format(self, target, trim = True):
        """Convert the content to the specified target format.

        :param target: The target format to convert the content to.
        :type target: :class:`str <python:str>`

        :param trim: If ``True``, trim whitespace from either end of the resulting string.
          Defaults to ``True``.
        :type trim: :class:`bool <python:bool>`

        :returns: The converted content.
        :rtype: :class:`Markup`
        """
        if self.markup_format == target and trim:
            return self.strip()
        elif self.markup_format == target:
            return self

        converted_text = pypandoc.convert_text(self, target, self.markup_format).strip()
        result = Markup(converted_text, markup_format = target)

        return result

    def to_markdown(self, github_flavor = False):
        """Convert the content into :term:`Markdown`.

        :param github_flavor: If ``True``, converts to
          `Github-flavored Markdown <https://help.github.com/articles/github-flavored-markdown/>`_.
          If ``False``, converts to `Commonmark <http://commonmark.org/>`_. Defaults to
          ``False``.
        :type github_flavor: :class:`bool <python:bool>`

        :returns: The content converted into :term:`Markdown`.
        :rtype: :class:`Markup`

        """
        if github_flavor:
            target = 'gfm'
        else:
            target = 'commonmark'

        return self._to_format(target = target)

    def to_rst(self):
        """Convert the content into :term:`ReStructuredText`.

        :returns: The content converted into :term:`ReStructuredText`.
        :rtype: :class:`Markup`
        """
        return self._to_format(target = 'rst')
