from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper



register = template.Library()



class MustacheICanHazNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = ('<script type="text/html" id="{0}">'.format(resolved_name)
                    + file_content + '</script>')
        return output



@register.tag
def icanhazjs(parser, token):
    """
    Finds the Mustache template for the given name and renders it surrounded by
    the requisite ICanHaz <script> tags.

    """
    return jstemplate_tag_helper('icanhazjs', MustacheICanHazNode,
                                 parser, token)
