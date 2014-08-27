This is a django app that wraps PyWPS

It make it possible to use PyWPS through django.

Installation
============

0. Create a virtualenv to hold the installation (This step is
   optional, but highly reccommended).

   .. code:: bash

      virtualenv venv
      source venv/bin/activate

#. Install the following system-wide dependencies:

   .. code:: bash

      sudo apt-get install libxml2 libxml2-dev libxslt1.1 libxslt1-dev

#. Install lxml, which is required by pywps.

   .. code:: bash

      pip install lxml

#. Install pywps from its source code repository using pip

   .. code:: bash

      pip install git+https://github.com/geopython/PyWPS.git#egg=pywps

#. Install this repository using pip

   .. code:: bash

      pip install git+https://github.com/ricardogsilva/django-pywps.git#egg=django-pywps

Usage
=====

1. Create your pywps settings file
#. Create a new django project.
#. Modify your settings.py to include the `PYWPS_SETTINGS_FILE` variable that
   points to your pywps settings file
#. Modify your django project's urls.py to include the djangopywps views
