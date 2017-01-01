# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

import concurrent.futures
import imp
import importlib
import logging
import os
import threading
from datetime import datetime

from fval.external.six import iteritems, text_type
from fval.utils import get_relative_path


class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired lock')
            self.value += 1
        finally:
            self.lock.release()


class OutputWriter(object):
    def __init__(self, output=None, output_path=None):
        self.lock = threading.Lock()
        self.output = output
        self.output_path = output_path

    def write(self):
        self.lock.acquire()
        try:
            if self.output:
                with open(self.output_path, mode='a') as output_file:
                    output_file.writelines(text_type(self.output) + os.linesep)
        finally:
            self.lock.release()


def _check_worker(config=None, unit_path=None, check_name=None,
                  check_args=None, unit_content=None, error_counter=None,
                  output_writer=None):
    logger = config['logger']
    logger.debug('Checking Unit: {0}, Name: {1}, Args: {2}'.format(unit_path, check_name, check_args))
    check_module = None
    # Try loading check module from cwd/library/<check_name> first
    try:
        check_module = imp.load_source(check_name,
                                       '{0}{1}library{2}{3}.py'.format(os.getcwd(), os.sep, os.sep, check_name))
    except ImportError:
        logger.debug('Could not import user supplied module.')
    except IOError:
        logger.debug('Could not load: {0}{1}library{2}{3}.py'.format(os.getcwd(), os.sep, os.sep, check_name))
    # If check module not found locally, then try and load a built-in
    if not check_module:
        try:
            check_module = importlib.import_module(
                'fval.checks.{0}'.format(check_name), 'fval.checks')
        except ImportError:
            logger.error('{0}: {1}'.format(get_relative_path(unit_path),
                                           'CHECK MODULE: \'{0}\' NOT FOUND'.format(check_name)))

    output_written = False
    if check_module:
        execution_args = dict(unit_path=unit_path,
                              unit_content=unit_content,
                              check_args=check_args,
                              config=config)
        try:
            result = check_module.run(**execution_args)
            if result['level'] != 'INFO':
                error_counter.increment()
            execute_output = result.get('output')
            if execute_output and output_writer:
                # Replace returned \n with actual line separators
                execute_output = text_type(
                    execute_output).replace('\\n', os.linesep)
                if os.linesep not in text_type(execute_output):
                    output_writer.output = execute_output
                else:
                    output_writer.output = text_type(execute_output)
                output_writer.write()
                output_written = True

            if not config.get('silent'):  # pragma: no cover
                if result['level'] == 'DEBUG':
                    logger.debug(
                        '{0}: {1}'.format(get_relative_path(unit_path), result['message']))
                if result['level'] == 'INFO':
                    logger.info(
                        '{0}: {1}'.format(get_relative_path(unit_path), result['message']))
                elif result['level'] == 'WARN':
                    logger.warn(
                        '{0}: {1}'.format(get_relative_path(unit_path), result['message']))
                elif result['level'] == 'ERROR':
                    logger.error(
                        '{0}: {1}'.format(get_relative_path(unit_path), result['message']))
        except AttributeError:
            logger.error('{0}: {1}'.format(
                get_relative_path(unit_path),
                'CHECK MODULE: \'{0}\' HAS FAILED - RUN WITH --debug FOR DETAILS'.format(check_name)))
            # TODO: Output trace with debug loglevel
    return dict(output_written=output_written)


def execute_plan(plan=None, config=None):
    """ Execute the plan of checks

    Args:
        plan: The list of checks to perform

        config: The configuration that applies to the checks being run

    Returns:
        int: The number of unsuccessful executions

    """
    logger = config['logger']
    error_counter = Counter()

    output_writer = None
    output_path = None
    if config.get('output'):
        output_filename = 'fval_{0}'.format(
            datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
        output_path = config.get('output') + os.sep + output_filename
        output_writer = OutputWriter(output_path=output_path)
    # If mime_type and windows then strip them out and provide not currently supported message
    if config['platform'].startswith('win'):
        logger.info('mime_type checks currently disabled due to Windows compatibility')
    # Loop through each step of the plan
    output_written = False
    for item in plan:
        unit_path, unit_checks = item.get('unit_path'), item.get('unit_checks')
        with open(unit_path, mode='rb') as unit_file:
            unit_content = unit_file.read()

        # TODO: Determine optimum max_worker count
        # Add check to thread pool for execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor_list = list()
            try:
                for check_name, check_args in iteritems(unit_checks):
                    thread_args = dict(config=config,
                                       unit_path=unit_path,
                                       unit_content=unit_content,
                                       check_name=check_name,
                                       check_args=check_args,
                                       output_writer=output_writer,
                                       error_counter=error_counter)
                    if not (config['platform'].startswith('win') and check_name == 'mime_type'):
                        executor_list.append(executor.submit(_check_worker,
                                                             **thread_args))

                for future in executor_list:
                    result = future.result()
                    if result['output_written']:
                        output_written = True
            except:
                raise
    if output_written:
        logger.info('Output written to: {0}'.format(output_path))
    return error_counter.value
