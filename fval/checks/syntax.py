# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

import io
import json
import os
import re
from xml.etree import ElementTree

import yaml

import fval.external.six as six

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

CHECK_NAME = 'SYNTAX'


def get_parsed_config(markup=None, unit_content=None):
    parsed_config = None
    level = None
    message = None
    if markup == 'yaml':
        try:
            parsed_config = yaml.load(unit_content)
        except yaml.YAMLError:
            message = 'Required: YAML'
            level = 'WARN'
    elif markup == 'json':
        try:
            parsed_config = json.loads(unit_content)
        except ValueError:
            message = 'Required: JSON'
            level = 'WARN'
    elif markup == 'xml':
        try:
            ElementTree.fromstring(unit_content)
        except ElementTree.ParseError:
            level = 'WARN'
            message = 'Required: XML'
    elif markup == 'ini':
        try:
            config = ConfigParser(allow_no_value=True)
            config.readfp(io.StringIO(unit_content.decode("utf-8")))
        # TODO: Be specific
        except:
            level = 'WARN'
            message = 'Required: INI'
    elif markup == 'java_properties':
        try:
            unit_content = '[dummy]' + os.linesep + unit_content
            buf = six.StringIO(unit_content)
            config = six.moves.configparser.ConfigParser()
            config.readfp(buf)
            parsed_config = dict(config.items('dummy'))
        # TODO: Make specific
        except:
            level = 'WARN'
            message = 'Required: JAVA_PROPERTIES'
    else:
        message = 'Check failed to run. Unrecognised markup type specified.'
        level = 'ERROR'
    return dict(message=message, level=level, parsed_config=parsed_config)


def process_regexes(regexes=None, parsed_config=None, markup=None):
    result_list = list()
    if markup == 'java_properties':
        for regex in regexes:
            regex_key = next(six.iterkeys(regex))
            if parsed_config and regex_key in parsed_config:
                if not re.match(regex[regex_key], parsed_config[regex_key]):
                    result_list.append(
                        '{0}:{1} != {2}:{3}'.format(
                            regex_key, regex[regex_key], regex_key,
                            parsed_config[regex_key]))
            if parsed_config and regex_key not in parsed_config:
                result_list.append('{0} MISSING'.format(regex_key))
    if markup == 'yaml':
        for regex in regexes:
            selector = next(six.iterkeys(regex))
            selector_components = selector.split('.')
            processed_selector = ''
            for component in selector_components:
                if component.isdigit():
                    processed_selector = '{0}[{1}]'.format(
                        processed_selector, component)
                elif isinstance(component, six.string_types):
                    processed_selector = '{0}[\'{1}\']'.format(
                        processed_selector, component)
            regex_key = next(six.iterkeys(regex))
            try:
                selected_value = eval('parsed_config{0}'.format(
                    processed_selector))
                regex_value = regex[regex_key]
                if not re.match(regex_value, six.text_type(selected_value)):
                    result_list.append(
                        '{0}:{1} != {2}:{3}'.format(
                            regex_key, regex_value, regex_key,
                            selected_value))
            except (KeyError, IndexError):
                result_list.append('{0} MISSING'.format(regex_key))
    return result_list


def run(**kwargs):
    regexes = kwargs['check_args']['regexes']
    result = get_parsed_config(
        markup=kwargs['check_args']['markup'],
        unit_content=kwargs['unit_content'])
    if result.get('level'):
        return dict(message=result.get('message'), level=result.get('level'))
    parsed_config = result.get('parsed_config')

    failure_list_output = None
    if regexes:
        failure_list = process_regexes(regexes=regexes,
                                       parsed_config=parsed_config,
                                       markup=kwargs['check_args']['markup'])
        # failure_list_output = ''.join(failure_list)[:-2]
        if kwargs['config'] and kwargs['config'].get('multiline'):
            failure_list = ['\t{0}'.format(item) for item in failure_list]
            failure_list_output = os.linesep + os.linesep.join(failure_list)
        else:
            failure_list_output = ' | '.join(failure_list)
    if not failure_list_output:
        level = 'INFO'
        message = 'OK'
    else:
        level = 'WARN'
        # failure_list_output = os.linesep.join(failure_list_output.split('|'))
        message = failure_list_output
    message = '{0}: {1}'.format(CHECK_NAME, message)
    output = kwargs['unit_path'] + os.linesep + message + os.linesep
    return dict(message=message, level=level, output=output)
