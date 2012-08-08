import os
import re
import sys

from django.core.management.commands.makemessages import Command as I18nCommand
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import get_text_list
from django.utils.translation import templatize as orig_templatize

from mustachejs.loading import find, findAll, preprocess, MustacheJSTemplateNotFound
from mustachejs.preprocessors import I18nPreprocessor

class Command (I18nCommand):
    help = 'Adds the translatable strings from the js templates to the messages'

    def handle_noargs(self, *args, **options):
        # Monkey-patch django.utils.translation.templatize to use the
        # mustachejs version when dealing with a file that is in a mustachejs
        # finder directory.
        import django.utils.translation
        django.utils.translation.templatize = templatize

        return super(Command, self).handle_noargs(*args, **options)


def templatize(src, origin=None):
    # Get all the paths that we know about
    paths = [os.path.abspath(path) for name, path in findAll('', '.*')]

    # Hijack the process if the file we're talking about is in one of the
    # finder paths.
    if origin and os.path.abspath(origin) in paths:
        with open(origin) as template_file:

            # Load the template content.
            content = template_file.read()

            # Find all the translatable strings.
            processor = I18nPreprocessor()
            strings = set(re.findall(processor.trans_re, content))

            # Build a string that looks like a Python file that's ready to be
            # translated.
            translatable = '\n'.join(['_(r"{0}")'.format(
                string.replace('"', r'\"')) for string in strings
            ])

            return translatable

    # If the file isn't in one of our paths, then delegate to the original
    # method.
    else:
        return orig_templatize(src, origin)
