# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

import argparse
import logging
import os

import pytest

from fval import (_config_file_loader, _real_main)
from fval import parse_args, load_config
from fval.external.six import PY2, PY3

test_folder_path = os.path.join(os.getcwd(), 'test_folder')
test_config_path = os.path.join(os.getcwd(), 'test_folder', 'fval.cfg')

DEBUG_ARG = '--debug'
ALL_ARG = '--all'
PATH_ARG = '--path'
CONFIG_ARG = '--config'


def test_args():
    parsed = parse_args(
        [PATH_ARG, '/tmp', DEBUG_ARG, ALL_ARG, CONFIG_ARG, test_config_path])
    assert parsed.path == '/tmp'
    assert parsed.all


def test_config_file_loader():
    """ Test configuration loader """
    with pytest.raises(TypeError):
        _config_file_loader()
    assert isinstance(_config_file_loader(path='example_configs/config_1.yml'), dict)
    assert 'failure_message' in _config_file_loader(path='example_configs/invalid_format.yml')


def test_load_config_bad_call():
    with pytest.raises(AttributeError):
        load_config()


def test_load_config_without_config_provided():
    fake_args = argparse.Namespace
    fake_args.config = None
    fake_args.path = None
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
    assert isinstance(load_config(cmdline_args=fake_args), dict)


def test_load_config_with_config_1_provided():
    fake_args = argparse.Namespace
    fake_args.config = 'example_configs/config_1.yml'
    fake_args.path = None
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
    loaded = load_config(cmdline_args=fake_args)
    assert isinstance(loaded, dict)
    assert not loaded.get('all')
    assert not loaded.get('depth')
    assert 'dirs' in loaded.get('exclusions')
    assert 'paths' in loaded.get('exclusions')
    assert isinstance(loaded.get('logger'), logging.Logger)


def test_real_main_empty_dir(tmpdir):
    empty_dir = tmpdir.mkdir("empty").strpath
    with pytest.raises(SystemExit) as se:
        _real_main(['--path={0}'.format(empty_dir), '--error'])

    if PY2:
        assert se.value[0] == 0
    elif PY3:
        assert se.exconly() == 'SystemExit: 0'

# # def test_internal_folder_all(capsys):
# #     parsed = parse_args(
# #         [CONFIG_ARG, test_config_path, ALL_ARG])
# #     config = load_config(args=parsed)
# #     result, orphans = discover(args=parsed, config=config)
# #     assert len(orphans) == 1
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config, args=parsed)
# #     out, err = capsys.readouterr()
# #     assert execution_result == 10
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
#
# #
# # def test_internal_folder_1(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_1'), CONFIG_ARG, test_config_path,
# #          CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 1
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 0
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_2(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_2'), CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 1
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_3(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_3'), CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 2
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_4(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_4'), CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 0
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_5(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_5'), CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 2
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_6(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_6'), CONFIG_ARG, test_config_path, DEBUG_ARG])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 2
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
# #
# #
# # def test_internal_folder_7(capsys):
# #     parsed = parse_args(
# #         [PATH_ARG, os.path.join(test_folder_path, 'internal_folder_7'), CONFIG_ARG, test_config_path])
# #     config = load_config(cmdline_args=parsed)
# #     result, orphans = discover(config=config)
# #     assert len(orphans) == 0
# #     test_plan = build_plan(result, config=config)
# #     execution_result = execute_plan(test_plan, config=config)
# #     out, err = capsys.readouterr()
# #     # assert execution_result == 0
# #     # print(execution_result)
# #     # print('\n\nxxx OUT = {0} xxx'.format(out))
# #     # print('\n\nERR = {0}'.format(err))
