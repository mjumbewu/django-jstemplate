from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .conf import conf



def find(name):
    for finder in finders:
        filepath = finder.find(name)
        if filepath is not None:
            return filepath

    raise MustacheJSTemplateNotFound(name)


def preprocess(content):
    for preprocessor in preprocessors:
        content = preprocessor.process(content)

    return content


def findAll(dir, regex):
    result = []
    for finder in regexfinders:
        paths = finder.findAll(dir, regex)
        if paths is not None:
            result += paths
    return result


def _get_classes(dotted_paths):
    ret = []
    for path in dotted_paths:
        modpath, cls_name = path.rsplit(".", 1)
        try:
            mod = import_module(modpath)
        except ImportError, e:
            raise ImproperlyConfigured(
                "ImportError %s: %s" % (modpath, e.args[0]))

        try:
            cls = getattr(mod, cls_name)
        except AttributeError, e:
            raise ImproperlyConfigured(
                "AttributeError %s: %s" % (cls_name, e.args[0]))

        ret.append(cls())

    return ret


def _get_finders():
    return _get_classes(conf.MUSTACHEJS_FINDERS)


def _get_regexfinders():
    return _get_classes(conf.MUSTACHEJS_REGEX_FINDERS)


def _get_preprocessors():
    return _get_classes(conf.MUSTACHEJS_PREPROCESSORS)


# Instantiate finders
finders = _get_finders()
regexfinders = _get_regexfinders()
preprocessors = _get_preprocessors()


class MustacheJSTemplateNotFound(Exception):
    pass
