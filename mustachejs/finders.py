import glob, os, sys, re

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
        matches = {}

        for directory in self.directories:
            for extension in self.extensions:
                self._update_matches(matches, name, directory, extension)

        return matches.items()

    def _update_matches(self, matches, pathspec, directory, extension):
        """
        Add names and paths corresponding to the given glob pattern (pathspec)
        to the mapping (matches).  Do not override existing matching entries.
        """

        lenext = len(extension) + 1  # The +1 is for the '.'
        lendir = len(directory)

        # Catch the ending '/', if it's not already accounted for
        if not directory.endswith(os.path.sep):
            lendir += 1

        normdir = os.path.normpath(directory)

        pathname = os.path.join(directory, pathspec + "." + extension)
        pathmatches = glob.glob(pathname)

        for filepath in pathmatches:
            # Remove the template directory name and the extension to
            # get the template name
            matchname = filepath[lendir:-lenext]

            # Add matchname => filepath to the mapping.  Do not override.
            if matchname not in matches:
                absfilepath = os.path.abspath(filepath)
                if absfilepath.startswith(normdir):
                    matches[matchname] = absfilepath


class FilesystemRegexFinder(BaseRegexFinder):
    @property
    def directories(self):
        return conf.MUSTACHEJS_DIRS

    @property
    def extensions(self):
        return conf.MUSTACHEJS_EXTS

    def findAll(self, path, regex):
        result = []

        regex = re.compile("(" + regex + ").(?:" + '|'.join(self.extensions) + ")")
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
