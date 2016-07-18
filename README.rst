
.. This document is intended as the main entry point for new users,
   it serves as the landing page on GitHub and on PyPI and
   it is also used as Quickstart section of the docs.
   Its goal are:
   * inspire and raise interest in new users
   * present one complete end-to-end use case
   * direct interested users to the appropriate project resource
   * state license and open source nature
   * credit contributors
   Anything else should go into docs.

.. NOTE: only the first couple of lines of the README are shown on GitHub mobile

nodev.specs helps you write robust tests that describe the abstract behaviour of your code
leaving many implementation details out of your tests.

The general idea is best explained with an example,
let's write a specification test for the following function ``skip_comments`` that
returns the non-comment part of every line in the input file::

    def skip_comments(stream):
        return [line.partition('#')[0] for line in stream]

The simplest unit test may look like the following::

    def test_skip_comments():
        assert skip_comments(['# comment']) == ['']
        assert skip_comments(['value # comment']) == ['value ']
        assert skip_comments(['value 1', '', 'value 2']) == ['value 1', '', value 2']

Such a unit test is much more tied to current ``skip_comments`` implementation than it needs to be
and the test will need update every time a tiny feature is added,
like turning the function into a generator::

    def skip_comments(stream):
        for line in stream:
            yield line.partition('#')[0]

This can be fixed by re-writing the test in more generic way::

    def test_skip_comments():
        assert '' in skip_comments(['# comment'])
        assert 'value ' in skip_comments(['value # comment'])
        assert 'value 1' in skip_comments(['value 1', '', 'value 2'])
        assert 'value 2' in skip_comments(['value 1', '', 'value 2'])

Let's re-write the test making use of the ``nodev.specs.FlatContainer`` helper::

    def test_skip_comments():
        assert '' in FlatContainer(skip_comments(['# comment']))
        assert 'value ' in FlatContainer(skip_comments(['value # comment']))
        assert 'value 1' in FlatContainer(skip_comments(['value 1', '', 'value 2']))
        assert 'value 2' in FlatContainer(skip_comments(['value 1', '', 'value 2']))

Now you can choose to skip empty lines returning the current line index instead::

    def skip_comments(stream):
        for index, line in enumerate(stream):
            value = line.partition('#')[0]
            if value:
                yield index, value

Or return also the comment for every line::

    def skip_comments(stream):
        for index, line in enumerate(stream):
            value, sep, comment = line.partition('#')
            if value:
                yield index, value, sep + comment

The nodev test needs no update because it makes almost no assumption on the details
of the return value.


Project resources
-----------------

============= ======================
Support       https://stackoverflow.com/search?q=nodev
Development   https://github.com/nodev-io/nodev.specs
Discussion    To be decided, see issue `#15 <https://github.com/nodev-io/pytest-nodev/issues/15>`_
              of the pytest-nodev repository.
Download      https://pypi.python.org/pypi/nodev.specs
Code quality  .. image:: https://api.travis-ci.org/nodev-io/nodev.specs.svg?branch=master
                :target: https://travis-ci.org/nodev-io/nodev.specs/branches
                :alt: Build Status on Travis CI
              .. image:: https://ci.appveyor.com/api/projects/status/github/nodev-io/nodev.specs?branch=master
                :target: https://ci.appveyor.com/project/alexamici/nodev.specs/branch/master
                :alt: Build Status on AppVeyor
              .. image:: https://coveralls.io/repos/nodev-io/nodev.specs/badge.svg?branch=master&service=github
                :target: https://coveralls.io/github/nodev-io/nodev.specs?branch=master
                :alt: Coverage Status on Coveralls
nodev website http://nodev.io
============= ======================


Contributing
------------

Contributions are very welcome. Please see the `CONTRIBUTING`_ document for
the best way to help.
If you encounter any problems, please file an issue along with a detailed description.

.. _`CONTRIBUTING`: https://github.com/nodev-io/nodev.specs/blob/master/CONTRIBUTING.rst

Authors:

- Alessandro Amici - `@alexamici <https://github.com/alexamici>`_

Sponsors:

- .. image:: http://www.bopen.it/wp-content/uploads/2016/01/logo-no-back.png
      :target: http://bopen.eu/
      :alt: B-Open Solutions srl


License
-------

nodev.specs is free and open source software
distributed under the terms of the `MIT <http://opensource.org/licenses/MIT>`_ license.
