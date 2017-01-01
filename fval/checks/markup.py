# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

import json
import os
from xml.etree import ElementTree

import yaml
import io

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


CHECK_NAME = 'MARKUP'


def run(**kwargs):
    message = None
    level = 'INFO'
    if kwargs['check_args'] == 'yaml':
        try:
            yaml.load(kwargs['unit_content'])
            level = 'INFO'
            message = 'Valid YAML'
        except yaml.YAMLError:
            message = 'Invalid YAML'
            level = 'WARN'
    elif kwargs['check_args'] == 'json':
        try:
            json.loads(kwargs['unit_content'].decode("utf-8"))
            level = 'INFO'
            message = 'Valid JSON'
        except ValueError:
            message = 'Invalid JSON'
            level = 'WARN'
    elif kwargs['check_args'] == 'ini':
        try:
            config = ConfigParser(allow_no_value=True)
            config.readfp(io.StringIO(kwargs['unit_content'].decode("utf-8")))
            level = 'INFO'
            message = 'Valid INI'
        # TODO: Be specific
        except:
            message = 'Invalid INI'
            level = 'WARN'
    elif kwargs['check_args'] == 'xml':
        try:
            ElementTree.fromstring(kwargs['unit_content'])
            level = 'INFO'
            message = 'Valid XML'
        except ElementTree.ParseError:
            message = 'Invalid XML'
            level = 'WARN'
    message = '{0}: {1}'.format(CHECK_NAME, message)
    output = kwargs['unit_path'] + os.linesep + message + os.linesep
    return dict(message=message, level=level, output=output)
