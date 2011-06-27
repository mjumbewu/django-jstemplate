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
    ICANHAZ_FINDERS=[
        "icanhaz.finders.FilesystemFinder",
        "icanhaz.finders.AppFinder",
        ],
    ICANHAZ_DIRS=[],
    ICANHAZ_APP_DIRNAMES=["jstemplates"],
    )
