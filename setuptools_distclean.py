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
from distutils.util import strtobool
from distutils import log


def locate(pattern, root_path):
    for path, dirs, files in os.walk(abspath(root_path)):
        for filename in fnmatch.filter(dirs + files, pattern):
            yield join(path, filename)


class DistCleanCommand(setuptools.Command):
    description = "cleans up all build files, inline or otherwise"
    produce_pat = [
        '*.py[cod]',
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
            'List of comma delimited paths to delete. :default:'),
        ('dry-run', 'n',
            "Don't do anything just print"),
    ]

    def initialize_options(self):
        self.clean_exclude_paths = None
        self.clean_include_paths = ':default:'
        self.dry_run = False

    def finalize_options(self):
        # self.dry_run = strtobool(self.dry_run)
        log.info('%s' % self.dry_run)
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

        self.included_paths = map(abspath, include_paths)

    def run(self):
        log.info("include_paths:\n%s", '\n'.join(self.included_paths))
        dirs = []
        for pat in self.produce_dir:
            dirs += locate(pat, '.')

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

        if not self.dry_run:
            map(remove_tree, filtered_dirs)

        paths = []
        for pat in self.produce_pat:
            paths += locate(pat, '.')

        if paths:
            log.info("removing:\n%s", '\n'.join(paths))
            if not self.dry_run:
                map(os.remove, paths)


def clean_exclude_paths(dist, attr, value):
    pass

if __name__ == "__main__":
    p('called!')
