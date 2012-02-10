from django import template

from ..conf import conf
from ..loading import find, MustacheJSTemplateNotFound

from .base import BaseMustacheNode
from .mustacheraw import mustacheraw
from .mustacheich import mustacheich


register = template.Library()

register.tag(mustacheraw)
register.tag(mustacheich)



class DustJSNode(BaseMustacheNode):
    def generate_node_text(self, resolved_name, file_content):
        output = file_content
        output = output.replace('\\', r'\\')
        output = output.replace('\n', r'\n')
        output = output.replace("'", r"\'")

        output = """
        <script type="text/javascript">
        if (typeof(dust) !== 'undefined') {
            compiled = dust.compile('%s', '%s')
            dust.loadSource(compiled)
        }
        </script>
        """ % (output, format(resolved_name))
        return output

@register.tag
def dustjs(parser, token):
    """
    Finds the DustJS template for the given name and compiles.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'dustjs' tag takes one argument: the name/id of the template")
    return DustJSNode(bits[1])

