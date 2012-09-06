import mock
import os.path

from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from mock import patch

from jstemplate.management.commands import makemessages

from .utils import override_settings

DIR = os.path.join(os.path.dirname(__file__), "project", "project", "jstemplates")

class MonkeyPatchedTemplatizeTest (TestCase):

    @override_settings(JSTEMPLATE_DIRS=[DIR])
    def test_translateable_strings_are_discovered(self):
        filepath = os.path.join(DIR, 'my-template.html')
        result = makemessages.templatize(None, filepath)
        self.assertEqual(result, '''_("""Here is
      a multi-line
      string
""")
_("""it's Mustache's turn to do i18n""")
_("""this is a {{ string }} {{# with }} variables {{/ with }}""")
_("""this is a \\"<b>string</b>\\" with <i>tags</i>""")''')
