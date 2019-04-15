# -*- coding: utf-8 -*-

"""
***********************************
tests.test_Markup.py
***********************************

Tests for the :class:`Markup` utility class.

"""

import pytest

from open_api.utility_classes import Markup

@pytest.mark.parametrize('value, format, expected', [
    # pylint: disable=line-too-long
    ('test123', None, 'test123'),
    ('******************\nHeading Goes Here\n******************', None, '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', None, '# Heading Goes Here'),

    ('test123', 'commonmark', 'test123'),
    ('******************\nHeading Goes Here\n******************', 'commonmark', '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', 'commonmark', '# Heading Goes Here'),

    ('test123', 'rst', 'test123'),
    ('******************\nHeading Goes Here\n******************', 'rst', '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', 'rst', '# Heading Goes Here'),

    ('test123', 'gfm', 'test123'),
    ('******************\nHeading Goes Here\n******************', 'gfm', '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', 'gfm', '# Heading Goes Here'),
    # pylint: enable=line-too-long
])
def test_Markup__init__(value, format, expected):
    """Test that the Markup class instantiates correctly."""
    result = Markup(value, markup_format = format)

    assert isinstance(result, Markup) is True
    assert hasattr(result, 'markup_format')
    if not format:
        assert result.markup_format == 'commonmark'
    else:
        assert result.markup_format == format

    assert result == expected
    assert isinstance(result, str) is True
    assert len(result) == len(value)
    assert hasattr(result, 'to_markdown')
    assert hasattr(result, 'to_rst')


@pytest.mark.parametrize('value, initial_format, github_flavor, expected', [
    # pylint: disable=line-too-long
    ('test123', None, False, 'test123'),
    ('******************\nHeading Goes Here\n******************', None, False, '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', None, False, '# Heading Goes Here'),

    ('test123', 'commonmark', False, 'test123'),
    ('******************\nHeading Goes Here\n******************', 'commonmark', False, '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', 'commonmark', False, '# Heading Goes Here'),

    ('test123', 'rst', False, 'test123'),
    ('******************\nHeading Goes Here\n******************', 'rst', False, '# Heading Goes Here'),
    ('# Heading Goes Here', 'rst', False, '\\# Heading Goes Here'),

    ('test123', 'gfm', False, 'test123'),
    ('# Heading Goes Here', 'gfm', False, '# Heading Goes Here'),

    ## Github Flavor: True
    ('test123', None, True, 'test123'),
    ('******************\nHeading Goes Here\n******************', None, True, '-----\n\nHeading Goes Here\n\n-----'),
    ('# Heading Goes Here', None, True, '# Heading Goes Here'),

    ('test123', 'commonmark', True, 'test123'),
    ('******************\nHeading Goes Here\n******************', 'commonmark', True, '-----\n\nHeading Goes Here\n\n-----'),
    ('# Heading Goes Here', 'commonmark', True, '# Heading Goes Here'),

    ('test123', 'rst', True, 'test123'),
    ('******************\nHeading Goes Here\n******************', 'rst', True, '# Heading Goes Here'),
    ('# Heading Goes Here', 'rst', True, '\\# Heading Goes Here'),

    ('test123', 'gfm', True, 'test123'),
    ('# Heading Goes Here', 'gfm', True, '# Heading Goes Here'),
    # pylint: enable=line-too-long
])
def test_Markup_to_markdown(value, initial_format, github_flavor, expected):
    """Test that the ``Markup.to_markdown()`` method works correctly."""
    obj = Markup(value, markup_format = initial_format)
    markdown = obj.to_markdown(github_flavor = github_flavor)

    print('markdown: {}'.format(markdown))
    print('expected: {}'.format(expected))

    assert markdown == expected

    if github_flavor:
        expected_format = 'gfm'
    else:
        expected_format = 'commonmark'

    assert markdown.markup_format == expected_format

    target = initial_format or 'commonmark'

    result = obj._to_format(target = target, trim = True)                                 # pylint: disable=W0212

    assert result == obj


@pytest.mark.parametrize('value, initial_format, expected', [
    # pylint: disable=line-too-long
    ('test123', None, 'test123'),
    ('******************\nHeading Goes Here\n******************', None, '--------------\n\nHeading Goes Here\n\n--------------'),
    ('# Heading Goes Here', None, 'Heading Goes Here\n================='),

    ('test123', 'commonmark', 'test123'),
    ('******************\nHeading Goes Here\n******************', 'commonmark', '--------------\n\nHeading Goes Here\n\n--------------'),
    ('# Heading Goes Here', 'commonmark', 'Heading Goes Here\n================='),

    ('test123', 'rst', 'test123'),
    ('******************\nHeading Goes Here\n******************', 'rst', '******************\nHeading Goes Here\n******************'),
    ('# Heading Goes Here', 'rst', '# Heading Goes Here'),

    ('test123', 'gfm', 'test123'),
    ('# Heading Goes Here', 'gfm', 'Heading Goes Here\n================='),

    # pylint: enable=line-too-long
])
def test_Markup_to_rst(value, initial_format, expected):
    """Test that the ``Markup.to_markdown()`` method works correctly."""
    obj = Markup(value, markup_format = initial_format)
    rst = obj.to_rst()

    print('markdown: {}'.format(rst))
    print('expected: {}'.format(expected))

    assert rst == expected

    assert rst.markup_format == 'rst'

    target = initial_format or 'commonmark'

    result = obj._to_format(target = target, trim = True)                                 # pylint: disable=W0212

    assert result == obj
