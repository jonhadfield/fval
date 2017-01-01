# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

import argparse
from collections import OrderedDict

from fval import load_config
from fval.plan import build_plan


def test_build_plan():
    fake_args = argparse.Namespace
    fake_args.config = 'example_configs/config_excluded_dirs.yml'
    fake_args.path = 'test_discover/'
    fake_args.quiet = None
    fake_args.loglevel = None
    fake_args.debug = None
    fake_args.warn = None
    fake_args.error = None
    fake_args.all = True
    fake_args.output = None
    fake_args.depth = None
    fake_args.theme = None
    fake_args.multiline = None
    config = load_config(cmdline_args=fake_args)
    discovery = [
        OrderedDict([('unit_path', u'test_discover/file0.txt'), ('fval_path', u'test_discover/.file0.txt.fval')]),
        OrderedDict([('dir_fval_path', u'test_discover/depth_test_level_1/.fval'),
                     ('unit_path', u'test_discover/depth_test_level_1/file1.txt')]),
        OrderedDict([('unit_path', u'test_discover/depth_test_level_1/depth_test_level_2/file2.txt')]),
        OrderedDict([('unit_path', u'test_discover/depth_test_level_1/depth_test_level_2/unfvaled.yml')])
    ]
    plan = build_plan(discovery_result=discovery, config=config)
    # [{'unit_checks': {'mime_type': 'text/plain'}, 'unit_path': 'test_discover/file0.txt'},
    #  {'unit_checks': {'mime_type': '...it_checks': {
    #     'mime_type': 'text/plain'}, 'unit_path': 'test_discover/depth_test_level_1/depth_test_level_2/file2.txt'}] == 0
