from django import template
from ..conf import conf
from .base import BaseJSTemplateNode, jstemplate_tag_helper



register = template.Library()



class HandlebarsJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = (
            u'<script type="text/x-handlebars-template" id="{name}">'
                u'{content}'
            u'</script>'
        )

        # If there are additional arguments, process the template further
        if self.args:
            output += (
                u'<script>'
                    u'(function(H) {{'
                        u'var source = $("#{name}").html();'
            )

            if 'register_partials' in self.args:
                output += u'H.registerPartial("{name}", source);'

            if 'precompile' in self.args:
                output += (u'H.templates = H.templates || {{}};'
                           u'H.templates["{name}"] = H.compile(source);')

            output += (
                    u'}})(Handlebars);'
                u'</script>'
            )

        return output.format(name=resolved_name, content=file_content)



@register.tag
def handlebarsjs(parser, token):
    """
    Finds the Handlebars template for the given name and renders it surrounded
    by the requisite Handlebars <script> tags.

    We don't use the jstemplate_tag_helper here, since we can take an 
    additional parameter denoting whether to register partials inline.

    """
    return jstemplate_tag_helper('handlebarsjs', HandlebarsJSNode,
                                 parser, token)
