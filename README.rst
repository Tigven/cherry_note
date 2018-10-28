Cherry Note
===========

  CherryTree_ web version
.. _CherryTree: https://www.giuspen.com/cherrytree/

Deployment
----------
::

  ``$ ./setup.sh``
  ``$ nano .env # setting up values``
  $`` ./manage.py loaddata ./cherry_note/fixtures/notes.json # filling DB with test data``

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



