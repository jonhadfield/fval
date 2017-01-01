# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

import os

from fval.checks import syntax

CHECK_NAME = 'SYNTAX'


def test_valid_yaml_check():
    yaml_content = """---
    item1: a
    item2: 1
    item3:
      - first: f
      - second: s
    """
    test_1 = {"item1": "a"}
    test_2 = {"item2": "1"}
    test_3 = {"item3.1.second": "s"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2, test_3]
    check_args['markup'] = 'yaml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'INFO'


def test_valid_yaml_check_with_failed_match():
    yaml_content = """---
    item1: a
    item2: 1
    item3:
      - first: f
      - second: t
    """
    test_1 = {"item1": "a"}
    test_2 = {"item2": "1"}
    test_3 = {"item3.1.second": "s"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2, test_3]
    check_args['markup'] = 'yaml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_yaml_check_with_missing_param():
    yaml_content = """---
    item1: a
    item2: 1
    item3:
      - first: f
      - second: t
    """
    test_1 = {"item1": "a"}
    test_2 = {"item2": "1"}
    test_3 = {"item4.1.second": "s"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2, test_3]
    check_args['markup'] = 'yaml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'

def test_invalid_yaml_check():
    yaml_content = """*a
    """
    test_1 = {"item1": "b"}
    test_2 = {"item2": "b"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'yaml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_invalid_json_check():
    json_content = """---
    item1: a
    item2: b
    """
    test_1 = {"item1": "b"}
    test_2 = {"item2": "b"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'json'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_json_check():
    json_content = """
    {"employees":[
        {"firstName":"John", "lastName":"Doe"},
            {"firstName":"Anna", "lastName":"Smith"},
                {"firstName":"Peter", "lastName":"Jones"}
]}
    """
    test_1 = {"employees.0.firstName": "John"}
    check_args = dict()
    check_args['regexes'] = [test_1]
    check_args['markup'] = 'json'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'INFO'


def test_invalid_ini_check():
    ini_content = """*"""
    check_args = dict()
    check_args['regexes'] = list()
    check_args['markup'] = 'ini'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=ini_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_invalid_xml_check():
    xml_content = """---
    item1: a
    item2: b
    """
    test_1 = {"item1": "b"}
    test_2 = {"item2": "b"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'xml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=xml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_xml_check():
    xml_content = b"""<valid>a</valid>"""
    test_1 = {"employees.0.firstName": "John"}
    check_args = dict()
    check_args['regexes'] = [test_1]
    check_args['markup'] = 'xml'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=xml_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'INFO'


def test_invalid_java_properties_check():
    java_properties_content = b"""invalid"""
    test_1 = {"employees.0.firstName": "John"}
    check_args = dict()
    check_args['regexes'] = [test_1]
    check_args['markup'] = 'java_properties'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=java_properties_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_java_properties_check():
    java_properties_content = 'hello=world' + os.linesep + 'job:goodun'
    test_1 = {"hello": "world"}
    test_2 = {"job": "goodun"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'java_properties'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=java_properties_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'INFO'


def test_valid_java_properties_check_with_non_matching_regex():
    java_properties_content = 'hello=world' + os.linesep + 'job:goodun'
    test_1 = {"hello": "world"}
    test_2 = {"job": "baddun"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'java_properties'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=java_properties_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_java_properties_check_with_missing_param():
    java_properties_content = 'hello=world'
    test_1 = {"hello": "world"}
    test_2 = {"job": "goodun"}
    check_args = dict()
    check_args['regexes'] = [test_1, test_2]
    check_args['markup'] = 'java_properties'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=java_properties_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'WARN'


def test_invalid_check():
    java_properties_content = 'hello=world'
    test_1 = {"hello": "world"}
    check_args = dict()
    check_args['regexes'] = [test_1]
    check_args['markup'] = 'dodgy_markup'
    check_args['config'] = 'test'
    execution_args = dict(unit_path='fake_path',
                          unit_content=java_properties_content,
                          check_args=check_args,
                          config=None)
    result = syntax.run(**execution_args)
    assert result['level'] == 'ERROR'
