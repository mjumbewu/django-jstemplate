from django import template

from ..conf import conf
from ..loading import find, ICanHazTemplateNotFound



register = template.Library()



class ICanHazNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        name = self.name.resolve(context)

        try:
            filepath = find(name)
            fp = open(filepath, "r")
            output = fp.read()
            fp.close()
            output = ('<script id="%s" type="text/html">\n'
                      % name) + output + "\n</script>\n"
        except (IOError, ICanHazTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output



@register.tag
def icanhaz(parser, token):
    """
    Finds the ICanHaz template for the given name and renders it surrounded by
    the requisite ICanHaz <script> tags.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'icanhaz' tag takes one argument: the name/id of the template")
    return ICanHazNode(bits[1])
