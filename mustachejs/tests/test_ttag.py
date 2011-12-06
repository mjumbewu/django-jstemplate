import os.path

from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

from .utils import override_settings



__all__ = ["TemplateTagTest"]


DIR = os.path.join(os.path.dirname(__file__), "templates")


class TemplateTagTest(TestCase):
    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load mustachejs %}{% mustachejs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
             "<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
             "Mustache.TEMPLATES['testtemplate']="
            r"'<p>Mustache\'s template full of {{ foo }} and \\.</p>\n';"
             "</script>")


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load mustachejs %}{% mustachejs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
             "<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
             "Mustache.TEMPLATES['testtemplate']="
            r"'<p>Mustache\'s template full of {{ foo }} and \\.</p>\n';"
             "</script>")


    @override_settings(MUSTACHEJS_DIRS=[DIR], DEBUG=False)
    def test_no_template(self):
        res = Template(
            "{% load mustachejs %}{% mustachejs 'notemplate' %}"
            ).render(Context())

        self.assertEqual(res, "")


    @override_settings(MUSTACHEJS_DIRS=[DIR], DEBUG=True)
    def test_no_template_debug(self):
        from mustachejs.loading import MustacheJSTemplateNotFound
        with self.assertRaises(MustacheJSTemplateNotFound):
            Template(
                "{% load mustachejs %}{% mustachejs 'notemplate' %}"
                ).render(Context())


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_no_break_out(self):
        res = Template(
                "{% load mustachejs %}{% mustachejs '../outside_dir' %}"
                ).render(Context())

        self.assertEqual(res, "")


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_no_absolute(self):
        res = Template(
                "{% load mustachejs %}{% mustachejs '/testtemplate' %}"
                ).render(Context())

        self.assertEqual(res, "")


    def test_bad_args(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{% load mustachejs %}{% mustachejs %}"
                ).render(Context())
