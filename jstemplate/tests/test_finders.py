import os

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from mock import patch

from .utils import override_settings



__all__ = ["BaseFinderTest", "FilesystemFinderTest", "AppFinderTest",
           "FilesystemRegexFinderTest"]


here = os.path.abspath(os.path.dirname(__file__))



class BaseFinderTest(TestCase):
    @property
    def finder(self):
        from jstemplate.finders import BaseFinder
        return BaseFinder()


    def test_find_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.finder.find("name")



class FilesystemFinderTest(TestCase):
    @property
    def finder(self):
        from jstemplate.finders import FilesystemFinder
        return FilesystemFinder()


    @override_settings(JSTEMPLATE_DIRS=["/one/path", "/another/path"])
    def test_directories(self):
        self.assertEqual(
            self.finder.directories,
            ["/one/path", "/another/path"])


    @override_settings(JSTEMPLATE_EXTS=["thtml"])
    def test_extensions(self):
        self.assertEqual(
            self.finder.extensions,
            ["thtml"])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_html_file(self):
        self.assertEqual(
            self.finder.find("testtemplate"),
            [("testtemplate", os.path.join(here, "templates", "testtemplate.html"))])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_mustache_file(self):
        # This will not only demonstrate that it finds .mustache files, but also
        # that .mustache files take precedence over .html files.
        self.assertEqual(
            self.finder.find("othertesttemplate"),
            [("othertesttemplate", os.path.join(here, "templates", "othertesttemplate.mustache"))])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_many_files(self):
        self.assertEqual(
            set(self.finder.find("many*")),
            set([("manytemplates1", os.path.join(here, "templates", "manytemplates1.html")),
                 ("manytemplates2", os.path.join(here, "templates", "manytemplates2.mustache")),
                 ("manytemplates3", os.path.join(here, "templates", "manytemplates3.html"))])
        )


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_mustache_file_takes_precedence_over_html(self):
        self.assertEqual(
            self.finder.find("bothtesttemplate"),
            [("bothtesttemplate", os.path.join(here, "templates", "bothtesttemplate.mustache"))])


    @override_settings(
        JSTEMPLATE_DIRS=[os.path.join(here, "..", "tests", "templates")])
    def test_find_non_normalized_dir(self):
        self.assertEqual(
            self.finder.find("testtemplate"),
            [("testtemplate", os.path.join(here, "templates", "testtemplate.html"))])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_non_existing(self):
        self.assertEqual(self.finder.find("doesntexist"), [])


class FilesystemRegexFinderTest(TestCase):
    @property
    def finder(self):
        from jstemplate.finders import FilesystemRegexFinder
        return FilesystemRegexFinder()


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_file(self):
        self.assertEqual(
            self.finder.find("(test.*)"),
            [("testtemplate", os.path.join(here, "templates", "testtemplate.html"))])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_file(self):
        self.assertEqual(
            self.finder.find("(test.*)"),
            [("testtemplate", os.path.join(here, "templates", "testtemplate.html"))])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_requires_match_group(self):
        self.assertEqual(
            self.finder.find("test.*"), [])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_requires_exact_match_for_extensions(self):
        self.assertEqual(
            self.finder.find("(wrong_extension)"), [])


    @override_settings(JSTEMPLATE_DIRS=[os.path.join(here, "templates")])
    def test_find_many_files(self):
        self.assertEqual(
            set(self.finder.find("(many.*)")),
            set([("manytemplates1", os.path.join(here, "templates", "manytemplates1.html")),
                 ("manytemplates2", os.path.join(here, "templates", "manytemplates2.mustache")),
                 ("manytemplates3", os.path.join(here, "templates", "manytemplates3.html"))])
        )


class AppFinderTest(TestCase):
    @property
    def finder(self):
        from jstemplate.finders import AppFinder
        return AppFinder()


    def test_directories(self):
        with patch(
            "jstemplate.finders.app_template_dirs",
            [os.path.join(here, "templates")]):
            dirs = self.finder.directories

        self.assertEqual(dirs, [os.path.join(here, "templates")])


    @property
    def func(self):
        from jstemplate.finders import _get_app_template_dirs
        return _get_app_template_dirs


    @override_settings(
        INSTALLED_APPS=["jstemplate.tests"],
        JSTEMPLATE_APP_DIRNAMES=["templates", "jstemplates"])
    def test_get_app_template_dirs(self):
        self.assertEqual(self.func(), [os.path.join(here, "templates")])


    @override_settings(INSTALLED_APPS=["jstemplate.nonexistent"])
    def test_bad_app(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()
