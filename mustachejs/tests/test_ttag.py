import os.path

from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

from .utils import override_settings



__all__ = [
    "JSTemplateTagTest",
    "RawTemplateTagTest",
    "ICHTemplateTagTest",
    "DustTemplateTagTest",
]


DIR = os.path.join(os.path.dirname(__file__), "templates")


class BaseMustacheJSTagTestMixin (object):
    # The following should be true for all tag types.  Remember to define
    # tag_string for any derived test classes.

    @override_settings(MUSTACHEJS_DIRS=[DIR], DEBUG=False)
    def test_no_template(self):
        res = Template(
            "{{% load mustachejs %}}{{% {} 'notemplate' %}}".format(self.tag_string)
            ).render(Context())

        self.assertEqual(res, "")


    @override_settings(MUSTACHEJS_DIRS=[DIR], DEBUG=True)
    def test_no_template_debug(self):
        from mustachejs.loading import MustacheJSTemplateNotFound
        with self.assertRaises(MustacheJSTemplateNotFound):
            Template(
                "{{% load mustachejs %}}{{% {} 'notemplate' %}}".format(self.tag_string)
                ).render(Context())


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_no_break_out(self):
        res = Template(
                "{{% load mustachejs %}}{{% {} '../outside_dir' %}}".format(self.tag_string)
                ).render(Context())

        self.assertEqual(res, "")


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_no_absolute(self):
        res = Template(
                "{{% load mustachejs %}}{{% {} '/testtemplate' %}}".format(self.tag_string)
                ).render(Context())

        self.assertEqual(res, "")


    def test_bad_args(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{{% load mustachejs %}}{{% {} %}}".format(self.tag_string)
                ).render(Context())

class JSTemplateTagTest(TestCase, BaseMustacheJSTagTestMixin):
    tag_string = 'mustachejs'

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




class ICHTemplateTagTest(TestCase, BaseMustacheJSTagTestMixin):
    tag_string = 'mustacheich'

    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load mustachejs %}{% mustacheich 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
             '<script type="text/html" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load mustachejs %}{% mustacheich templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
             '<script type="text/html" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


class DustTemplateTagTest(TestCase, BaseMustacheJSTagTestMixin):
    tag_string = 'dustjs'

    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load mustachejs %}{% dustjs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('<p>Mustache\\'s template full of {{ foo }} and \\\\.</p>\\n', 'testtemplate');"
                "dust.loadSource(compiled);"
            "}"
            '</script>')


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load mustachejs %}{% dustjs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('<p>Mustache\\'s template full of {{ foo }} and \\\\.</p>\\n', 'testtemplate');"
                "dust.loadSource(compiled);"
            "}"
            '</script>')


class RawTemplateTagTest(TestCase, BaseMustacheJSTagTestMixin):
    tag_string = 'mustacheraw'

    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load mustachejs %}{% mustacheraw 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
            "<p>Mustache's template full of {{ foo }} and \\.</p>\n")


    @override_settings(MUSTACHEJS_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load mustachejs %}{% mustacheraw templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
            "<p>Mustache's template full of {{ foo }} and \\.</p>\n")
