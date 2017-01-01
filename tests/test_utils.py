# -*- coding: utf-8 -*-

from __future__ import (absolute_import, unicode_literals)

import logging
import os
import tempfile

from fval.utils import get_logger, get_relative_path

test_folder_path = os.path.join(os.getcwd(), 'test_folder')
test_config_path = os.path.join(os.getcwd(), 'test_folder', 'fval.cfg')

DEBUG_ARG = '--debug'
ALL_ARG = '--all'
PATH_ARG = '--path'
CONFIG_ARG = '--config'


def test_get_logger():
    assert isinstance(get_logger(), logging.Logger)
    assert get_logger(log_level=logging.DEBUG).getEffectiveLevel() == 10
    assert get_logger(log_level=logging.INFO).getEffectiveLevel() == 20
    assert get_logger(log_level=logging.WARNING).getEffectiveLevel() == 30
    assert get_logger(log_level=logging.ERROR).getEffectiveLevel() == 40


def test_get_relative_path(tmpdir):
    level1 = tmpdir.mkdir("level1").strpath
    level2 = tmpdir.mkdir("level1/level2").strpath
    get_relative_path(level2)
    os.chdir(level1)
    get_relative_path(level2)

    # print(os.getcwd())
    # print(type(os.getcwd()))
    # print(get_relative_path(os.getcwd()))
    # print(get_relative_path('/var'))
    # temp_dir = tempfile.mkdtemp()
    # print('a')
    # temp_dir_path = os.path.abspath(temp_dir)
    # print(type(temp_dir_path))
    # print('b')
    # print(get_relative_path(temp_dir_path))
    # tmpdir.mkdir("level1")
    # test_file = tmpdir.mkdir("level1/level2").join("test_file")
    # test_file.write("hello world")
    # print(type(os.getcwd()))
    # print(get_relative_path(os.getcwd()))
    # print(get_relative_path(test_file.strpath))

    # print(get_relative_path(temp_dir_structure))
    # def test_real_main_empty_dir(tmpdir):
    #     empty_dir = tmpdir.mkdir("empty").strpath
    # if getcwd() in path.abspath(file_path):
    #     return file_path.replace(getcwd(), '.')
    # else:
    #     return file_path.relpath(path=file_path)
