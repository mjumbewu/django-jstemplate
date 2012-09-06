from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper



register = template.Library()



class RawJSTemplateNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        return file_content



@register.tag
def rawjstemplate(parser, token):
    """
    Prints out raw mustache content

    """
    return jstemplate_tag_helper('rawjstemplate', RawJSTemplateNode,
                                 parser, token)
