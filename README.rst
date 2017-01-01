fval
====
.. image:: https://travis-ci.org/jonhadfield/fval.svg?branch=devel
    :target: https://travis-ci.org/jonhadfield/fval
.. image:: https://img.shields.io/badge/status-alpha-orange.svg
    :target: https://travis-ci.org/jonhadfield/fval


fval is command-line tool for validating files against checks you define in YAML files

Tests currently available:

**syntax**   supply a list of keys and regular expressions to validate the file contents, e.g. a YAML configuration file

**command**    pass the file and arguments to any application and specify the expected exit code

**markup**    specify which markup specification the file should adhere to

**mime type**    specify which mime type the file should be recognised as

Installation
------------

Note: Not yet on pypi whilst still in alpha.

**pip**

``pip install https://github.com/jonhadfield/fval/archive/devel.zip``

**manual**

``git clone https://github.com/jonhadfield/fval``

``cd fval``

``python setup.py install``

Example Usage
-------------

TBC
