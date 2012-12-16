=================
django-jstemplate
=================

|build status|_

.. |build status| image:: https://secure.travis-ci.org/mjumbewu/django-jstemplate.png
.. _build status: https://secure.travis-ci.org/mjumbewu/django-jstemplate

A templatetag framework for easier integration of `mustache.js`_, `dust.js`_,
`handlebars.js`_, or other JavaScript templates with Django templates. Also will
wrap your templates in elements expected for libraries such as `ICanHaz.js`_.
Django-jstemplates is extensible, so if your favorite template library is not
included, it's easy to add.  Inspired by `django-icanhaz`_.

.. _mustache.js: http://mustache.github.com/
.. _dust.js: http://akdubya.github.com/dustjs/
.. _handlebars.js: http://handlebarsjs.com/
.. _ICanHaz.js: http://icanhazjs.com/
.. _django-icanhaz: http://github.com/carljm/django-icanhaz

Quick Usage
-----------

(Read the full docs on `Read the Docs`_)

.. _Read the Docs: http://django-jstemplate.readthedocs.org/en/latest/

Add ``"jstemplate"`` to your ``INSTALLED_APPS`` setting.

Download the templating library of your choice (I like to go straight
mustache.js)::

    wget https://raw.github.com/janl/mustache.js/master/mustache.js
    mv mustache.js app/static/libs/

``app/jstemplates/main.mustache``::

    <div>
      <p>This is {{ name }}'s template</p>
    </div>

``app/templates/main.html``::

    {% load jstemplate %}

    <html>
    <head>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js"></script>
      <script src="{{ STATIC_URL }}libs/mustache.js"></script>
      <script src="{{ STATIC_URL }}libs/django.mustache.js"></script>
    </head>

    <body>
      <div id="dynamic-area"></div>

      {% mustachejs "main" %}

      <script>
        $(document).ready(function() {

          var $area = $('#dynamic-area')
            , template;

          template = Mustache.template('main');
          $area.html(template.render());

        });
      </script>
    </body>
    </html>


Rationale
---------

The collision between Django templates' use of ``{{`` and ``}}`` as template
variable markers and `mustache.js`_' use of same has spawned a variety of
solutions. `One solution`_ simply replaces ``[[`` and ``]]`` with ``{{`` and
``}}`` inside an ``mustachejs`` template tag; `another`_ makes a valiant attempt
to reconstruct verbatim text within a chunk of a Django template after it has
already been mangled by the Django template tokenizer.

I prefer to keep my JavaScript templates in separate files in a dedicated
directory anyway, to avoid confusion between server-side and client-side
templating. So this solution is essentially just an "include" tag that avoids
parsing the included file as a Django template.

Enjoy!

.. _one solution: https://gist.github.com/975505
.. _another: https://gist.github.com/629508
