# -*- coding: utf-8 -*-
"""
This module contains helper functions
"""

from __future__ import (absolute_import, unicode_literals, print_function)

import inspect
import logging
import time
from os import getcwd, path, curdir

from colorlog import ColoredFormatter


def get_logger(log_level=logging.INFO):
    """Get a logger for outputting to console. """
    root_module_name = inspect.stack()[-1][1].split('/')[-1].split('.')[0]
    logging.addLevelName(30, "WARN")
    logger = logging.getLogger(root_module_name)
    logger.setLevel(log_level)
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    formatter = ColoredFormatter(fmt="%(log_color)s[%(levelname)4s]%(reset)s %(log_color)s%(message)s%(reset)s",
                                 datefmt=None,
                                 reset=True,
                                 log_colors={
                                     'DEBUG': 'cyan',
                                     'INFO': 'green',
                                     'WARN': 'red',
                                     'ERROR': 'black,bg_red',
                                 },
                                 secondary_log_colors={},
                                 style='%')
    formatter.converter = time.gmtime
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    logger.propagate = False
    return logger


def get_relative_path(file_path):
    if getcwd() in path.abspath(file_path):
        return file_path.replace(getcwd(), '.')
    else:
        return path.relpath(path=file_path, start=curdir)
