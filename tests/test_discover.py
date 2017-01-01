# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

import argparse
from functools import wraps
import os
from fval import load_config
from fval.discover import (walk_path, discover)


def test_walk_path_one_level():
    results = list()
    for current_path, dirs, file_list in walk_path('test_discover', depth=1):
        results.append((current_path, dirs, file_list))
    # Current, plus next folder down = 2 levels returned
    assert len(results) == 2


def test_walk_path_two_levels():
    results = list()
    for current_path, dirs, file_list in walk_path('test_discover', depth=2):
        results.append((current_path, dirs, file_list))
    # Current, plus next folder down, plus next folder down = 3 levels returned
    assert len(results) == 3


def test_walk_path_all_levels():
    results = list()
    for current_path, dirs, file_list in walk_path('test_discover'):
        results.append((current_path, dirs, file_list))
    # Current, plus next folder down, plus next folder down, plus next folder down = 4 levels returned
    assert len(results) == 4


def minimal_cmdline_args(func):
    @wraps(func)
    def with_args(*args, **kwargs):
        return func(*args, **kwargs)

    return with_args


@minimal_cmdline_args
def test_skipping_excluded_dirs():
    fake_args = argparse.Namespace
    fake_args.config = 'example_configs/config_excluded_dirs.yml'
    fake_args.path = 'test_discover/'
    fake_args.quiet = None
    fake_args.loglevel = None
    fake_args.debug = None
    fake_args.warn = None
    fake_args.error = None
    fake_args.all = None
    fake_args.output = None
    fake_args.depth = None
    fake_args.theme = None
    fake_args.multiline = None
    config = load_config(cmdline_args=fake_args)
    discovery_result, orphans = discover(config)
    assert len(discovery_result[0]) == 2
    assert orphans[0] == 'test_discover/depth_test_level_1/depth_test_level_2/orphan.fval'.replace('/', os.sep)


def test_using_all_to_bring_in_un_fvaled_file():
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
    discovery_result, orphans = discover(config)
    found_unfvaled = False
    for res in discovery_result:
        if 'unfvaled.yml' in res.get('unit_path'):
            found_unfvaled = True
            break
    assert found_unfvaled
    assert len(discovery_result[0]) == 2
    assert orphans[0] == 'test_discover/depth_test_level_1/depth_test_level_2/orphan.fval'.replace('/', os.sep)
