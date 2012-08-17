=================
django-mustachejs
=================

|build status|_

.. |build status| image:: https://secure.travis-ci.org/mjumbewu/django-mustachejs.png
.. _build status: https://secure.travis-ci.org/mjumbewu/django-mustachejs

A templatetag framework for easier integration of `mustache.js`_ JavaScript
templates with Django templates. Inspired by `ICanHaz.js`_, `django-icanhaz`_,
and `jquery.mustache`_.

.. _mustache.js: http://mustache.github.com/
.. _django-icanhaz: http://github.com/carljm/django-icanhaz
.. _ICanHaz.js: http://icanhazjs.com/
.. _jquery.mustache: https://github.com/AF83/jquery.mustache

Quick Usage
-----------

(Read the full docs on `Read the Docs`_)

.. _Read the Docs: http://django-mustachejs.readthedocs.org/en/latest/

Add ``"mustachejs"`` to your ``INSTALLED_APPS`` setting.

``app/jstemplates/main.mustache``::

    <div>
      <p>This is {{ name }}'s template</p>
    </div>

``app/templates/main.html``::

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

          template = Mustache.template('main');
          $area.html(template.render());

        });
      </script>
    </body>
    </html>


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
