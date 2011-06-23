import os.path

from django.core.exceptions import SuspiciousOperation
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

from .utils import override_settings



__all__ = ["ICanHazTest"]


DIR = os.path.join(os.path.dirname(__file__), "templates")


class ICanHazTest(TestCase):
    @override_settings(ICANHAZ_DIR=DIR)
    def test_simple(self):
        res = Template(
            "{% load icanhaz %}{% icanhaz 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
            '<script id="testtemplate" type="text/html">\n'
            '<p>A template full of {{ foo }}.</p>\n\n</script>\n')


    @override_settings(ICANHAZ_DIR=DIR)
    def test_variable_template_name(self):
        res = Template(
            "{% load icanhaz %}{% icanhaz templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
            '<script id="testtemplate" type="text/html">\n'
            '<p>A template full of {{ foo }}.</p>\n\n</script>\n')


    @override_settings(ICANHAZ_DIR=DIR, DEBUG=False)
    def test_no_template(self):
        res = Template(
            "{% load icanhaz %}{% icanhaz 'notemplate' %}"
            ).render(Context())

        self.assertEqual(res, "")


    @override_settings(ICANHAZ_DIR=DIR, DEBUG=True)
    def test_no_template_debug(self):
        with self.assertRaises(IOError):
            Template(
                "{% load icanhaz %}{% icanhaz 'notemplate' %}"
                ).render(Context())


    @override_settings(ICANHAZ_DIR=DIR)
    def test_suspicious(self):
        with self.assertRaises(SuspiciousOperation):
            Template(
                "{% load icanhaz %}{% icanhaz '../testtemplate' %}"
                ).render(Context())


    @override_settings(ICANHAZ_DIR=DIR)
    def test_suspicious_absolute(self):
        with self.assertRaises(SuspiciousOperation):
            Template(
                "{% load icanhaz %}{% icanhaz '/testtemplate' %}"
                ).render(Context())


    def test_bad_args(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load icanhaz %}{% icanhaz %}"
                ).render(Context())
