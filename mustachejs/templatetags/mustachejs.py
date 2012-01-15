from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound



register = template.Library()



class MustacheJSNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        name = self.name.resolve(context)

        try:
            filepath = find(name)

            with open(filepath, "r") as fp:
                output = fp.read().decode(conf.FILE_CHARSET)

            output = output.replace('\\', r'\\')
            output = output.replace('\n', r'\n')
            output = output.replace("'", r"\'")

            output = ("<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
                      + "Mustache.TEMPLATES['{0}']='".format(name)
                      + output + "';</script>")
        except (IOError, MustacheJSTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output



@register.tag
def mustachejs(parser, token):
    """
    Finds the MustacheJS template for the given name and renders it surrounded by
    the requisite MustacheJS <script> tags.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'mustachejs' tag takes one argument: the name/id of the template")
    return MustacheJSNode(bits[1])
