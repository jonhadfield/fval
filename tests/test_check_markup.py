# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

from fval.checks import markup


def test_valid_ini_check():
    ini_content = b"""[SectionOne]
Name: Derek"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=ini_content,
                          check_args='ini',
                          config=None)
    result = markup.run(**execution_args)
    # assert result == 'a'
    assert result['level'] == 'INFO'


def test_invalid_ini_check():
    ini_content = b"""---"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=ini_content,
                          check_args='ini',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_yaml_check():
    yaml_content = b"""---
    - item1
    - item2
    """
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args='yaml',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'INFO'


def test_invalid_yaml_check():
    yaml_content = b"""
    *< a: 2
    """
    execution_args = dict(unit_path='fake_path',
                          unit_content=yaml_content,
                          check_args='yaml',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_json_check():
    json_content = b"""{"a":1}"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args='json',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'INFO'


def test_invalid_json_check():
    json_content = b"""invalid"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args='json',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'WARN'


def test_valid_xml_check():
    json_content = b"""<valid>a</valid>"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args='xml',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'INFO'


def test_invalid_xml_check():
    json_content = b"""invalid"""
    execution_args = dict(unit_path='fake_path',
                          unit_content=json_content,
                          check_args='xml',
                          config=None)
    result = markup.run(**execution_args)
    assert result['level'] == 'WARN'
