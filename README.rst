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

* Set the ``ICANHAZ_DIR`` setting to the full (absolute) path to a directory
  where you will store your ICanHaz templates.

* ``{% load icanhaz %}`` and use ``{% icanhaz "templatename" %}`` in your
  Django templates to safely embed the ICanHaz.js template at
  ``ICANHAZ_DIR/templatename.html`` into your Django template, automatically
  wrapped in ``<script id="templatename" type="text/html">``, ready for
  ``ich.templatename({...})`` in your JavaScript.

``django-icanhaz`` does not bundle `ICanHaz.js`_ or provide any JavaScript
utilities; it just helps you easily embed the templates in your HTML. Include
`ICanHaz.js`_ in your project's static assets and use it in your JS as usual.


Philosophy
----------

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
