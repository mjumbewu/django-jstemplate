from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper

register = template.Library()


class RactiveJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        mapping = (
            ('\\', r'\\'),
            ('\n', r'\n'),
            ("'", r"\'"),
        )
        output = file_content
        for pair in mapping:
            output = output.replace(*pair)
        return (
            u"<script>Ractive.TEMPLATES=Ractive.TEMPLATES||{{}};"
            u"Ractive.TEMPLATES['{0}']=Ractive.parse('{1}');</script>"
        ).format(resolved_name, output)


@register.tag
def ractivejs(parser, token):
    """
    Finds the RactiveJS template for the given name and renders it surrounded
    by the requisite RactiveJS <script> tags.

    """
    return jstemplate_tag_helper('ractivejs', RactiveJSNode,
                                 parser, token)
