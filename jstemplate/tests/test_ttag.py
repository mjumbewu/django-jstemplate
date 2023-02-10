# -*- coding: utf-8 -*-

import os.path

from django.template import Template, Context, TemplateSyntaxError
from django.test import override_settings, TestCase


__all__ = [
    "MustacheJSTemplateTagTest",
    "RawTemplateTagTest",
    "ICHTemplateTagTest",
    "HandlebarsJSTemplateTagTest",
    "DustTemplateTagTest",
]


DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class BaseJSTemplateTagTestMixin (object):
    # The following should be true for all tag types.  Remember to define
    # tag_string for any derived test classes.

    @override_settings(JSTEMPLATE_DIRS=[DIR], DEBUG=False)
    def test_no_template(self):
        res = Template(
            "{{% load jstemplate %}}{{% {0} 'notemplate' %}}".format(self.tag_string)
            ).render(Context())

        self.assertEqual(res, "")


    @override_settings(JSTEMPLATE_DIRS=[DIR], DEBUG=True)
    def test_multiple_templates_with_regex(self):
        res = Template(
            "{{% load jstemplate %}}{{% {0} '(many.*)' %}}".format(self.tag_string)
            ).render(Context())

        import re
        self.assertEqual(len(re.findall('Mustache #1', res)), 1)
        self.assertEqual(len(re.findall('Mustache #2', res)), 1)
        self.assertEqual(len(re.findall('Mustache #3', res)), 1)


    @override_settings(JSTEMPLATE_DIRS=[DIR], DEBUG=True)
    def test_multiple_templates_with_glob(self):
        res = Template(
            "{{% load jstemplate %}}{{% {0} 'many*' %}}".format(self.tag_string)
            ).render(Context())

        import re
        self.assertEqual(len(re.findall('Mustache #1', res)), 1)
        self.assertEqual(len(re.findall('Mustache #2', res)), 1)
        self.assertEqual(len(re.findall('Mustache #3', res)), 1)


    @override_settings(JSTEMPLATE_DIRS=[DIR], DEBUG=True)
    def test_no_template_debug(self):
        from jstemplate.loading import JSTemplateNotFound
        with self.assertRaises(JSTemplateNotFound):
            Template(
                "{{% load jstemplate %}}{{% {0} 'notemplate' %}}".format(self.tag_string)
                ).render(Context())


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_no_break_out(self):
        res = Template(
                "{{% load jstemplate %}}{{% {0} '../outside_dir' %}}".format(self.tag_string)
                ).render(Context())

        self.assertEqual(res, "")


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_no_absolute(self):
        res = Template(
                "{{% load jstemplate %}}{{% {0} '/testtemplate' %}}".format(self.tag_string)
                ).render(Context())

        self.assertEqual(res, "")


    def test_bad_args(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(
                "{{% load jstemplate %}}{{% {0} %}}".format(self.tag_string)
                ).render(Context())

#    @override_settings(JSTEMPLATE_DIRS=[DIR])
#    def test_calls_preprocessors(self):
#        from jstemplate.tests.mockpreprocessors import MockPreprocessor1
#        from jstemplate.tests.mockpreprocessors import MockPreprocessor2
#        p1 = MockPreprocessor1()
#        p2 = MockPreprocessor2()
#        p1.process = mock.Mock(return_value="duck")
#        p2.process = mock.Mock(return_value="duck")

#        with patch('jstemplate.loading.preprocessors', [p1,p2]):
#            res = Template(
#                      "{{% load jstemplate %}}{{% {0} '/testtemplate' %}}".format(self.tag_string)
#                      ).render(Context())

#            self.assertEqual(p1.process.call_count, 1)
#            self.assertEqual(p2.process.call_count, 1)

class MustacheJSTemplateTagTest(TestCase, BaseJSTemplateTagTestMixin):
    tag_string = 'mustachejs'

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_unicode(self):
        res = Template(
            "{% load jstemplate %}{% mustachejs 'unicodetemplate' %}"
            ).render(Context())

        expected = (
            "<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
            "Mustache.TEMPLATES['unicodetemplate']="
            "'北京';"
            "</script>")

        self.assertEqual(res, expected)


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load jstemplate %}{% mustachejs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
             "<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
             "Mustache.TEMPLATES['testtemplate']="
            r"'<p>Mustache\'s template full of {{ foo }} and \\.</p>\n';"
             "</script>")


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load jstemplate %}{% mustachejs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
             "<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
             "Mustache.TEMPLATES['testtemplate']="
            r"'<p>Mustache\'s template full of {{ foo }} and \\.</p>\n';"
             "</script>")




class ICHTemplateTagTest(TestCase, BaseJSTemplateTagTestMixin):
    tag_string = 'icanhazjs'

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_unicode(self):
        res = Template(
            "{% load jstemplate %}{% icanhazjs 'unicodetemplate' %}"
            ).render(Context())

        expected = (
            '<script type="text/html" id="unicodetemplate">'
            '北京'
            '</script>')

        self.assertEqual(res, expected)


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load jstemplate %}{% icanhazjs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
             '<script type="text/html" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load jstemplate %}{% icanhazjs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
             '<script type="text/html" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


class HandlebarsJSTemplateTagTest(TestCase, BaseJSTemplateTagTestMixin):
    tag_string = 'handlebarsjs'

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_unicode(self):
        res = Template(
            "{% load jstemplate %}{% handlebarsjs 'unicodetemplate' %}"
            ).render(Context())

        expected = (
            '<script type="text/x-handlebars-template" id="unicodetemplate">'
            '北京'
            '</script>')

        self.assertEqual(res, expected)


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load jstemplate %}{% handlebarsjs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
             '<script type="text/x-handlebars-template" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load jstemplate %}{% handlebarsjs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
             '<script type="text/x-handlebars-template" id="testtemplate">'
             "<p>Mustache's template full of {{ foo }} and \\.</p>\n"
             '</script>')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_with_precompile(self):
        res = Template(
            "{% load jstemplate %}{% handlebarsjs 'testtemplate' precompile %}"
            ).render(Context())

        self.assertEqual(
            res,
             '<script type="text/x-handlebars-template" id="testtemplate">'
             '<p>Mustache\'s template full of {{ foo }} and \\.</p>\n'
             '</script><script>(function(H) {var source = document.getElementById("testtemplate").innerHTML,'
             'template = source;'
             'template = H.compile(source);'
             'H.templates = H.templates || {};'
             'H.templates["testtemplate"] = template;})(Handlebars);</script>')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_with_partials(self):
        res = Template(
            "{% load jstemplate %}{% handlebarsjs 'testtemplate' register_partials %}"
            ).render(Context())

        self.assertEqual(
            res,
             '<script type="text/x-handlebars-template" id="testtemplate">'
             '<p>Mustache\'s template full of {{ foo }} and \\.</p>\n'
             '</script><script>(function(H) {var source = document.getElementById("testtemplate").innerHTML,'
             'template = source;'
             'H.registerPartial("testtemplate", template);})(Handlebars);</script>')


class DustTemplateTagTest(TestCase, BaseJSTemplateTagTestMixin):
    tag_string = 'dustjs'

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_unicode(self):
        res = Template(
            "{% load jstemplate %}{% dustjs 'unicodetemplate' %}"
            ).render(Context())

        expected = (
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('北京', 'unicodetemplate');"
                "dust.loadSource(compiled);"
            "}"
            '</script>')

        self.assertEqual(res, expected)


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load jstemplate %}{% dustjs 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('<p>Mustache\\'s template full of {{ foo }} and \\\\.</p>\\n', 'testtemplate');"
                "dust.loadSource(compiled);"
            "}"
            '</script>')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load jstemplate %}{% dustjs templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('<p>Mustache\\'s template full of {{ foo }} and \\\\.</p>\\n', 'testtemplate');"
                "dust.loadSource(compiled);"
            "}"
            '</script>')


class RawTemplateTagTest(TestCase, BaseJSTemplateTagTestMixin):
    tag_string = 'rawjstemplate'

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_unicode(self):
        res = Template(
            "{% load jstemplate %}{% rawjstemplate 'unicodetemplate' %}"
            ).render(Context())

        self.assertEqual(res, '北京')


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_simple(self):
        res = Template(
            "{% load jstemplate %}{% rawjstemplate 'testtemplate' %}"
            ).render(Context())

        self.assertEqual(
            res,
            "<p>Mustache's template full of {{ foo }} and \\.</p>\n")


    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_variable_template_name(self):
        res = Template(
            "{% load jstemplate %}{% rawjstemplate templatename %}").render(
            Context({"templatename": "testtemplate"}))

        self.assertEqual(
            res,
            "<p>Mustache's template full of {{ foo }} and \\.</p>\n")
