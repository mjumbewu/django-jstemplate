from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound



register = template.Library()



class BaseMustacheNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        resolved_name = self.name.resolve(context)

        try:
            filepath = find(resolved_name)
            content = self.read_template_file_contents(filepath)
            output = self.generate_node_text(resolved_name, content)

        except (IOError, MustacheJSTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output

    def read_template_file_contents(self, filepath):
        with open(filepath, "r") as fp:
            return fp.read().decode(conf.FILE_CHARSET)

    def generate_node_text(self, resolved_name, file_content):
        raise NotImplementedError()


@register.tag
def mustacheraw(parser, token):
    """
    Prints out raw mustache content

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'mustacheraw' tag takes one argument: the name/id of the template")
    return MustacheRaw(bits[1])
