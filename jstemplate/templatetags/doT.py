from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper

register = template.Library()


class DoTJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        return (
            '<script type="text/x-dot-template" id="{0}">'.format(resolved_name) +
            file_content +
            '</script>'
        )


@register.tag
def doTjs(parser, token):
    """
    Finds the DoTJS template for the given name and renders it surrounded by
    the requisite DoTJS <script> tags.
    """
    return jstemplate_tag_helper(
        'doTjs', DoTJSNode, parser, token
    )
