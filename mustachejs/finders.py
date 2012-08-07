import os, sys, re

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .conf import conf



class BaseFinder(object):
    def find(self, name):
        raise NotImplementedError()



class BaseRegexFinder(object):
    # Returns a list of (name, filepath) pairs
    # from the given dir matching the given regex
    def findAll(self, dir, regex):
        raise NotImplementedError()




class FilesystemFinder(BaseFinder):
    @property
    def directories(self):
        return conf.MUSTACHEJS_DIRS

    @property
    def extensions(self):
        return conf.MUSTACHEJS_EXTS


    def find(self, name):
        for directory in self.directories:
            for extension in self.extensions:
                filepath = os.path.abspath(os.path.join(
                    directory,
                    name + "." + extension))

                if filepath.startswith(os.path.normpath(directory)) and os.path.exists(filepath):
                    return filepath

        return None



class FilesystemRegexFinder(BaseRegexFinder):
    @property
    def directories(self):
        return conf.MUSTACHEJS_DIRS


    def findAll(self, path, regex):
        result = []

        regex = re.compile("(" + regex + ").html")
        for directory in self.directories:
            dirpath = os.path.abspath(os.path.join(directory, path))
            for file in os.listdir(dirpath):
                if not os.path.isdir(file):
                    match = regex.match(file)
                    if match is not None:
                        result += [(match.groups()[0], os.path.join(dirpath, file))]

        return result



# Convenience subclass to add directory scope to
# the names of the files
class ScopedFilesystemRegexFinder(FilesystemRegexFinder):
    def findAll(self, dir, regex):
        res = super(ScopedFilesystemRegexFinder, self).findAll(dir, regex)
        dir = str(os.path.join(dir))
        scope_list = [x for x in dir.split("/") if x is not "." and len(x) > 0]
        return [("_".join(scope_list + [name]), dir) for (name, dir) in res]



def _get_app_template_dirs():
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    ret = []
    for app in conf.INSTALLED_APPS:
        try:
            mod = import_module(app)
        except ImportError, e:
            raise ImproperlyConfigured("ImportError %s: %s" % (app, e.args[0]))
        app_dir = os.path.dirname(mod.__file__)
        for dirname in conf.MUSTACHEJS_APP_DIRNAMES:
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



class AppRegexFinder(FilesystemRegexFinder):
    @property
    def directories(self):
        return app_template_dirs



class ScopedAppRegexFinder(ScopedFilesystemRegexFinder):
    @property
    def directories(self):
        return app_template_dirs
