This is a django app that wraps PyWPS

It make it possible to use PyWPS through django.

Installation
============

0. Create a virtualenv to hold the installation (This step is
   optional, but highly reccommended).

   .. code:: bash

      virtualenv venv

#. For a normal installation, just use the setup.py file:

   .. code:: bash

      venv/bin/python setup.py install

#. For a developer installation, use pip and the provided requirements file:

   .. code:: bash

      venv/bin/pip install -r requirements.txt

Usage
=====

1. Create your pywps settings file
#. Create a new django project.
#. Modify your settings.py to include the `PYWPS_SETTINGS_FILE` variable that
   points to your pywps settings file
#. Modify your django project's urls.py to include the djangopywps views
