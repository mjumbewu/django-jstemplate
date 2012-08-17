from django import template

from ..conf import conf
from ..loading import find, preprocess, MustacheJSTemplateNotFound


register = template.Library()


class BaseMustacheNode(template.Node):
    preprocessors = conf.MUSTACHEJS_PREPROCESSORS

    def __init__(self, name):
        self.name = template.Variable(name)

    def find_template_matches(self, name):
        return find(name)

    def preprocess(self, content):
        return preprocess(content)

    def render(self, context):
        name = self.name.resolve(context)

        try:
            matches = self.find_template_matches(name)
        except MustacheJSTemplateNotFound:
            if conf.DEBUG: raise
            else: return ''
        else:
            return ''.join([self.render_file(context, matchname, filepath)
                            for (matchname, filepath) in matches])

    def render_file(self, context, resolved_name, filepath):
        try:
            content = self.read_template_file_contents(filepath)
            content = self.preprocess(content)
            output = self.generate_node_text(resolved_name, content)

        except IOError:
            output = ""
            if conf.DEBUG:
                raise

        return output

    def read_template_file_contents(self, filepath):
        with open(filepath, "r") as fp:
            template_text = fp.read().decode(conf.FILE_CHARSET)
            template_text = self.preprocess(template_text)
            return template_text

    def generate_node_text(self, resolved_name, file_content):
        raise NotImplementedError()
