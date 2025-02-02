etiketle
========

Labeling System

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

  $ brew install postgresql
  $ python3 -m venv .venv
  $ source .venv/bin/activate
  $ pip install -r requirements/local.txt

  $ psql postgres

    CREATE DATABASE etiketle;
    CREATE USER etiketle WITH PASSWORD 'etiketle';
    ALTER ROLE etiketle SET client_encoding TO 'utf8';
    ALTER ROLE etiketle SET default_transaction_isolation TO 'read committed';
    ALTER ROLE etiketle SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE etiketle TO etiketle;

  $ python manage.py migrate
  $ python manage.py createsuperuser
  $ python manage.py runserver


* Navigate to https://localhost:8000/admin/
* Login with the superuser you created
* Create a new team
* Create a new project
* Create users if needed.
* Create a annotation config.
* Create annotation options
* Create a new dataset and upload a CSV file.


Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy etiketle

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

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Deployment
----------

The following details how to deploy this application.

Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html
