from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from mock import patch

from .mockfinders import MockFinder
from .utils import override_settings



__all__ = ["FindTest", "GetFindersTest"]



class FindTest(TestCase):
    @property
    def func(self):
        from mustachejs.loading import find
        return find


    @patch("mustachejs.loading.finders", [MockFinder("/path/to/a/file.html")])
    def test_find(self):
        self.assertEqual(self.func("file"), "/path/to/a/file.html")


    @patch(
        "mustachejs.loading.finders",
        [MockFinder(), MockFinder("/path/to/a/file.html")])
    def test_find_fallback(self):
        self.assertEqual(self.func("file"), "/path/to/a/file.html")


    @patch("mustachejs.loading.finders", [MockFinder()])
    def test_none_found(self):
        from mustachejs.loading import MustacheJSTemplateNotFound
        with self.assertRaises(MustacheJSTemplateNotFound):
            self.func("file")



class GetFindersTest(TestCase):
    @property
    def func(self):
        from mustachejs.loading import _get_finders
        return _get_finders


    @override_settings(MUSTACHEJS_FINDERS=["mustachejs.tests.mockfinders.MockFinder"])
    def test_get_finders(self):
        finders = self.func()

        self.assertEqual(len(finders), 1)
        self.assertIsInstance(finders[0], MockFinder)


    @override_settings(MUSTACHEJS_FINDERS=["mustachejs.tests.doesntexist.MockFinder"])
    def test_bad_module(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()


    @override_settings(
        MUSTACHEJS_FINDERS=["mustachejs.tests.mockfinders.DoesntExist"])
    def test_bad_attribute(self):
        with self.assertRaises(ImproperlyConfigured):
            self.func()
