# -*- coding: utf-8 -*-
"""
This package contains all of the modules utilised by the fval library.
"""
from __future__ import (absolute_import, unicode_literals, print_function)

import argparse
import os
import sys

from fval.utils import get_logger, get_relative_path

try:
    import yaml
    from yaml.parser import (ParserError, ScannerError)
except ImportError:
    print('The PyYAML library is missing.' +
          os.linesep +
          'Install using pip install PyYAML.')
    exit(1)

from fval.discover import discover
from fval.execute import execute_plan
from fval.plan import build_plan
import logging

__title__ = 'fval'
__version__ = '0.0.1'
__author__ = 'Jon Hadfield'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Jon Hadfield'

# CONSTANTS
CONFIG_FILENAME = 'fval.cfg'


def _config_file_loader(path):
    result = dict()
    if os.path.isfile(path):
        try:
            with open(path) as fval_cfg_file:
                result['config'] = yaml.load(fval_cfg_file.read())
        except IOError as ie:
            if ie.strerror == 'Permission denied':
                result['failure_message'] = 'Permission denied when loading file: {0}'.format(path)
            else:
                result['failure_message'] = 'Unhandled exception when loading file: {0}'.format(path)
        except (ParserError, ScannerError):
            result['failure_message'] = 'Unable to parse configuration: {0}'.format(path)
        except:
            result['failure_message'] = 'Unhandled exception'
    return result


# def get_config_errors(config):
    # errors = list()
    # if 'mappings' not in config:
    #     errors.append('mappings is undefined')
    # elif not config.get('mappings'):
    #     errors.append('no extension mappings are undefined')
    # return errors


def load_config(cmdline_args=None):
    config = dict()
    # TRY LOADING CONFIG FROM PATH SPECIFIED
    if cmdline_args.config:
        config_path = cmdline_args.config
        result = _config_file_loader(config_path)
        if result:
            config = result['config']
        else:
            exit('Configuration file: {0} does not exist.'.format(config_path))

    # ELSE, TRY LOADING CONFIG FROM CURRENT DIR
    if not config:
        local_config_path = '{0}{1}{2}'.format(
            os.getcwd(), os.sep, CONFIG_FILENAME)
        result = _config_file_loader(local_config_path)
        if result:
            config = result['config']

    # ELSE, TRY LOADING CONFIG FROM HOME DIR
    if not config:
        home_config_path = '{0}{1}.fval{2}{3}'.format(
            os.path.expanduser('~'), os.sep, os.sep, CONFIG_FILENAME)
        result = _config_file_loader(home_config_path)
        if result:
            config = result['config']

    # If we've got here, then configuration must be loaded and syntactically correct

    # COMBINE LOADED CONFIG WITH COMMAND LINE ARGS
    if cmdline_args.path:
        config['path'] = cmdline_args.path.replace('\\', os.sep).replace('/', os.sep)
    config['quiet'] = cmdline_args.quiet

    # Set default log level (matching argparse stated default)
    log_level = logging.INFO
    if cmdline_args.loglevel == 'debug' or cmdline_args.debug:
        log_level = logging.DEBUG
    elif cmdline_args.loglevel == 'info':
        log_level = logging.INFO
    elif cmdline_args.loglevel == 'warn' or cmdline_args.warn:
        log_level = logging.WARNING
    elif cmdline_args.loglevel == 'error' or cmdline_args.error:
        log_level = logging.ERROR
    config['all'] = cmdline_args.all
    config['output'] = cmdline_args.output
    config['depth'] = cmdline_args.depth
    config['theme'] = cmdline_args.theme
    config['logger'] = get_logger(log_level=log_level)
    config['platform'] = sys.platform
    config['multiline'] = cmdline_args.multiline

    return config


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--path",
                        help="directory to scan", default=os.getcwd())
    parser.add_argument("--config",
                        help="path to configuration")
    parser.add_argument("--loglevel", help="log level",
                        choices=['debug', 'info', 'warn', 'error'])
    parser.add_argument("--debug",
                        help="shortcut for --loglevel=debug", action="store_true")
    parser.add_argument("--warn",
                        help="shortcut for --loglevel=warn", action="store_true")
    parser.add_argument("--error",
                        help="shortcut for --loglevel=error", action="store_true")
    parser.add_argument("--quiet",
                        help="output errors only", action="store_true")
    parser.add_argument("--all",
                        help="recursively analyse all files in path",
                        action="store_true")
    parser.add_argument("--output",
                        help="where to output check feedback")
    parser.add_argument("--depth",
                        help="how many directories deep to recurse",
                        type=int, default=-1)
    parser.add_argument("--theme", help="colour theme")
    parser.add_argument("--multiline",
                        help="output warnings and errors over multiple lines", action="store_true")
    return parser.parse_args(args)


def _real_main(sys_args):
    cmdline_args = parse_args(sys_args)
    config = load_config(cmdline_args=cmdline_args)
    logger = config['logger']
    if not os.path.isdir(config.get('path')):
        sys.exit('{0}ERROR: Path: \'{1}\' does not exist.'.format(
            os.linesep, config.get('path')))

    # DISCOVER
    result, orphans = discover(config=config)
    if orphans:
        parsed_orphans = [get_relative_path(orphan_path) for orphan_path in orphans]
        logger.info('Discovered orphans: {0}'.format(','.join(parsed_orphans))),
    # BUILD PLAN
    test_plan = build_plan(result, config=config)

    # EXECUTE PLAN
    execution_result = execute_plan(test_plan, config=config)
    logger.debug('Total Errors: {0}'.format(execution_result))
    if execution_result:
        exit(1)
    else:
        exit(0)


def main():
    try:
        _real_main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(os.linesep + 'ERROR: Interrupted by user')
