from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound



register = template.Library()



class MustacheRaw(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        name = self.name.resolve(context)

        try:
            filepath = find(name)

            with open(filepath, "r") as fp:
                output = fp.read().decode(conf.FILE_CHARSET)

        except (IOError, MustacheJSTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output



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
