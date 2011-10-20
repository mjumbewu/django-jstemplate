from django import template

from ..conf import conf
from ..loading import find, ICanHazTemplateNotFound



register = template.Library()



class ICanHazNode(template.Node):
    def __init__(self, name, classes="''"):
        self.name = template.Variable(name)
        self.classes = template.Variable(classes)


    def render(self, context):
        name = self.name.resolve(context)
        classes = self.classes.resolve(context)

        try:
            filepath = find(name)
            fp = open(filepath, "r")
            output = fp.read()
            fp.close()
            output = ('<script id="%s" class="%s" type="text/html">\n'
                      % (name, classes)) + output + "\n</script>\n"
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

@register.tag
def icanhaz_partial(parser, token):
    """
    Finds the ICanHaz template partial for the given name and renders it
    surrounded by the requisite ICanHaz <script> tags.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'icanhaz_partial' tag takes one argument: the name/id of the template")
    return ICanHazNode(bits[1], "'partial'")
