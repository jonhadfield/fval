fval
====
.. image:: https://travis-ci.org/jonhadfield/fval.svg?branch=devel
    :target: https://travis-ci.org/jonhadfield/fval
.. image:: https://img.shields.io/badge/status-alpha-orange.svg
    :target: https://travis-ci.org/jonhadfield/fval

|


The idea of fval is to validate one or more files, e.g. a source code repository, against a set of tests and then report the findings.
Validation tests are written in YAML files and then run against single files, single directories or an entire filesystem hierarchy.

fval returns an exit code of 0 if all the tests pass, so it can be applied as git pre-commit hook for checking configuration files are valid before allowing them to be committed.


Currently available tests:

**syntax**   supply a list of keys and regular expressions to validate the file contents, e.g. a YAML or Java properties file

**command**    pass the file and arguments to any application and specify the expected exit code

**markup**    specify which markup specification the file should adhere to

**mime type**    specify which mime type the file should be recognised as


Compatibility
-------------
Python 2.7 and above

Tested on Linux and macOS with limited testing on Windows 10


Installation
------------

Note: Not yet on pypi whilst still in alpha.

**pip**

``pip install https://github.com/jonhadfield/fval/archive/devel.zip``

**manual**

::


    git clone https://github.com/jonhadfield/fval
    cd fval
    python setup.py install


Examples
--------

**Ensuring URLs are secure in a single configuration file**

Create a file called test.yml with the following content:

::

    ---
    endpoint_url: http://www.example.com


Create a validator file called .test.yml.fval with content:

::

    syntax:
      markup: yaml
      regexes:
        - endpoint_url: "^https://"

Running ``fval`` will return a warning that the regular expression doesn't match. Modify the endpoint_url to use https and the next run will pass.
