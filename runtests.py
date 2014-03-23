#!/usr/bin/env python

from __future__ import unicode_literals
import os, sys

try:
    import six
    from django.conf import settings
except ImportError:
    print("Django has not been installed.")
    sys.exit(0)


if not settings.configured:
    settings.configure(
        INSTALLED_APPS=["jstemplate"],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}})


def runtests(*test_args):
    if not test_args:
        test_args = ["jstemplate"]

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner as DjangoTestSuiteRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner

    def run_tests(test_args, verbosity, interactive):
        runner = DjangoTestSuiteRunner(
            verbosity=verbosity, interactive=interactive, failfast=False)
        return runner.run_tests(test_args)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    import django
    if six.PY3 and django.VERSION < (1, 5):
        print("Django " + '.'.join([str(i) for i in django.VERSION]) +
              " is not compatible with Python 3. Skipping tests.")
        sys.exit(0)

    runtests()
