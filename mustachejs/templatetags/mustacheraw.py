from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound

from .base import BaseMustacheNode



register = template.Library()



class MustacheRaw(BaseMustacheNode):
    def generate_node_text(self, resolved_name, file_content):
        return file_content



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
