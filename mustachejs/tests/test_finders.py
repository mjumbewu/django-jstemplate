import os

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from mock import patch

from .utils import override_settings



__all__ = ["BaseFinderTest", "FilesystemFinderTest", "AppFinderTest"]


here = os.path.abspath(os.path.dirname(__file__))



class BaseFinderTest(TestCase):
    @property
    def finder(self):
        from mustachejs.finders import BaseFinder
        return BaseFinder()


    def test_find_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.finder.find("name")



class FilesystemFinderTest(TestCase):
    @property
    def finder(self):
        from mustachejs.finders import FilesystemFinder
        return FilesystemFinder()


    @override_settings(MUSTACHEJS_DIRS=["/one/path", "/another/path"])
    def test_directories(self):
        self.assertEqual(
            self.finder.directories,
            ["/one/path", "/another/path"])


    @override_settings(MUSTACHEJS_EXTS=["thtml"])
    def test_extensions(self):
        self.assertEqual(
            self.finder.extensions,
            ["thtml"])


    @override_settings(MUSTACHEJS_DIRS=[os.path.join(here, "templates")])
    def test_find_html_file(self):
        self.assertEqual(
            self.finder.find("testtemplate"),
            os.path.join(here, "templates", "testtemplate.html"))


    @override_settings(MUSTACHEJS_DIRS=[os.path.join(here, "templates")])
    def test_find_mustache_file(self):
        # This will not only demonstrate that it finds .mustache files, but also
        # that .mustache files take precedence over .html files.
        self.assertEqual(
            self.finder.find("othertesttemplate"),
            os.path.join(here, "templates", "othertesttemplate.mustache"))


    @override_settings(MUSTACHEJS_DIRS=[os.path.join(here, "templates")])
    def test_mustache_file_takes_precedence_over_html(self):
        self.assertEqual(
            self.finder.find("bothtesttemplate"),
            os.path.join(here, "templates", "bothtesttemplate.mustache"))


    @override_settings(
        MUSTACHEJS_DIRS=[os.path.join(here, "..", "tests", "templates")])
    def test_find_non_normalized_dir(self):
        self.assertEqual(
            self.finder.find("testtemplate"),
            os.path.join(here, "templates", "testtemplate.html"))


    @override_settings(MUSTACHEJS_DIRS=[os.path.join(here, "templates")])
    def test_find_non_existing(self):
        self.assertEqual(self.finder.find("doesntexist"), None)



class AppFinderTest(TestCase):
    @property
    def finder(self):
        from mustachejs.finders import AppFinder
        return AppFinder()


    def test_directories(self):
        with patch(
            "mustachejs.finders.app_template_dirs",
            [os.path.join(here, "templates")]):
            dirs = self.finder.directories

        self.assertEqual(dirs, [os.path.join(here, "templates")])


    @property
    def func(self):
        from mustachejs.finders import _get_app_template_dirs
        return _get_app_template_dirs


    @override_settings(
        INSTALLED_APPS=["mustachejs.tests"],
        MUSTACHEJS_APP_DIRNAMES=["templates", "jstemplates"])
    def test_get_app_template_dirs(self):
        self.assertEqual(self.func(), [os.path.join(here, "templates")])


    @override_settings(INSTALLED_APPS=["mustachejs.nonexistent"])
    def test_bad_app(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()
