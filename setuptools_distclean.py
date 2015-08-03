"""
A plugin for setuptools to delete all build products - especially useful
for binary extensions,
"""
from __future__ import absolute_import

__version__ = '0.1'
__author__ = 'Gabi Davar'
__all__ = ['DistCleanCommand']


import os
from os.path import abspath, join, normcase, relpath

import fnmatch
import setuptools
from six import print_
from distutils.dir_util import remove_tree
from distutils.util import strtobool
from distutils import log
from itertools import chain


def locate(pattern, root_path):
    root = abspath(root_path)

    for path, dirs, files in os.walk(root):
        parent = relpath(path, root)

        candidates = fnmatch.filter(dirs + files, pattern)
        for filename in candidates:
            yield join(path, filename)
        if not candidates:
            local_paths = [join(parent, p) for p in (dirs + files)]
            for path in fnmatch.filter(local_paths, pattern):
                yield path


class DistCleanCommand(setuptools.Command):
    description = "cleans up all build files, inline or otherwise"

    # dirs
    produce_dir = [
        'dist',
        'build',
        '__pycache__',
        '.tox',
        '.cache',
        '*.egg-info',
        '*.py[cod]',
        '*.pdb',
    ]

    user_options = [
        ('clean-exclude-paths=', 'x',
            'List of comma delimited paths to exclude from delete'),
        ('clean-include-paths=', 'i',
            'List of comma delimited paths to delete. :default:'),
        ('dry-run', 'n',
            "Don't do anything just print"),
    ]

    def initialize_options(self):
        self.clean_exclude_paths = None
        self.clean_include_paths = ':default:'
        self.dry_run = False

    def finalize_options(self):
        self.excluded_paths = [abspath('.git')]
        if self.clean_exclude_paths:
            self.excluded_paths += \
                map(abspath, self.clean_exclude_paths.split(','))

        include_paths = self.clean_include_paths.split(',')
        try:
            i = include_paths.index(':default:')
            include_paths[i:i] = self.produce_dir
            include_paths.remove(':default:')
        except ValueError:
            pass

        #self.included_paths = map(abspath, include_paths)
        self.included_paths = include_paths

    def run(self):
        #log.info("include_paths:\n%s", '\n'.join(self.included_paths))
        dirs = []
        for pat in self.included_paths:
            dirs += locate(normcase(pat), '.')

        if self.distribution.clean_exclude_paths:
            self.excluded_paths += map(abspath, self.distribution.clean_exclude_paths)

        dirs.sort(reverse=True)
        filtered_dirs = []

        while dirs:
            x = dirs.pop()
            if x not in self.excluded_paths:
                for exclude in self.excluded_paths:
                    if x.startswith(exclude):
                        break
                else:
                    filtered_dirs.append(x)

            # don't delete subdirectories of things we already deleted
            dirs = [d for d in dirs if not d.startswith(x)]

        log.info("removing:\n%s", '\n'.join(filtered_dirs))
        if not self.dry_run:
            for p in filtered_dirs:
                if os.path.isdir(p):
                    remove_tree(p)
                else:
                    os.remove(p)
        else:
            log.info("Dry Run!")


def clean_exclude_paths(dist, attr, value):
    pass

if __name__ == "__main__":
    print_('called!')
