from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



class Configuration(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs


    def __getattr__(self, k):
        try:
            return getattr(settings, k)
        except AttributeError:
            if k in self.defaults:
                return self.defaults[k]
            raise ImproperlyConfigured("%s setting is required." % k)


conf = Configuration(
    MUSTACHEJS_FINDERS=[
        "mustachejs.finders.FilesystemFinder",
        "mustachejs.finders.AppFinder",
        "mustachejs.finders.FilesystemRegexFinder",
        "mustachejs.finders.AppRegexFinder",
        ],
    MUSTACHEJS_DIRS=[],
    MUSTACHEJS_EXTS=["mustache", "html"],
    MUSTACHEJS_APP_DIRNAMES=["jstemplates"],
    MUSTACHEJS_I18N_TAGS=["_", "i18n"],
    MUSTACHEJS_PREPROCESSORS=['mustachejs.preprocessors.I18nPreprocessor'],
    )
