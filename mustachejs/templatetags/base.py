from django import template

from ..conf import conf
from ..loading import find, findAll, preprocess, MustacheJSTemplateNotFound


register = template.Library()


class BaseMustacheNode(template.Node):
    preprocessors = conf.MUSTACHEJS_PREPROCESSORS

    def __init__(self, name_or_path, pattern=None):
        if pattern is None:
            self.name = template.Variable(name_or_path)
        else:
            self.path = template.Variable(name_or_path)
            self.pattern = template.Variable(pattern)

    def find_template_file(self, path):
        return find(path)

    def preprocess(self, content):
        return preprocess(content)

    def render(self, context):
        # If this is a path and a patter, loop through and render all the files
        # that match the pattern.
        if hasattr(self, 'pattern'):
            resolved_path = self.path.resolve(context)
            pattern = self.pattern.resolve(context)
            pairs = findAll(resolved_path, pattern)
            return ''.join([self.render_file(context, name, filepath)
                            for (name, filepath) in pairs])

        # If this is just a file name, render that file.
        else:
            name = self.name.resolve(context)
            return self.render_file(context, name)

    def render_file(self, context, resolved_name, filepath=None):
        try:
            if filepath is None:
                filepath = self.find_template_file(resolved_name)
            content = self.read_template_file_contents(filepath)
            content = self.preprocess(content)
            output = self.generate_node_text(resolved_name, content)

        except (IOError, MustacheJSTemplateNotFound):
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
