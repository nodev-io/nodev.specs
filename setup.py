#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


version = '0.3.0'

setup(
    name='nodev.specs',
    version=version,
    author='Alessandro Amici',
    author_email='alexamici@gmail.com',
    license='MIT',
    url='https://github.com/nodev-io/nodev.specs',
    download_url='https://github.com/nodev-io/nodev.specs/archive/%s.tar.gz' % version,
    description="nodev helpers to write specification tests.",
    long_description=read('README.rst'),
    namespace_packages=['nodev'],
    packages=['nodev', 'nodev.specs'],
    install_requires=[
        'future',
        'singledispatch',
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='source code search-by-tests nodev',
)
