CHANGES
=======

1.3.3
------------------

* Fix compatibility with Python 3.2. Explicity unicode literals (i.e., u'...')
  are not supported in Python 3.2 and cause a syntax error. Support was revived
  in Python 3.3. Python 2.6 and 2.7 allow using unicode string literals by
  default with `from __future__ import unicode_literals`, so we use that here.

1.3.3
------------------

* Sort translatable strings so that results are consistent across Python
  versions.

1.3.2
------------------

* All template renderers handle unicode characters.

1.3.1
------------------

* Bug fix: Closure that was registering Handlbars partials was not wrapped in 
  parentheses.

1.3.0
------------------

* Add a short translation form::

      {{ _ 'this is translatable' }}

1.2.1
------------------

* Allow optional precompiling and and registering of partials for the
  Handlebars.js tag. For example::

      {% handlebarsjs '(.*)' precompile register_partials }

  This will add a `templates` object to `Handlebars`, and register all
  templates for use as partials.

1.2.0
------------------

* Add Handlebars.js support

1.1.1
------------------

* Fix setup script requirements

1.1.0
------------------

* Python 3 support!

1.0.3
------------------

* Move the static/mustache/js/ folder to static/libs/

1.0.2
------------------

* Update MANIFEST file to use "jstemplate" folder instead of "mustachejs"

1.0.1
------------------

* Simplify the template tag methods, and get rid of unused imports in the
  template tag modules
* Update project references in the docs

1.0.0
------------------

* Rename project to "django-jstemplate" (from "django-mustachejs")
* Rename the "mustacheraw" template tag to "rawjstemplate"
* Rename the "mustacheich" template tag to "icanhazjs"

0.8.3
------------------

* Fix incorrect identifier name in makemessages command

0.8.2
------------------

* Fix the FilesystemRegexFinder to match exactly the extensions specified in
  the configuration, and no more

0.8.1
------------------

* Fix makemessages to work with recent code updates

0.8.0
------------------

* Have the regex finder respect the MUSTACHEJS_EXTS setting
* Update normal file finders to use glob patterns

0.7.4
------------------

* Fix i18n preprocessor for python 2.6 compatibility

0.7.3
------------------

* Correctly escaped translated strings.

0.7.2
------------------

* Changed search pattern to be non-greedy.

0.7.1
------------------

* Handle translation strings with new lines.

0.7.0
------------------

* Pulled in commit from django-icanhaz to load templates using regular
  expressions.

* Added preprocessing framework, and a preprocessor for i18n.

* Hijack the makemessages command to find js template messages as well.

0.6.0
------------------

* Add ``dustjs`` tag to insert a script block to create a compiled dustjs
  template.  Thanks to `Gehan Gonsalkorale <https://github.com/gehan>`_.

0.5.0
------------------

* Add ``mustacheraw`` tag to insert just the raw text of a mustacehe template.
  Thanks to Greg Hinch.

* Add ``mustacheich`` tag to insert a mustache script block as icanhaz expects.

0.4.1 (2012.01.09)
------------------

* Fixed template reading to explicitly decode template file contents using
  Django's ``FILE_CHARSET`` setting. Thanks Eduard Iskandarov.

* Fixed template-finding failure with non-normalized directories in
  ``MUSTACHEJS_DIRS``. Thanks Eduard Iskandarov for report and patch.


0.4.0
------------------

* Add the MUSTACHEJS_EXTS configuration variable for specifying the extensions
  allowed for template files located by the FilesystemFinder (and, by extension,
  the AppFinder).


0.3.3
------------------

* Add a package_data value to the setup call


0.3.2
------------------

* Add the MANIFEST.in file itself as an entry in MANIFEST.in.


0.3.0
------------------

* Change the name from django-icanhaz to django-mustachejs.
* Remove dependency on ICanHaz.js.  I like the library, but the maintainers
  were not responsive enough for now.  Use Mustache.js straight, with a little
  bit of minimal sugar.  Templates are rendered to straight Javascript.


0.2.0 (2011.06.26)
------------------

* Made template-finding more flexible: ``ICANHAZ_DIR`` is now ``ICANHAZ_DIRS``
  (a list); added ``ICANHAZ_FINDERS``, ``ICANHAZ_APP_DIRNAMES``, and finding of
  templates in installed apps.


0.1.0 (2011.06.22)
------------------

* Initial release.
