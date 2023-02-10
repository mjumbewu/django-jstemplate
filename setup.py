from os.path import join, dirname, abspath

from setuptools import setup, find_packages

here = dirname(abspath(__file__))

long_description = (open(join(here, "README.rst")).read() + "\n\n" +
                    open(join(here, "CHANGES.rst")).read() + "\n\n" +
                    open(join(here, "TODO.rst")).read())

def get_version():
    fh = open(join(here, "jstemplate", "__init__.py"))
    try:
        for line in fh.readlines():
            if line.startswith("__version__ ="):
                return line.split("=")[1].strip().strip('"')
    finally:
        fh.close()

setup(
    name="django-jstemplate",
    version=get_version(),
    description="A Django template tag for embedding Mustache.js templates -- or other JavaScript templates -- safely.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Mjumbe Wawatu Ukweli",
    author_email="mjumbewu@gmail.com",
    url="https://github.com/mjumbewu/django-jstemplate/",
    packages=find_packages(),
    package_data={'jstemplate': ['static/libs/*.js']},
    install_requires=[
        'Django >= 2.2',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
    ],
    zip_safe=False,
    tests_require=["Django>=2.2", "coverage"],
    test_suite="runtests.runtests"
)
