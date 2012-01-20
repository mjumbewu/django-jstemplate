from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound

from mustacheraw import MustacheRaw


register = template.Library()



class MustacheJSNode(MustacheRaw):
    def render(self, context):
        name = self.name.resolve(context)

        output = MustacheRaw.render(self, context)
        output = output.replace('\\', r'\\')
        output = output.replace('\n', r'\n')
        output = output.replace("'", r"\'")
        
        output = ("<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
                    + "Mustache.TEMPLATES['{0}']='".format(name)
                    + output + "';</script>")

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
