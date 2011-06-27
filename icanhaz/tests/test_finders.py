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
        from icanhaz.finders import BaseFinder
        return BaseFinder()


    def test_find_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.finder.find("name")



class FilesystemFinderTest(TestCase):
    @property
    def finder(self):
        from icanhaz.finders import FilesystemFinder
        return FilesystemFinder()


    @override_settings(ICANHAZ_DIRS=["/one/path", "/another/path"])
    def test_directories(self):
        self.assertEqual(
            self.finder.directories,
            ["/one/path", "/another/path"])


    @override_settings(ICANHAZ_DIRS=[os.path.join(here, "templates")])
    def test_find(self):
        self.assertEqual(
            self.finder.find("testtemplate"),
            os.path.join(here, "templates", "testtemplate.html"))


    @override_settings(ICANHAZ_DIRS=[os.path.join(here, "templates")])
    def test_find_non_existing(self):
        self.assertEqual(self.finder.find("doesntexist"), None)



class AppFinderTest(TestCase):
    @property
    def finder(self):
        from icanhaz.finders import AppFinder
        return AppFinder()


    def test_directories(self):
        with patch(
            "icanhaz.finders.app_template_dirs",
            [os.path.join(here, "templates")]):
            dirs = self.finder.directories

        self.assertEqual(dirs, [os.path.join(here, "templates")])


    @property
    def func(self):
        from icanhaz.finders import _get_app_template_dirs
        return _get_app_template_dirs


    @override_settings(
        INSTALLED_APPS=["icanhaz.tests"],
        ICANHAZ_APP_DIRNAMES=["templates", "jstemplates"])
    def test_get_app_template_dirs(self):
        self.assertEqual(self.func(), [os.path.join(here, "templates")])


    @override_settings(INSTALLED_APPS=["icanhaz.nonexistent"])
    def test_bad_app(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()
