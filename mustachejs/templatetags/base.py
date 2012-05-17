from django import template

from ..conf import conf
from ..loading import find, preprocess, MustacheJSTemplateNotFound


register = template.Library()


class BaseMustacheNode(template.Node):
    preprocessors = conf.MUSTACHEJS_PREPROCESSORS

    def __init__(self, name):
        self.name = template.Variable(name)

    def find_template_file(self, name):
        return find(name)

    def preprocess(self, content):
        return preprocess(content)

    def render(self, context):
        resolved_name = self.name.resolve(context)

        try:
            filepath = self.find_template_file(resolved_name)
            content = self.read_template_file_contents(filepath)
            content = self.preprocess(content)
            output = self.generate_node_text(resolved_name, content)

        except (IOError, MustacheJSTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output

    def read_template_file_contents(self, filepath):
        with open(filepath, "r") as fp:
            template_text = fp.read().decode(conf.FILE_CHARSET)
            template_text = self.preprocess(template_text)
            return template_text

    def generate_node_text(self, resolved_name, file_content):
        raise NotImplementedError()


class BaseMustacheRegexNode(template.Node):
    def __init__(self, dir, regex):
        self.dir = template.Variable(dir)
        self.regex = template.Variable(regex)


    def render(self, context):
        dir = self.dir.resolve(context)
        regex = self.regex.resolve(context)

        pairs = findAll(dir, regex)
        result = ""

        for (name, filepath) in pairs:
            try:
                fp = open(filepath, "r")
                output = fp.read().decode(conf.FILE_CHARSET)
                fp.close()
                result += ('<script id="%s" type="text/html">\n'
                           % name) + output + "\n</script>\n"
            except IOError:
                if conf.DEBUG:
                    raise

        return result



@register.tag
def mustacheraw(parser, token):
    """
    Prints out raw mustache content

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError(
            "'mustacheraw' tag takes one argument: the name/id of the template")
    return MustacheRaw(bits[1])
