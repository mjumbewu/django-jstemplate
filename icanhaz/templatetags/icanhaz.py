import os.path

from django import template
from django.core.exceptions import SuspiciousOperation

from ..conf import conf



register = template.Library()



class ICanHazNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


class ICanHazNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        name = self.name.resolve(context)

        filepath = os.path.abspath(os.path.join(
            conf.ICANHAZ_DIR,
            name + ".html"))

        if not filepath.startswith(conf.ICANHAZ_DIR):
            raise SuspiciousOperation(
                "icanhaz tag attempting to open file at %r, outside of %r"
                % (filepath, conf.ICANHAZ_DIR))

        try:
            fp = open(filepath, "r")
            output = fp.read()
            fp.close()
            output = ('<script id="%s" type="text/html">\n'
                      % name) + output + "\n</script>\n"
        except IOError:
            output = ""
            if conf.DEBUG:
                raise

        return output



@register.tag
def icanhaz(parser, token):
    """
    Outputs the contents of a given file, path relative to ICANHAZ_DIR
    setting, into the page.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'icanhaz' tag takes one argument: the name/id of the template")
    return ICanHazNode(bits[1])
