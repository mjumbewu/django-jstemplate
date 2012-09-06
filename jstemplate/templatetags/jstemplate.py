from django import template

from .rawjstemplate import rawjstemplate
from .mustachejs import mustachejs
from .icanhazjs import icanhazjs
from .dustjs import dustjs

register = template.Library()


register.tag(rawjstemplate)
register.tag(mustachejs)
register.tag(icanhazjs)
register.tag(dustjs)
