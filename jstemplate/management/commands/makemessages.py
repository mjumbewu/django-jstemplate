"""In order to avoid having to send our project's translation mapping to the
client, we have built-in the ability to preprocess i18n tags in the mustache
templates.

There aren't any nice solutions here.  The code behind ``makemessages``
unfortunately isn't extensible, so we can:

  * Duplicate the command + code behind it.
  * Offer a separate command for Mustache tag extraction.
  * Try to get Django to offer hooks into makemessages().
  * Monkey-patch.

We are currently doing that last thing. In this case we override the templatize
method.  Templatize takes a template, extracts the translatable strings (along
with desired metadata), and generates a file that xgettext knows how to parse,
e.g. a file with Python syntax.  We override this function to find
Mustache-tagged strings if the file that we are templatizing is in one of the
paths found by the active MUSTACHEJS_FINDERS.
"""

import os
import re
import sys

from django.core.management.commands.makemessages \
    import Command as BaseI18nCommand
from django.utils.translation \
    import templatize as base_templatize

from jstemplate.loading import find, preprocess
from jstemplate.preprocessors import I18nPreprocessor


class Command (BaseI18nCommand):
    help = ('Adds the translatable strings from the js templates to the '
            'messages')

    def handle_noargs(self, *args, **options):
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
            translatable = '\n'.join(['_("""{0}""")'.format(escape(string))
                                      for string in strings])

            return translatable

    # If the file isn't in one of our paths, then delegate to the original
    # method.
    else:
        return base_templatize(src, origin)


# ============================================================================
#
# Monkey-patch django.utils.translation.templatize to use the mustachejs
# version when dealing with a file that is in a mustachejs finder directory.
# Patch it globally so that any other commands that also patch the function
# will inherit this functionality.

import django.utils.translation
django.utils.translation.templatize = templatize
