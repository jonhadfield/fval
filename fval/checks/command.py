# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

import os
import shlex
from distutils.spawn import find_executable
from subprocess import Popen, PIPE

from fval.external.six import text_type

CHECK_NAME = 'COMMAND'


def run(**kwargs):
    script = kwargs['check_args']['script']
    script = find_executable(script)
    args = kwargs['check_args']['args'] if kwargs['check_args']['args'] else ''
    success_exit_code = kwargs['check_args'].get('success_exit_code')
    if not success_exit_code:
        success_exit_code = 0
    raw_command = '{0} {1} {2}'.format(script, args, kwargs['unit_path'])
    display_command = '{0} {1}'.format(script, args)

    # Make options Windows compatible
    platform = kwargs['config']['platform']
    if platform.startswith('freebsd') or platform.startswith('linux') or platform.startswith('darwin'):
        close_fds = True
        shlex_posix = True
    else:
        close_fds = False
        shlex_posix = False

    command = shlex.split(raw_command, posix=shlex_posix)

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE,
              close_fds=close_fds, bufsize=-1)

    stdout, stderr = p.communicate()
    output = '{0}{1}'.format(' '.join(command), os.linesep)
    output += '>>>>>>>>> stdout' + os.linesep
    if stdout:
        output += text_type(stdout.decode('utf-8'))
    output += '>>>>>>>>> stderr' + os.linesep
    if stderr:
        output += text_type(stderr.decode('utf-8')) + os.linesep
    rc = p.returncode
    if kwargs['config'].get('multiline'):
        message = '{0}:{1}\t{2}'.format(CHECK_NAME, os.linesep, display_command)
    else:
        message = '{0}: {1}'.format(CHECK_NAME, display_command)
    if rc == success_exit_code:
        level = 'INFO'
    else:
        level = 'WARN'

    return dict(message=message, level=level, output=output)
