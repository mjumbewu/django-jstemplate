from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from mock import patch

from .mockfinders import MockFinder
from .utils import override_settings



__all__ = ["FindTest", "GetFindersTest"]



class FindTest(TestCase):
    @property
    def func(self):
        from jstemplate.loading import find
        return find


    @patch("jstemplate.loading.finders", [MockFinder("/path/to/a/file.html")])
    def test_find(self):
        self.assertEqual(self.func("file"), [("file", "/path/to/a/file.html")])


    @patch(
        "jstemplate.loading.finders",
        [MockFinder(), MockFinder("/path/to/a/file.html")])
    def test_find_fallback(self):
        self.assertEqual(self.func("file"), [("file", "/path/to/a/file.html")])


    @patch("jstemplate.loading.finders", [MockFinder()])
    def test_none_found(self):
        from jstemplate.loading import JSTemplateNotFound
        with self.assertRaises(JSTemplateNotFound):
            self.func("file")



class GetFindersTest(TestCase):
    @property
    def func(self):
        from jstemplate.loading import _get_finders
        return _get_finders


    @override_settings(JSTEMPLATE_FINDERS=["jstemplate.tests.mockfinders.MockFinder"])
    def test_get_finders(self):
        finders = self.func()

        self.assertEqual(len(finders), 1)
        self.assertIsInstance(finders[0], MockFinder)


    @override_settings(JSTEMPLATE_FINDERS=["jstemplate.tests.doesntexist.MockFinder"])
    def test_bad_module(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()


    @override_settings(
        JSTEMPLATE_FINDERS=["jstemplate.tests.mockfinders.DoesntExist"])
    def test_bad_attribute(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()
