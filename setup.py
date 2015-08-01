import codecs
from os import path
from setuptools import setup

try:
    unicode
except NameError:
    unicode = str


def read(name):
    full_path = path.join(path.abspath(path.dirname(__file__)), name)
    return unicode(codecs.open(full_path).read())

setup(
    name="setuptools_distclean",
    version="0.1",
    author="Gabi Davar",
    author_email="grizzly.nyo@gmail.com",
    url="http://bitbucket.org/jezdez/setuptools_hg/",
    description="Setuptools/distribute plugin for cleaning all built files",
    long_description=read("README.rst")+read('CHANGES.txt'),
    license="BSD",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License)",
        "Topic :: Software Development :: Version Control",
        "Framework :: Setuptools Plugin",
    ],
    py_modules=["setuptools_distclean"],
    install_requires=['six'],
    entry_points={
        'distutils.commands': [
            'distclean = setuptools_distclean:DistCleanCommand'
        ],
        "distutils.setup_keywords": [
            "clean_exclude_paths = setuptools_distclean:clean_exclude_paths",
            "clean_include_paths = setuptools_distclean:include_exclude_paths",
        ]

    }
)
