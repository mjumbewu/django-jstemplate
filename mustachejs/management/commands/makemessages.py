"""In order to avoid having to send our project's translation mapping to the
client, we have built-in the ability to preprocess i18n tags in the mustache
templates.

There aren't any nice solutions here.  The code behind ``makemessages``
unfortunately isn't extensible, so we can:

  * Duplicate the command + code behind it.
  * Offer a separate command for Mustache tag extraction.
  * Try to get Django to offer hooks into makemessages().
  * Monkey-patch.

We are currently doing that last thing. It turns out there we are lucky
for once: It's simply a matter of extending two regular expressions.
Credit for the approach goes to:
http://stackoverflow.com/questions/2090717/getting-translation-strings-for-jinja2-templates-integrated-with-django-1-x
"""

import os
import re
import sys

from django.core.management.commands.makemessages import Command as I18nCommand
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import get_text_list
from django.utils.translation import templatize as orig_templatize

from mustachejs.loading import find, preprocess, MustacheJSTemplateNotFound
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
    paths = [os.path.abspath(path) for name, path in find('(.*)')]

    # Hijack the process if the file we're talking about is in one of the
    # finder paths.
    if origin and os.path.abspath(origin) in paths:
        with open(origin) as template_file:

            # Load the template content.
            content = template_file.read()

            # Find all the translatable strings.
            processor = I18nPreprocessor()
            pattern = re.compile(processor.trans_re, flags=re.DOTALL)
            strings = set(re.findall(pattern, content))

            def escape(s):
                s = s.replace('\\', '\\\\')
                s = s.replace('"', r'\"')
                return s

            # Build a string that looks like a Python file that's ready to be
            # translated.
            translatable = '\n'.join(['_("""{0}""")'.format(escape(string)) for string in strings
            ])

            return translatable

    # If the file isn't in one of our paths, then delegate to the original
    # method.
    else:
        return orig_templatize(src, origin)
