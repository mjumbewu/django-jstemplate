CHANGES
=======

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
