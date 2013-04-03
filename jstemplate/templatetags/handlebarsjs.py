from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper



register = template.Library()



class HandlebarsJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = ('<script type="text/x-handlebars-template" id="{0}">'.format(resolved_name)
                    + file_content + '</script>')
        return output



@register.tag
def handlebarsjs(parser, token):
    """
    Finds the Mustache template for the given name and renders it surrounded by
    the requisite ICanHaz <script> tags.

    """
    return jstemplate_tag_helper('handlebarsjs', HandlebarsJSNode,
                                 parser, token)
