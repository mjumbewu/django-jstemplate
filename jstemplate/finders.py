import glob
import os
import re
import sys
import warnings
from importlib import import_module

from .conf import conf


class BaseFinder(object):
    def find(self, name):
        raise NotImplementedError()


class FilesystemFinder(BaseFinder):
    @property
    def directories(self):
        return conf.JSTEMPLATE_DIRS

    @property
    def extensions(self):
        return conf.JSTEMPLATE_EXTS

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


class FilesystemRegexFinder(BaseFinder):
    @property
    def directories(self):
        return conf.JSTEMPLATE_DIRS

    @property
    def extensions(self):
        return conf.JSTEMPLATE_EXTS

    def find(self, name):
        matches = {}

        try:
            pattern = re.compile(name + ".(?:" + '|'.join(self.extensions) + ")$")
        except re.error:
            return []

        # Bail if there are no capturing groups in the pattern
        if pattern.groups == 0:
            return []

        for directory in self.directories:
            self._update_matches(matches, directory, pattern)

        return matches.items()

    def _update_matches(self, matches, directory, pattern):
        # Walk recursively under directory and search for matches
        for root, dirs, files in os.walk(directory):
            # Build relative path to current directory, omit .
            relative_root = os.path.relpath(root, directory).replace('.', '', 1)
            for filename in files:
                # Build relative path to file
                relative_filepath = os.path.join(relative_root, filename)
                match = pattern.match(relative_filepath)
                if match is not None and match.group(1) not in matches:
                    matches[match.group(1)] = os.path.join(directory, relative_filepath)


def _get_app_template_dirs():
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    ret = []
    for app in conf.INSTALLED_APPS:
        try:
            mod = import_module(app)
        except ImportError:
            warnings.warn('Installed app %s is not an importable Python module and will be ignored' % app)
            continue
        app_dir = os.path.dirname(os.path.abspath(mod.__file__))
        for dirname in conf.JSTEMPLATE_APP_DIRNAMES:
            template_dir = os.path.join(app_dir, dirname)
            if os.path.isdir(template_dir):
                ret.append(template_dir)
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
