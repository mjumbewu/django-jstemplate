import os, sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .conf import conf



class BaseFinder(object):
    def find(self, name):
        raise NotImplementedError()



class FilesystemFinder(BaseFinder):
    @property
    def directories(self):
        return conf.ICANHAZ_DIRS


    def find(self, name):
        for directory in self.directories:
            filepath = os.path.abspath(os.path.join(
                directory,
                name + ".html"))

            if filepath.startswith(os.path.normpath(directory)) and os.path.exists(filepath):
                return filepath

        return None



def _get_app_template_dirs():
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    ret = []
    for app in conf.INSTALLED_APPS:
        try:
            mod = import_module(app)
        except ImportError, e:
            raise ImproperlyConfigured("ImportError %s: %s" % (app, e.args[0]))
        app_dir = os.path.dirname(mod.__file__)
        for dirname in conf.ICANHAZ_APP_DIRNAMES:
            template_dir = os.path.join(app_dir, dirname)
            if os.path.isdir(template_dir):
                ret.append(template_dir.decode(fs_encoding))
    return ret



# At import time, cache the app directories to search.
app_template_dirs = _get_app_template_dirs()



class AppFinder(FilesystemFinder):
    @property
    def directories(self):
        return app_template_dirs
