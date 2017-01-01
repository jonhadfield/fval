# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals, print_function)

import os

CHECK_NAME = 'MIME_TYPE'


def run(**kwargs):
    try:
        import magic
        # TODO: Check file-magic imported and not python-magic/filemagic
    except (ImportError, TypeError):
        return dict(message='MIME_TYPE: Failed to check as '
                            '\'python-magic\' not installed', level='ERROR')
    except:
        return dict(message='MIME_TYPE: Unhandled exception', level='ERROR')
    requested_file_format = kwargs['check_args']
    content_as_bytes = kwargs['unit_content']
    try:
        content_as_bytes = str.encode(kwargs['unit_content'])
    except:
        pass
    detected_mime_type = magic.detect_from_content(content_as_bytes).mime_type
    message = '{0}: {1}'.format(CHECK_NAME, requested_file_format)
    if not detected_mime_type == requested_file_format:
        level = 'WARN'
        message += ' (Detected: {0})'.format(detected_mime_type)
    else:
        level = 'INFO'
    output = kwargs['unit_path'] + os.linesep + message + os.linesep
    return dict(message=message, level=level, output=output)
