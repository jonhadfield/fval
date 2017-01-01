#!/usr/bin/env python

import os
import re
import sys

from setuptools import (setup, find_packages)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()

install_requires = ['colorama',
                    'colorlog',
                    'PyYAML>=3.11',
                    'file-magic']
try:
    import concurrent.futures
except ImportError:
    install_requires.append('futures')

if sys.version_info < (2, 7):
    exit('Python version 2.7 or above is required.')

test_requirements = ['pytest>=3.0.3', 'pytest-cov>=2.4.0']

with open('fval/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

readme = open('README.rst').read()
long_description = readme
setup(
    name='fval',
    version=version,
    description='A file validator.',
    long_description=long_description,
    author='Jon Hadfield',
    author_email='jon@lessknown.co.uk',
    url='http://github.com/jonhadfield/fval',
    packages=find_packages(),
    data_files=[
        ('{0}/.fval'.format(os.path.expanduser('~')),
         ['samples/fval.cfg'])
    ],
    entry_points={
        'console_scripts': [
            'fval = fval:main'
        ],
    },
    include_package_data=True,
    install_requires=install_requires,
    license='MIT',
    scripts=['bin/fval'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: BSD :: Linux',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    tests_require=install_requires + test_requirements,
)
