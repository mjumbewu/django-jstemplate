CHANGES
=======

0.2.1 (2012.01.09)
------------------

* Fixed template reading to explicitly decode template file contents using
  Django's ``FILE_CHARSET`` setting. Thanks Eduard Iskandarov.

* Fixed template-finding failure with non-normalized directories in
  ``ICANHAZ_DIRS``. Thanks Eduard Iskandarov for report and patch.


0.2.0 (2011.06.26)
------------------

* Made template-finding more flexible: ``ICANHAZ_DIR`` is now ``ICANHAZ_DIRS``
  (a list); added ``ICANHAZ_FINDERS``, ``ICANHAZ_APP_DIRNAMES``, and finding of
  templates in installed apps.


0.1.0 (2011.06.22)
------------------

* Initial release.

