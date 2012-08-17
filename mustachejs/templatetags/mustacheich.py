from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound

from .base import BaseMustacheNode



register = template.Library()



class MustacheICanHazNode(BaseMustacheNode):
    def generate_node_text(self, resolved_name, file_content):
        output = ('<script type="text/html" id="{0}">'.format(resolved_name)
                    + file_content + '</script>')
        return output



@register.tag
def mustacheich(parser, token):
    """
    Finds the Mustache template for the given name and renders it surrounded by
    the requisite ICanHaz <script> tags.

    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(
            "'mustacheich' tag takes either one argument: the name/id of "
            "the template, or a pattern matching a set of templates.")
    return MustacheICanHazNode(*bits[1:])
