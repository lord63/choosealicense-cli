ChooseALicense-cli
==================

|Latest Version| |Build Status| |Coverage Status| |Python Versions|

Bring http://choosealicense.com to your terminal. Choose a license in
your terminal.

.. figure:: https://cloud.githubusercontent.com/assets/5268051/7150903/b7f16168-e354-11e4-91b5-0965a86c8158.jpeg
   :alt: demo

Install
-------

note: please update version to 1.0.0 and above, the github api has changed.

::

    $ pip install -U choosealicense-cli

Usage
-----

List all the available licenses:

::

    $ license show

Show the info of the specified license:

::

    $ license info LICENSE(e.g. mit)

Show the default context for the license template:

::

    $ license context LICENSE(e.g. mit)

Generate a license:

::

    $ license generate LICENSE(e.g. mit)

Get detailed help message via ``license -h`` and
``license show/info/context/generate -h``

Developing
----------

First, prepare your development environment, it is
recommended to use a virtual environment.

Create the virtual environment:

::

    $ python -m venv venv

Activate the virtual environment:

::

    $ source venv/bin/activate

Install the development dependencies:

::

    $ pip install -r dev-requirements.txt

Run the tests:

::

    $ pip install -e . && make test

License
-------

MIT.

.. |Latest Version| image:: http://img.shields.io/pypi/v/choosealicense-cli.svg
   :target: https://pypi.python.org/pypi/choosealicense-cli
.. |Build Status| image:: https://travis-ci.org/lord63/choosealicense-cli.svg
   :target: https://travis-ci.org/lord63/choosealicense-cli
.. |Coverage Status| image:: https://codecov.io/github/lord63/choosealicense-cli/coverage.svg?branch=master
   :target: https://codecov.io/github/lord63/choosealicense-cli?branch=master
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/choosealicense-cli.svg
