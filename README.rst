=================
django-mustachejs
=================

A templatetag for easier integration of `mustache.js`_ JavaScript templates with
Django templates.  Inspired by `ICanHaz.js`_, `django-icanhaz`_, and
`jquery.mustache`_.

.. _mustache.js: http://mustache.github.com/
.. _django-icanhaz: http://github.com/carljm/django-icanhaz
.. _ICanHaz.js: http://icanhazjs.com/
.. _jquery.mustache: https://github.com/AF83/jquery.mustache

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

    pip install django-mustachejs

or get the `in-development version`_::

    pip install django-mustachejs==dev

.. _in-development version: https://github.com/mjumbewu/django-mustachejs/tarball/develop#egg=mustachejs

Usage
-----

* Add ``"mustachejs"`` to your ``INSTALLED_APPS`` setting.

* Set the ``MUSTACHEJS_DIRS`` setting to a list of full (absolute) path to
  directories where you will store your mustache templates.  By default this is
  set to a directory named ``jstemplates``.

* Set the ``MUSTACHEJS_EXTS`` setting to a list of the app should search for
  to find template files.  By default this is set to ``['mustache', 'html']``.
  Order matters (e.g., ``*.mustache`` will take precedence over ``*.html``).

* In your HTML header, include ``mustache/js/mustache-<version>.js``.  The
  versions shipped with django-mustache are ``0.3.0`` and ``0.4.0-dev``.

* ``{% load mustachejs %}`` and use ``{% mustachejs "templatename" %}`` in your
  Django templates to safely embed the mustache.js template at
  ``<MUSTACHEJS_DIRS-entry>/templatename.html`` into your Django template.  It
  will be stored in the ``Mustache.TEMPLATES`` object as a string, accessible
  as ``Mustache.TEMPLATES.templatename``.

* In your JavaScript, use
  ``Mustache.to_html(Mustache.TEMPLATES.templatename, {...}, Mustache.TEMPLATES)``
  to render your mustache template.  Alternatively, if you include the
  ``mustache/js/django.mustache.js`` script in your HTML, you can use
  ``Mustache.template('templatename').render({...})`` to render your mustache
  template.


An Example
----------

For example consider the files ``app/jstemplates/main.mustache``::

    <div>
      <p>This is {{ name }}'s template</p>
    </div>

and ``app/templates/main.html``::

    {% load mustachejs %}

    <html>
    <head>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js"></script>

      <script src="{{ STATIC_URL }}mustache/js/mustache-0.3.0.js"></script>
      <script src="{{ STATIC_URL }}mustache/js/django.mustache.js"></script>
    </head>

    <body>
      <div id="dynamic-area"></div>

      {% mustachejs "main" %}

      <script>
        $(document).ready(function() {

          var $area = $('#dynamic-area')
            , template;

          // Either render by accessing the TEMPLATES object 
          // directly...

          $area.html(Mustache.to_html(Mustache.TEMPLATES.main));

          // ...or render by using a cached template object
          // (requires django.mustache.js)

          template = Mustache.template('main');
          $area.html(template.render());

        });
      </script>
    </body>
    </html>

What's going on?
----------------

Any time you use the ``mustachejs`` template tag::

    {% load mustachejs %}
    {% mustachejs "main" %}

django-mustachejs will generate the following::

    <script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};Mustache.TEMPLATES['main']='<div>\n  <p>This is {{ name }}\'s template</p>\n</div>';</script>

This stores the text of the template in an attribute on the ``Mustache.TEMPLATES``
object (it will first create the object if it does not yet exist).  The
``Mustache.template(...)`` function then creates an object with a ``render(...)`` method
that has a similar signature as ``Mustache.to_html(...)``, except without the template
name as the first parameter.  The ``render`` method will also use the set of templates
in ``Mustache.TEMPLATES`` as partials, allowing any template that django-mustachejs
knows about to be used as a template partial as well.

Advanced usage
--------------

You can also bundle MustacheJS templates with Django reusable apps; by default
``django-mustache`` will look for templates in a ``jstemplates`` subdirectory of
each app in ``INSTALLED_APPS``. The app subdirectory name(s) to check can be
configured via the ``MUSTACHEJS_APP_DIRNAMES`` setting, which defaults to
``["jstemplates"]``.

The finding of templates can be fully controlled via the ``MUSTACHEJS_FINDERS``
setting, which is a list of dotted paths to finder classes. A finder class
should be instantiable with no arguments, and have a ``find(name)`` method
which returns the full absolute path to a template file, given a base-name.

By default, ``MUSTACHEJS_FINDERS`` contains ``"mustachejs.finders.FilesystemFinder"``
(which searches directories listed in ``MUSTACHEJS_DIRS``) and
``"mustachejs.finders.AppFinder"`` (which searches subdirectories named in
``MUSTACHEJS_APP_DIRNAMES`` of each app in ``INSTALLED_APPS``), in that order --
thus templates found in ``MUSTACHEJS_DIRS`` take precedence over templates in
apps.


Rationale (from `django-icanhaz`_)
----------------------------------

The collision between Django templates' use of ``{{`` and ``}}`` as template
variable markers and `mustache.js`_' use of same has spawned a variety of
solutions. `One solution`_ simply replaces ``[[`` and ``]]`` with ``{{`` and
``}}`` inside an ``mustachejs`` template tag; `another`_ makes a valiant attempt
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