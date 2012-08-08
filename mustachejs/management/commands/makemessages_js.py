import os
import re
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import get_text_list
from django.utils.translation import templatize as orig_templatize

from mustachejs.loading import find, findAll, preprocess, MustacheJSTemplateNotFound
from mustachejs.preprocessors import I18nPreprocessor

class Command(BaseCommand):
    help = 'Adds the translatable strings from the js templates to the messages'

    def handle(self, *args, **options):
        import django.utils.translation
        django.utils.translation.templatize = templatize
        call_command('makemessages', *args, **options)


def templatize(src, origin=None):
    # Load all the js template files
    paths = [os.path.abspath(path) for name, path in findAll('', '.*')]

    if os.path.abspath(src) in paths:
        with open(src) as template_file:
            # Pick out all the internationalized strings
            content = template_file.read()
            processor = I18nPreprocessor()
            strings = set(re.findall(processor.trans_re, content))
            translatable = '\n'.join(['_(r"{0}")'.format(
                string.replace('"', r'\"') for string in strings
            )])
            return translatable

    else:
        return orig_templatize(src, origin)
