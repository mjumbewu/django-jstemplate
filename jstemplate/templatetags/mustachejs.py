from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper

register = template.Library()


class MustacheJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = file_content
        output = output.replace('\\', r'\\')
        output = output.replace('\n', r'\n')
        output = output.replace("'", r"\'")

        output = ("<script>Mustache.TEMPLATES=Mustache.TEMPLATES||{};"
                    + "Mustache.TEMPLATES['{0}']='".format(resolved_name)
                    + output + "';</script>")

        return output



@register.tag
def mustachejs(parser, token):
    """
    Finds the MustacheJS template for the given name and renders it surrounded by
    the requisite MustacheJS <script> tags.

    """
    return jstemplate_tag_helper('mustachejs', MustacheJSNode,
                                 parser, token)
