import os.path

from django.test import override_settings, TestCase

from jstemplate.management.commands import makemessages

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project", "project", "jstemplates")

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
_("""this is a \\"<b>string</b>\\" with <i>tags</i>""")
_("""this is a {{ string }} {{# with }} variables {{/ with }}""")''')
