from __future__ import unicode_literals
from django import template
from ..conf import conf
from .base import BaseJSTemplateNode, jstemplate_tag_helper



register = template.Library()



class HandlebarsJSNode(BaseJSTemplateNode):
    def generate_node_text(self, resolved_name, file_content):
        output = (
            '<script type="text/x-handlebars-template" id="{name}">'
                '{content}'
            '</script>'
        )

        # If there are additional arguments, process the template further
        if self.args:
            output += (
                '<script>'
                    '(function(H) {{'
                        'var source = $("#{name}").html();'
            )

            if 'register_partials' in self.args:
                output += 'H.registerPartial("{name}", source);'

            if 'precompile' in self.args:
                output += ('H.templates = H.templates || {{}};'
                           'H.templates["{name}"] = H.compile(source);')

            output += (
                    '}})(Handlebars);'
                '</script>'
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
