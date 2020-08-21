# -*- coding: utf-8 -*-

"""
***********************************
tests.test_utility_functions.py
***********************************

Tests for the functions contained in :module:`utility_functions.py <utility_functions>`.

"""
import pytest

from validator_collection._compat import basestring
from validator_collection import checkers

from open_api.utility_functions import validate_url, traverse_dict, validate_runtime_expression, validate_component_map_key


@pytest.mark.parametrize('value, fails, allow_empty, allow_special_ips', [
    (u"http://foo.com/blah_blah", False, False, False),
    (u"http://foo.com/blah_blah/", False, False, False),
    (u"http://foo.com/blah_blah_(wikipedia)", False, False, False),
    (u"http://foo.com/blah_blah_(wikipedia)_(again)", False, False, False),
    (u"http://www.example.com/wpstyle/?p=364", False, False, False),
    (u"https://www.example.com/foo/?bar=baz&inga=42&quux", False, False, False),
    (u"http://✪df.ws/123", False, False, False),
    (u"http://userid:password@example.com:8080", False, False, False),
    (u"http://userid:password@example.com:8080/", False, False, False),
    (u"http://userid@example.com", False, False, False),
    (u"http://userid@example.com/", False, False, False),
    (u"http://userid@example.com:8080", False, False, False),
    (u"http://userid@example.com:8080/", False, False, False),
    (u"http://userid:password@example.com", False, False, False),
    (u"http://userid:password@example.com/", False, False, False),
    (u"http://142.42.1.1/", False, False, False),
    (u"http://142.42.1.1:8080/", False, False, False),
    (u"http://➡.ws/䨹", False, False, False),
    (u"http://⌘.ws", False, False, False),
    (u"http://⌘.ws/", False, False, False),
    (u"http://foo.com/blah_(wikipedia)#cite-1", False, False, False),
    (u"http://foo.com/blah_(wikipedia)_blah#cite-1", False, False, False),
    (u"http://foo.com/unicode_(✪)_in_parens", False, False, False),
    (u"http://foo.com/(something)?after=parens", False, False, False),
    (u"http://☺.damowmow.com/", False, False, False),
    (u"http://jurnalsda_pusair.pu.go.id", False, False, False),
    (u"http://code.google.com/events/#&product=browser", False, False, False),
    (u"http://j.mp", False, False, False),
    (u"ftp://foo.bar/baz", False, False, False),
    (u"http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False, False),
    (u"http://مثال.إختبار", False, False, False),
    (u"http://例子.测试", False, False, False),
    (u"http://उदाहरण.परीक्षा", False, False, False),
    (u"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False, False),
    (u"http://1337.net", False, False, False),
    (u"http://a.b-c.de", False, False, False),
    (u"http://a.b--c.de/", False, False, False),
    (u"http://223.255.255.254", False, False, False),
    (u"", True, False, False),
    (None, True, False, False),
    (u"http://", True, False, False),
    (u"http://.", True, False, False),
    (u"http://..", True, False, False),
    (u"http://../", True, False, False),
    (u"http://?", True, False, False),
    (u"http://??", True, False, False),
    (u"http://??/", True, False, False),
    (u"http://#", True, False, False),
    (u"http://##", True, False, False),
    (u"http://##/", True, False, False),
    (u"http://foo.bar?q=Spaces should be encoded", True, False, False),
    (u"//", False, False, False),
    (u"//a", False, False, False),
    (u"///a", False, False, False),
    (u"///", False, False, False),
    (u"http:///a", True, False, False),
    (u"foo.com", False, False, False),
    (u"rdar://1234", True, False, False),
    (u"h://test", True, False, False),
    (u"http:// shouldfail.com", True, False, False),
    (u":// should fail", True, False, False),
    (u"http://foo.bar/foo(bar)baz quux", True, False, False),
    (u"ftps://foo.bar/", True, False, False),
    (u"http://-error-.invalid/", True, False, False),
    (u"http://-a.b.co", True, False, False),
    (u"http://a.b-.co", True, False, False),
    (u"http://0.0.0.0", True, False, False),
    (u"http://10.1.1.0", True, False, False),
    (u"http://10.1.1.255", True, False, False),
    (u"http://224.1.1.1", True, False, False),
    (u"http://1.1.1.1.1", True, False, False),
    (u"http://123.123.123", True, False, False),
    (u"http://3628126748", True, False, False),
    (u"http://.www.foo.bar/", True, False, False),
    (u"http://www.foo.bar./", True, False, False),
    (u"http://.www.foo.bar./", True, False, False),
    (u"http://10.1.1.1", True, False, False),
    (u"", False, True, False),
    (None, False, True, False),

    (u"localhost", False, False, False),
    (u"abc.localhost.com", False, False, False),
    (u"invalid", False, False, False),
    (u"abc.invalid.com", False, False, False),

    (u"http://localhost", False, False, False),
    (u"http://abc.localhost.com", False, False, False),
    (u"http://invalid", False, False, False),
    (u"http://abc.invalid.com", False, False, False),

    (u"http://foo.com/blah_blah", False, False, True),
    (u"http://foo.com/blah_blah/", False, False, True),
    (u"http://foo.com/blah_blah_(wikipedia)", False, False, True),
    (u"http://foo.com/blah_blah_(wikipedia)_(again)", False, False, True),
    (u"http://www.example.com/wpstyle/?p=364", False, False, True),
    (u"https://www.example.com/foo/?bar=baz&inga=42&quux", False, False, True),
    (u"http://✪df.ws/123", False, False, True),
    (u"http://userid:password@example.com:8080", False, False, True),
    (u"http://userid:password@example.com:8080/", False, False, True),
    (u"http://userid@example.com", False, False, True),
    (u"http://userid@example.com/", False, False, True),
    (u"http://userid@example.com:8080", False, False, True),
    (u"http://userid@example.com:8080/", False, False, True),
    (u"http://userid:password@example.com", False, False, True),
    (u"http://userid:password@example.com/", False, False, True),
    (u"http://142.42.1.1/", False, False, True),
    (u"http://142.42.1.1:8080/", False, False, True),
    (u"http://➡.ws/䨹", False, False, True),
    (u"http://⌘.ws", False, False, True),
    (u"http://⌘.ws/", False, False, True),
    (u"http://foo.com/blah_(wikipedia)#cite-1", False, False, True),
    (u"http://foo.com/blah_(wikipedia)_blah#cite-1", False, False, True),
    (u"http://foo.com/unicode_(✪)_in_parens", False, False, True),
    (u"http://foo.com/(something)?after=parens", False, False, True),
    (u"http://☺.damowmow.com/", False, False, True),
    (u"http://jurnalsda_pusair.pu.go.id", False, False, True),
    (u"http://code.google.com/events/#&product=browser", False, False, True),
    (u"http://j.mp", False, False, True),
    (u"ftp://foo.bar/baz", False, False, True),
    (u"http://foo.bar/?q=Test%20URL-encoded%20stuff", False, False, True),
    (u"http://مثال.إختبار", False, False, True),
    (u"http://例子.测试", False, False, True),
    (u"http://उदाहरण.परीक्षा", False, False, True),
    (u"http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com", False, False, True),
    (u"http://1337.net", False, False, True),
    (u"http://a.b-c.de", False, False, True),
    (u"http://a.b--c.de/", False, False, True),
    (u"http://223.255.255.254", False, False, True),
    (u"", True, False, True),
    (None, True, False, True),
    (u"http://", True, False, True),
    (u"http://.", True, False, True),
    (u"http://..", True, False, True),
    (u"http://../", True, False, True),
    (u"http://?", True, False, True),
    (u"http://??", True, False, True),
    (u"http://??/", True, False, True),
    (u"http://#", True, False, True),
    (u"http://##", True, False, True),
    (u"http://##/", True, False, True),
    (u"http://foo.bar?q=Spaces should be encoded", True, False, True),
    (u"//", False, False, True),
    (u"//a", False, False, True),
    (u"///a", False, False, True),
    (u"///", False, False, True),
    (u"http:///a", True, False, True),
    (u"foo.com", False, False, True),
    (u"rdar://1234", True, False, True),
    (u"h://test", True, False, True),
    (u"http:// shouldfail.com", True, False, True),
    (u":// should fail", True, False, True),
    (u"http://foo.bar/foo(bar)baz quux", True, False, True),
    (u"ftps://foo.bar/", True, False, True),
    (u"http://-error-.invalid/", True, False, True),
    (u"http://-a.b.co", True, False, True),
    (u"http://a.b-.co", True, False, True),
    (u"http://0.0.0.0", False, False, True),
    (u"http://10.1.1.0", False, False, True),
    (u"http://10.1.1.255", False, False, True),
    (u"http://224.1.1.1", False, False, True),
    (u"http://1.1.1.1.1", True, False, True),
    (u"http://123.123.123", True, False, True),
    (u"http://3628126748", True, False, True),
    (u"http://.www.foo.bar/", True, False, True),
    (u"http://www.foo.bar./", True, False, True),
    (u"http://.www.foo.bar./", True, False, True),
    (u"http://10.1.1.1", False, False, True),
    (u"", False, True, True),
    (None, False, True, True),

    (u"localhost", False, False, True),
    (u"abc.localhost.com", False, False, True),
    (u"invalid", False, False, True),
    (u"abc.invalid.com", False, False, True),

    (u"http://localhost", False, False, True),
    (u"http://abc.localhost.com", False, False, True),
    (u"http://invalid", False, False, True),
    (u"http://abc.invalid.com", False, False, True),


    (u"https://{somevariable}.testurl.com/api", False, False, True),
    (u"/{someVariable}testpath.com/{other_Variable}/{other}", False, False, True),
    (u"https://{username}.gigantic-server.com:{port}/{basePath}", False, False, True),
])
def test_validate_url(value, fails, allow_empty, allow_special_ips):
    """Test the URL validator."""
    if not fails:
        validated = validate_url(value,
                                 allow_empty = allow_empty,
                                 allow_special_ips = allow_special_ips)
        if value:
            assert isinstance(validated, basestring)
        else:
            assert validated is None
    else:
        with pytest.raises((ValueError, TypeError)):
            value = validate_url(value, allow_empty = allow_empty)


@pytest.mark.parametrize('content, target, expects, error', [
    ({'test': 'value', 'test2': {'something': 'value', 'something2': {'level3': 123}}}, 'test', ['test'], None),
    ({'test': 'value', 'test2': {'something': 'value', 'something2': {'level3': 123}}}, 'test2', ['test2'], None),
    ({'test': 'value', 'test2': {'something': 'value', 'something2': {'level3': 123}}}, 'something', ['test2', 'something'], None),
    ({'test': 'value', 'test2': {'something': 'value', 'something2': {'level3': 123}}}, 'level3', ['test2', 'something2', 'level3'], None),

    ({'test': 'value', 'test2': {'something': 'value', 'something2': {'level3': 123}}}, 'missing-value', [], None),
])
def test_traverse_dict(content, target, expects, error):
    if not error:
        result = traverse_dict(content, target)
        assert len(result) == len(expects)
        assert checkers.are_equivalent(expects, result)
    else:
        with pytest.raises(error):
            result = traverse_dict(content, target)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('$method', False, False),
    ('$request.header.accept', False, False),
    ('$request.path.id', False, False),
    ('$request.body#/user/uuid', False, False),
    ('$url', False, False),
    ('$response.body#/status', False, False),
    ('$response.header.Server', False, False),

    ('invalid expression', True, False),
])
def test_validate_runtime_expression(value, fails, allow_empty):
    if not fails:
        validated = validate_runtime_expression(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validate_runtime_expression(value, allow_empty = allow_empty)


@pytest.mark.parametrize('value, fails, allow_empty', [
    ('User', False, False),
    ('User_1', False, False),
    ('User_Name', False, False),
    ('user-name', False, False),
    ('my.org.User', False, False),

    ('invalid expression', True, False),
])
def test_validate_component_map_key(value, fails, allow_empty):
    if not fails:
        validated = validate_component_map_key(value, allow_empty = allow_empty)
        if value:
            assert validated is not None
        else:
            assert validated is None
    else:
        with pytest.raises(ValueError):
            value = validate_component_map_key(value, allow_empty = allow_empty)
