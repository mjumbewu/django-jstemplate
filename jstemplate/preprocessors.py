from __future__ import unicode_literals

import re
from django.utils.translation import ugettext
from .conf import conf

class I18nPreprocessor(object):
    @property
    def tagnames(self):
        return conf.JSTEMPLATE_I18N_TAGS

    @property
    def short_trans_re(self):
        # Should match strings like: {{ _ "Hello, world! }}
        tagnames = '|'.join(['(?:{0})'.format(t) for t in self.tagnames])
        
        left_side = r'''(?P<left>\{\{\s*(?P<tag>(?:''' + tagnames + r''')\s+)(?P<quote>['"]))'''
        right_side = r'''(?P<right>(?P=quote)\s*\}\})'''

        return left_side + r'(?P<msg>.*?)' + right_side

    @property
    def long_trans_re(self):
        # Should match strings like: {{# _ }}Hello, {{ name }}.{{/ _ }}
        tagnames = '|'.join(['(?:{0})'.format(t) for t in self.tagnames])
        
        start_tag = r'\{\{#\s*(?P<tag>' + tagnames + r')\s*\}\}'
        end_tag = r'\{\{\/\s*(?P=tag)\s*\}\}'

        return start_tag + r'(?P<msg>.*?)' + end_tag

    def translate_short_form(self, match):
        """Translate a result of matching the compiled trans_re pattern."""
        tag = match.group('tag')
        msg = match.group('msg')
        msg = ugettext(msg) if len(msg) > 0 else ''
        string = match.group('left').replace(tag, '', 1) + msg + match.group('right')
        return string

    def translate_long_form(self, match):
        """Translate a result of matching the compiled trans_re pattern."""
        msg = match.group('msg')
        string = ugettext(msg) if len(msg) > 0 else ''
        return string

    def process(self, content):
        # TODO: cache the compiled regex.
        # We need to compile here because re.sub doesn't accept a flags
        # argument in python < 2.7, but re.compile does.
        pattern = re.compile(self.short_trans_re)
        content = re.sub(pattern, self.translate_short_form, content)

        pattern = re.compile(self.long_trans_re, flags=re.DOTALL)
        content = re.sub(pattern, self.translate_long_form, content)

        return content
