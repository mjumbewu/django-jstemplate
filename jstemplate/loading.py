from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .conf import conf



def find(name):
    all_matches = {}

    for finder in finders:
        matches = finder.find(name)

        # <finder>.find may return a single string.  The name of the template
        # will then be the name given to 'find'
        if isinstance(matches, basestring):
            filepath = matches
            if name not in all_matches:
                all_matches[name] = filepath

        # None valus should be ignored
        elif matches is None:
            continue

        # Otherwise, matches should be a list of (name, filepath) pairs
        else:
            for matchname, filepath in matches:
                if matchname not in all_matches:
                    all_matches[matchname] = filepath

    if len(all_matches) == 0:
        raise JSTemplateNotFound(name)

    return all_matches.items()


def preprocess(content):
    for preprocessor in preprocessors:
        content = preprocessor.process(content)

    return content


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
    return _get_classes(conf.JSTEMPLATE_FINDERS)


def _get_preprocessors():
    return _get_classes(conf.JSTEMPLATE_PREPROCESSORS)


# Instantiate finders
finders = _get_finders()
preprocessors = _get_preprocessors()


class JSTemplateNotFound(Exception):
    pass
