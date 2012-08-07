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
            "'mustacheraw' tag takes either (1) one argument: the name/id of "
            "the template, or (2)  two arguments: the name of a subdirectory "
            "to search and a regular expression of files to search for")
    return MustacheRaw(*bits[1:])
