from django import template
from .base import BaseJSTemplateNode, jstemplate_tag_helper


register = template.Library()


class DustJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = file_content
        output = output.replace('\\', r'\\')
        output = output.replace('\n', r'\n')
        output = output.replace("'", r"\'")

        output = (
            '<script type="text/javascript">'
            "if (typeof(dust) !== 'undefined') {"
                "compiled = dust.compile('%s', '%s');"
                "dust.loadSource(compiled);"
            "}"
            '</script>'
        ) % (output, format(resolved_name))
        return output

@register.tag
def dustjs(parser, token):
    """
    Finds the DustJS template for the given name and compiles.

    """
    return jstemplate_tag_helper('dustjs', DustJSNode,
                                 parser, token)
