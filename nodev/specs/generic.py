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


def mapping_contains(container, item):
    assert isinstance(container, abc.Mapping)
    return item in container.values() or item in container


def str_strict_contains(container, item):
    assert isinstance(container, str)
    return item in list(container)


def instance_contains(container, item):
    """Search into instance attributes, properties and return values of no-args methods."""
    for _, member in inspect.getmembers(container):
        if item == member:
            return True
        if callable(member):
            try:
                if item == member():
                    return True
            except:
                pass
    return False


def contains(container, item):
    """Extends ``operator.contains`` by trying very hard to find ``item`` inside container."""

    # equality counts as containment
    if container == item:
        return True

    # standard containment except special cases
    if isinstance(container, str):
        # str __contains__ includes substring match that we don't count as containment
        if str_strict_contains(container, item):
            return True
    elif isinstance(container, abc.Container) or isinstance(container, abc.Iterable):
        if item in container:
            return True

    # search matches more thoroughly in known containers
    if isinstance(container, abc.Mapping) and mapping_contains(container, item):
        return True

    # search matches in generic instances
    return instance_contains(container, item)


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

