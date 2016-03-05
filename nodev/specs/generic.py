# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import super

import inspect

try:
    # from python version >= 3.0
    from collections import abc
except ImportError:
    import collections as abc

try:
    # from python version >= 3.5
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch


@singledispatch
def contains(container, item):
    """Extends ``operator.contains`` by trying very hard to find ``item`` inside container."""
    contained = False
    try:
        contained = instance_contains(container, item)
    except:
        pass
    return contained


@contains.register(abc.Container)
@contains.register(abc.Iterator)
def container_contains(container, item):
    return item in container


@contains.register(abc.Mapping)
def mapping_contains(container, item):
    return item in container.values()


@contains.register(str)
def str_contains(container, item):
    return item in set(container)


def instance_contains(container, item):
    """Search into instance attributes and properties and class attributes."""
    return item in (p for _, p in inspect.getmembers(container))


class Container(object):
    def __init__(self, container):
        self.container = container

    def __contains__(self, item):
        return contains(self.container, item)


def generate_items(object):
    if isinstance(object, abc.Mapping):
        for key, value in object.items():
            yield key
            yield value
    elif isinstance(object, abc.Iterable):
        for item in object:
            yield item
    for name, attr in inspect.getmembers(object):
        if not name.startswith('_'):
            yield attr


def generate_flat_items(object):
    for item in generate_items(object):
        yield item
        try:
            for subitem in generate_items(item):
                yield subitem
        except:
            pass


class FlatContainer(tuple):
    def __new__(cls, object):
        super().__new__(generate_flat_items(object))

