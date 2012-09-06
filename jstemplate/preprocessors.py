import re
from django.utils.translation import ugettext
from .conf import conf

class I18nPreprocessor(object):
    @property
    def tagnames(self):
        return conf.JSTEMPLATE_I18N_TAGS

    @property
    def trans_re(self):
        # Should match strings like: {{# _ }}Hello, {{ name }}.{{/ _ }}
        tagnames = '|'.join(['(?:{0})'.format(t) for t in self.tagnames])
        start_tag = r'\{\{#\s*(?:' + tagnames + r')\s*\}\}'
        end_tag = r'\{\{\/\s*(?:' + tagnames + r')\s*\}\}'

        return start_tag + '(.*?)' + end_tag

    def translate(self, match):
        """Translate a result of matching the compiled trans_re pattern."""
        string = match.group(1)
        return ugettext(string) if len(string) > 0 else u''

    def process(self, content):
        # TODO: cache the compiled regex.
        # We need to compile here because re.sub doesn't accept a flags
        # argument in python < 2.7, but re.compile does.
        pattern = re.compile(self.trans_re, flags=re.DOTALL)
        return re.sub(pattern, self.translate, content)
