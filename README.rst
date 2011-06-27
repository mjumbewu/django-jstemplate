==============
django-icanhaz
==============

A templatetag for easier integration of `ICanHaz.js`_ JavaScript templates with
Django templates.

.. _ICanHaz.js: http://icanhazjs.com

Quickstart
==========

Dependencies
------------

Tested with `Django`_ 1.3 through trunk, and `Python`_ 2.6 and 2.7. Almost
certainly works with older versions of both.

.. _Django: http://www.djangoproject.com/
.. _Python: http://www.python.org/

Installation
------------

Install from PyPI with ``pip``::

    pip install django-icanhaz

or get the `in-development version`_::

    pip install django-icanhaz==dev

.. _in-development version: https://github.com/carljm/django-icanhaz/tarball/master#egg=django_secure-dev

Usage
-----

* Add ``"icanhaz"`` to your ``INSTALLED_APPS`` setting.

* Set the ``ICANHAZ_DIRS`` setting to a list of full (absolute) path to
  directories where you will store your ICanHaz templates.

* ``{% load icanhaz %}`` and use ``{% icanhaz "templatename" %}`` in your
  Django templates to safely embed the ICanHaz.js template at
  ``<ICANHAZ_DIRS-entry>/templatename.html`` into your Django template,
  automatically wrapped in ``<script id="templatename" type="text/html">``,
  ready for ``ich.templatename({...})`` in your JavaScript.

``django-icanhaz`` does not bundle `ICanHaz.js`_ or provide any JavaScript
utilities; it just helps you easily embed the templates in your HTML. Include
`ICanHaz.js`_ in your project's static assets and use it in your JS as usual.


Advanced usage
--------------

You can also bundle ICanHaz templates with Django reusable apps; by default
``django-icanhaz`` will look for templates in a ``jstemplates`` subdirectory of
each app in ``INSTALLED_APPS``. The app subdirectory name(s) to check can be
configured via the ``ICANHAZ_APP_DIRNAMES`` setting, which defaults to
``["jstemplates"]``.

The finding of templates can be fully controlled via the ``ICANHAZ_FINDERS``
setting, which is a list of dotted paths to finder classes. A finder class
should be instantiable with no arguments, and have a ``find(name)`` method
which returns the full absolute path to a template file, given a base-name.

By default, ``ICANHAZ_FINDERS`` contains ``"icanhaz.finders.FilesystemFinder"``
(which searches directories listed in ``ICANHAZ_DIRS``) and
``"icanhaz.finders.AppFinder"`` (which searches subdirectories named in
``ICANHAZ_APP_DIRNAMES`` of each app in ``INSTALLED_APPS``), in that order --
thus templates found in ``ICANHAZ_DIRS`` take precedence over templates in
apps.


Rationale
---------

The collision between Django templates' use of ``{{`` and ``}}`` as template
variable markers and `ICanHaz.js`_' use of same has spawned a variety of
solutions. `One solution`_ simply replaces ``[[`` and ``]]`` with ``{{`` and
``}}`` inside an ``icanhaz`` template tag; `another`_ makes a valiant attempt
to reconstruct verbatim text within a chunk of a Django template after it has
already been mangled by the Django template tokenizer.

I prefer to keep my JavaScript templates in separate files in a dedicated
directory anyway, to avoid confusion between server-side and client-side
templating. So my contribution to the array of solutions is essentially just an
"include" tag that avoids parsing the included file as a Django template (and
for convenience, automatically wraps it in the script tag that `ICanHaz.js`_
expects to find it in).

Enjoy!

.. _one solution: https://gist.github.com/975505
.. _another: https://gist.github.com/629508
