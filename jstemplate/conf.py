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
    JSTEMPLATE_FINDERS=[
        "jstemplate.finders.FilesystemFinder",
        "jstemplate.finders.AppFinder",
        "jstemplate.finders.FilesystemRegexFinder",
        "jstemplate.finders.AppRegexFinder",
        ],
    JSTEMPLATE_DIRS=[],
    JSTEMPLATE_EXTS=["mustache", "html"],
    JSTEMPLATE_APP_DIRNAMES=["jstemplates"],
    JSTEMPLATE_I18N_TAGS=["_", "i18n"],
    JSTEMPLATE_PREPROCESSORS=['jstemplate.preprocessors.I18nPreprocessor'],
    )
