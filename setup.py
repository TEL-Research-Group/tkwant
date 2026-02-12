#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016-2023 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.

import os
import sys
import configparser
import versioneer

from setuptools import setup, Extension


CONFIG_FILE = 'build.conf'
CYTHON_OPTION = '--no-cython'
CYTHON_TRACE_OPTION = '--cython-trace'


# Cython setup
try:
    sys.argv.remove(CYTHON_OPTION)
    use_cython = False
except ValueError:
    use_cython = True

try:
    sys.argv.remove(CYTHON_TRACE_OPTION)
    trace_cython = True
except ValueError:
    trace_cython = False

if use_cython:
    try:
        import Cython
        from Cython.Build import cythonize
        cython_present = True
    except ImportError:
        cython_present = False


# ----------------- utility functions

def complain_cython_unavailable():
    if use_cython:
        msg = ("Install Cython so it can be made\n"
               "or use a source distribution of tkwant.")
        print(msg, file=sys.stderr)


def extension_config():
    # --- Configure external dependencies
    config = configparser.ConfigParser()
    try:
        with open(CONFIG_FILE) as f:
            config.read_file(f)
    except IOError:
        pass

    kwrds_by_section = {}
    for section in config.sections():
        kwrds_by_section[section] = kwrds = {}
        for name, value in config.items(section):
            kwrds[name] = value.split()
    return kwrds_by_section


def extensions():
    """Return a list of tuples (args, kwrds) to be passed to Extension."""
    result = []
    kwrds_by_section = extension_config()

    # -- add tkwant components

    # kernels
    result.append((['tkwant.onebody.kernels', ['tkwant/onebody/kernels.pyx']],
                   {}))

    # solvers
    result.append((['tkwant.onebody.solvers', ['tkwant/onebody/solvers.pyx']],
                   {'depends': ['tkwant/onebody/kernels.pxd']}))

    # --- Add cython tracing macro
    if trace_cython:
        for args, kwargs in result:
            macros = kwargs.get('define_macros', [])
            macros.append(('CYTHON_TRACE', '1'))
            kwargs['define_macros'] = macros

    return result


def ext_modules(extensions):
    """Prepare the ext_modules argument for setuptools.

    If Cython is not to be run, replace .pyx extensions with .c or .cpp, and
    check timestamps.
    """
    if use_cython:
        return cythonize([Extension(*args, **kwrds) for args, kwrds in extensions],
                         language_level=3,
                         compiler_directives={'profile': False,
                                              'linetrace': trace_cython}
                         )

    # Cython is not going to be run: replace pyx extension by that of
    # the shipped translated file.
    if 'egg_info' in sys.argv:
        return

    result = []
    problematic_files = []
    for args, kwrds in extensions:
        name, sources = args

        language = kwrds.get('language')
        if language is None:
            ext = '.c'
        elif language == 'c':
            ext = '.c'
        elif language == 'c++':
            ext = '.cpp'
        else:
            print('Unknown language: {}'.format(language), file=sys.stderr)
            exit(1)

        pyx_files = []
        cythonized_files = []
        new_sources = []
        for f in sources:
            if f.endswith('.pyx'):
                pyx_files.append(f)
                f = f.rstrip('.pyx') + ext
                cythonized_files.append(f)
            new_sources.append(f)
        sources = new_sources

        # Complain if cythonized files are older than Cython source files.
        try:
            cythonized_oldest = min(os.stat(f).st_mtime
                                    for f in cythonized_files)
        except OSError:
            print("error: Cython-generated file {} is missing.".format(f),
                  file=sys.stderr)
            complain_cython_unavailable()
            exit(1)

        for f in pyx_files + kwrds.get('depends', []):
            if f == CONFIG_FILE:
                # The config file is only a dependency for the compilation
                # of the cythonized file, not for the cythonization.
                continue
            if os.stat(f).st_mtime > cythonized_oldest:
                problematic_files.append(f)

        result.append(Extension(name, sources, **kwrds))

    if problematic_files:
        problematic_files = ", ".join(problematic_files)
        msg = ("Some Cython source files are newer than files that should have\n"
               "been derived from them, but {}.\n"
               "\n"
               "Affected files: {}")
        if use_cython:
            if not cython_present:
                reason = "Cython is not installed"
            print(banner(" Error "), msg.format(reason, problematic_files),
                  banner(), sep="\n", file=sys.stderr)
            print()
            complain_cython_unavailable()
            exit(1)
        else:
            reason = "the option {} has been given or no cython available.".format(CYTHON_OPTION)
            dontworry = ('(Do not worry about this if you are building tkwant\n'
                         'from unmodified sources, e.g. with "pip install".)\n')
            print(banner(" Caution "), dontworry,
                  msg.format(reason, problematic_files),
                  banner(), sep='\n', file=sys.stderr)

    return result


def banner(title=''):
    starred = title.center(79, '*')
    return '\n' + starred if title else starred


def main():
    kwargs = dict(
        name='tkwant',
        version=versioneer.get_version(),
        ext_modules=ext_modules(extensions()))
    setup(**kwargs)


if __name__ == '__main__':
    main()
