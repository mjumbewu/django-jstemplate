.. django-mustachejs documentation master file, created by
   sphinx-quickstart on Fri Aug 17 03:28:33 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
django-mustachejs
=================

A templatetag framework for easier integration of `mustache.js`_ JavaScript
templates with Django templates. Inspired by `ICanHaz.js`_, `django-icanhaz`_,
and `jquery.mustache`_.

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

* In your HTML header, include your desired version of mustache.js.  This
  application comes with two versions of the library available at
  ``mustache/js/mustache-<version>.js``. The versions shipped with
  django-mustache are ``0.3.0`` and ``0.4.0-dev``.

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

Flavors of Mustache
-------------------

In addition to ``{% mustachejs ... %}``, django-mustachejs comes with several
template tags that you can use to render your mustache templates:

* ``{% dustjs ... %}`` renders templates ready for consumption by dust.js
* ``{% mustacheich ... %}`` renders templates ready for consumption by
  ICanHaz.js
* ``{% mustacheraw ... %}`` renders the raw contents of a mustache template,
  after preprocessing

Matching Multiple Template Files
--------------------------------

The name provided to the template tag can be a string that will match a single
file, a file glob pattern, or a regular expression. Using the template tag ``{%
mustachejs [glob/regex] %}`` in your Django templates will embed all files
matching that regex in the template directories. So, ``{% mustachejs
'(.*_template)' %}`` and ``{% mustachejs '*_template' %}`` would both match
`note_template.html` and `comment_template.html`, giving them templatename
`note_template` and `comment_template`, respectively. (Note that the regular
expression pattern must contain parentheses denoting a single matching group;
this group will become the name of the template).


Internationalization (i18n)
===========================

django-mustachejs supports internationalization tags.  In your settings module,
set the ``MUSTACHEJS_I18N_TAGS`` variables (default: ``('_', 'i18n')``).  These
tags can be used to preprocess the javascript templates into translatable
content. For example::

    <div>{{#_}}Hello, {{name}}.  I like your {{color}} {{thing}}?{{/_}}</div>

may render to::

    <div>Salut, {{name}}.  J'aime votre {{thing}} {{color}}?</div>

The translatable strings will be picked up by Django's ``makemessages``
management command.


Settings
========

* Set ``MUSTACHEJS_FINDERS`` to configure the dotted class names of the finders
  the application will use.  By default, this is the following list::

    ["mustachejs.finders.FilesystemFinder",
     "mustachejs.finders.AppFinder",
     "mustachejs.finders.FilesystemRegexFinder",
     "mustachejs.finders.AppRegexFinder",]

* Set the ``MUSTACHEJS_DIRS`` setting to a list of full (absolute) path to
  directories where you will store your mustache templates.  By default this is
  an empty list.

* Set ``MUSTACHEJS_APP_DIRNAMES`` to a list of directory names that can be
  found under directories of applications specified in ``INSTALLED_APPS``.  By
  default, this setting has the value of ``["jstemplates"]``.

* Set the ``MUSTACHEJS_EXTS`` setting to a list of the app should search for
  to find template files.  By default this is set to ``['mustache', 'html']``.
  Order matters (e.g., ``*.mustache`` will take precedence over ``*.html``).

* Set the ``MUSTACHEJS_PREPROCESSORS`` variable to control how the templates
  are preprocessed.  By default, there is one preprocessor activated::

    ['mustachejs.preprocessors.I18nPreprocessor']

  The ``I18nPreprocessor`` will translate marked strings before rendering the
  template.  To disable this feature, set ``MUSTACHEJS_PREPROCESSORS`` to an
  empty list.

* Set ``MUSTACHEJS_I18N_TAGS`` to the names of the tags used to mark strings
  for internationalization.  By default, this is set to the list::

    ["_", "i18n"]

  Meaning that text falling between the tags ``{{#_}}...{{/_}}`` and
  ``{{#i18n}}...{{/i18n}}`` will be marked for translation.


Advanced usage
==============

Custom Finders
--------------

The finding of templates can be fully controlled via the ``MUSTACHEJS_FINDERS``
setting, which is a list of dotted paths to finder classes. A finder class
should be instantiable with no arguments, and have a ``find(name)`` method
which returns either (1) the full absolute path to a template file, given a
base-name, or (2) a list of (template name, template file path) pairs according
to the given base name.

By default, ``MUSTACHEJS_FINDERS`` contains ``"mustachejs.finders.FilesystemFinder"``
(which searches directories listed in ``MUSTACHEJS_DIRS``),
``"mustachejs.finders.AppFinder"`` (which searches subdirectories named in
``MUSTACHEJS_APP_DIRNAMES`` of each app in ``INSTALLED_APPS``),
``"mustachejs.finders.FilesystemRegexFinder"``, and
``"mustachejs.finders.AppRegexFinder"``, in that order --
thus templates found in ``MUSTACHEJS_DIRS`` take precedence over templates in
apps, and templates identified by file glob patterns take precedence over those
identified by regular expression patterns.

Custom Flavors
--------------

It is simple to extend django-mustachejs to prepare your mustache templates to
be used with your favorite Javascript library creating a template node class
that derives from ``mustachejs.templatetags.BaseMustacheNode``, and overriding
a single function.  Refer to the existing tag definitions for ``mustachejs``,
``mustacheich``, ``mustacheraw``, and ``dustjs`` for more information.

Source
======

The source for django-mustachejs is available on `GitHub`_

.. _GitHub: http://github.com/mjumbewu/django-mustachejs/
