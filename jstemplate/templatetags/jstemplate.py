from django import template

from .rawjstemplate import rawjstemplate
from .handlebarsjs import handlebarsjs
from .mustachejs import mustachejs
from .icanhazjs import icanhazjs
from .dustjs import dustjs
from .ractivejs import ractivejs

register = template.Library()


register.tag(rawjstemplate)
register.tag(handlebarsjs)
register.tag(mustachejs)
register.tag(icanhazjs)
register.tag(dustjs)
register.tag(ractivejs)
