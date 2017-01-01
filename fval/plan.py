# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import splitext

import yaml


def build_plan(discovery_result, config=None):
    """ Extract content and determine which checks need to be run

    Checks are assigned in the following order:
    1. <filename>.fval
    2. <dir>.fval
    3. default config

    Note: As soon as a matching set of tests is found, the build is complete.
          Merging/inheritance is not currently supported.

    Args:
        discovery_result: The paths discovered
        config: Options provided in configuration file and
                through command line options

    Returns:
        list: The checks to perform against the discovered paths
    """

    logger = config['logger']
    plan = list()
    for item in discovery_result:
        fval_path = item.get('fval_path')
        dir_fval_path = item.get('dir_fval_path')
        unit_path = item.get('unit_path')
        fval_dir_config = None
        unit_ext = splitext(unit_path)[1]
        unit_tests = list()

        # If a 'unit specific' fval file was found, then loads its checks
        if fval_path:
            try:
                with open(fval_path.encode('utf-8')) as fval_file:
                    cf_yaml_content = yaml.load(fval_file.read())
                    unit_tests = cf_yaml_content
            except IOError:
                logger.debug('No unit specific file found for: {0}'.format(fval_path))
        # If a fval file was found in the directory, then load its checks
        elif dir_fval_path:
            try:
                with open(
                        dir_fval_path.encode(
                            'utf-8'), 'r') as dir_fval_file:
                    fval_dir_config = yaml.load(dir_fval_file.read())
            except IOError:
                logger.debug('No dir specific file found for: {0}'.format(fval_path))
            except:
                raise
        # If no tests (specific to the unit or the directory) are found,
        # then fall back to master config
        if not unit_tests and fval_dir_config and fval_dir_config.get('mappings'):
            # CHECK IF UNIT FILE HAS RECOGNISED EXTENSION IN MAPPINGS
            matching_templates = list()
            for mapping in fval_dir_config.get('mappings'):
                if mapping.get('extension') == unit_ext[1:]:
                    matching_templates = mapping.get('templates')
            # IF MATCHING TEMPLATES WERE FOUND, THEN EXTRACT THE CHECKS
            if matching_templates:
                extracted_checks = dict()
                for matching_template in matching_templates:
                    if matching_template in fval_dir_config.get('templates'):
                        matched_template = fval_dir_config.get('templates').get(matching_template)
                        extracted_checks.update(matched_template)
                unit_tests = extracted_checks
        elif not unit_tests and (config.get('all') or dir_fval_path) and config.get('mappings'):
            # CHECK IF UNIT FILE HAS RECOGNISED EXTENSION IN MAPPINGS
            matching_templates = list()
            for mapping in config.get('mappings'):
                if mapping.get('extension') == unit_ext[1:]:
                    matching_templates = mapping.get('templates')
            # IF MATCHING TEMPLATES WERE FOUND, THEN EXTRACT THE CHECKS
            if matching_templates:
                extracted_checks = dict()
                for matching_template in matching_templates:
                    if config.get('templates') and matching_template in config.get('templates'):
                        matched_template = config.get('templates').get(matching_template)
                        extracted_checks.update(matched_template)
                unit_tests = extracted_checks
        if unit_tests:
            plan.append(dict(unit_path=unit_path, unit_checks=unit_tests))
    return plan
