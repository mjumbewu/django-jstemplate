import os.path

from django.test import TestCase
from django.utils import translation
from jstemplate.preprocessors import I18nPreprocessor

from .utils import override_settings



__all__ = [
    "I18nTest",
]


DIR = os.path.join(os.path.dirname(__file__), "templates")


class I18nTest (TestCase):
    @override_settings(USE_I18N=True)
    def setUp(self):
        # A decorator function that just adds 'XXX ' to the front of all strings
        def wrap_with_xxx(func):
            def new_func(*args, **kwargs):
                output = func(*args, **kwargs)
                return "XXX "+output
            return new_func

        self.native_lang = translation.get_language()
        # Activate french, so that if the fr files haven't been loaded, they will be loaded now.
        translation.activate("fr")
        fake_translation = translation.trans_real._active.value

        # wrap the ugettext and ungettext functions so that 'XXX ' will prefix each translation
        self.original_ugettext = fake_translation.ugettext
        fake_translation.ugettext = wrap_with_xxx(fake_translation.ugettext)

        # Turn back on our old translations
        translation.activate(self.native_lang)

    def tearDown(self):
        # Restore the french translation function
        translation.activate("fr")
        fake_translation = translation.trans_real._active.value
        fake_translation.ugettext = self.original_ugettext

        # Turn back on our old translations
        translation.activate(self.native_lang)

    def test_no_string(self):
        res = I18nPreprocessor().process(
            '<div>{{# _ }}{{/ _ }}</div>'
        )

        self.assertEqual(res, '<div></div>')

    @override_settings(JSTEMPLATE_I18N_TAGS=['hello', 'world'])
    def test_different_tagname(self):
        res = I18nPreprocessor().process(
            '<div>{{# hello }}{{name}}{{/ hello }}</div>'
        )

        self.assertEqual(res, '<div>{{name}}</div>')

        res = I18nPreprocessor().process(
            '<div>{{# _ }}{{name}}{{/ _ }}</div>'
        )

        self.assertEqual(res, '<div>{{# _ }}{{name}}{{/ _ }}</div>')

    def test_simple_string_translation(self):
        translation.activate('fr')
        res = I18nPreprocessor().process(
            '<div>{{# _ }}Hello, {{name}}!{{/ _ }}</div>'
        )

        self.assertEqual(res, '<div>XXX Hello, {{name}}!</div>')

    def test_string_with_newlines_translation(self):
        translation.activate('fr')
        res = I18nPreprocessor().process(
            '<div>{{# _ }}Hello, \n{{name}}\n!{{/ _ }}</div>'
        )

        self.assertEqual(res, '<div>XXX Hello, \n{{name}}\n!</div>')

    def test_string_with_newlines_translation(self):
        translation.activate('fr')
        res = I18nPreprocessor().process(
            '<div>{{# _ }}Hello, \n{{name}}\n!{{/ _ }} {{# _ }}Second string{{/ _ }}</div>'
        )

        self.assertEqual(res, '<div>XXX Hello, \n{{name}}\n! XXX Second string</div>')
