"""
A plugin for setuptools to delete all build products - especially useful
for binary extensions,
"""
__version__ = '0.1'
__author__ = 'Gabi Davar'
__all__ = ['DistCleanCommand']

import os
from os.path import abspath, join
import fnmatch
import setuptools
from six import print_ as p
from distutils.dir_util import remove_tree
from distutils import log


def locate(pattern, root_path):
    for path, dirs, files in os.walk(path.abspath(root_path)):
        for filename in fnmatch.filter(dirs + files, pattern):
            yield join(path, filename)


class DistCleanCommand(setuptools.Command):
    description = "cleans up all build files, inline or otherwise"
    produce_pat = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.pdb',
    ]

    # dirs
    produce_dir = [
        'dist',
        'build',
        '__pycache__',
        '.tox',
        '.cache',
        '*.egg-info',
    ]

    user_options = [
        ('clean-exclude-paths=', 'x',
            'List of comma delimited paths to exclude from delete'),
        ('clean-include-paths=', 'i',
            'List of additional comma delimited paths to delete'),
    ]

    def initialize_options(self):
        self.clean_exclude_paths = None
        self.clean_include_paths = None

    def finalize_options(self):
        self.excluded_paths = [abspath('.git')]
        if self.clean_exclude_paths:
            self.excluded_paths += \
                map(abspath, self.clean_exclude_paths.split(','))

    def run(self):
        dirs = []
        for pat in self.produce_dir:
            dirs += locate(pat, '.')

        if self.distribution.clean_exclude_paths:
            self.excluded_paths += map(abspath, self.distribution.clean_exclude_paths)

        dirs.sort()
        filtered_dirs = []

        while dirs:
            x = dirs.pop(0)
            if x not in self.excluded_paths:
                for exclude in self.excluded_paths:
                    if x.startswith(exclude):
                        dirs = [d for d in dirs if not d.startswith(x)]
                        break
                else:
                    filtered_dirs.append(x)
                dirs = [d for d in dirs if not d.startswith(x)]
            else:
                dirs = [d for d in dirs if not d.startswith(x)]

        for d in filtered_dirs:
            remove_tree(d)

        paths = []
        for pat in self.produce_pat:
            paths += locate(pat, '.')

        if paths:
            log.info("removing:\n%s", '\n'.join(paths))
            map(os.remove, paths)


def clean_exclude_paths(dist, attr, value):
    pass

if __name__ == "__main__":
    p('called!')
