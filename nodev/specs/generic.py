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

import inspect


try:
    # from python version >= 3.0
    from collections import abc
except ImportError:
    import collections as abc


def mapping_contains(container, item):
    return item in container.values() or item in container


def strict_contains(container, item):
    return item in iter(container)


def instance_contains(container, item):
    """Search into instance attributes, properties and return values of no-args methods."""
    return item in (member for _, member in inspect.getmembers(container))


def contains(container, item):
    """Extends ``operator.contains`` by trying very hard to find ``item`` inside container."""

    # equality counts as containment and is usually non destructive
    if container == item:
        return True

    # standard containment except special cases
    if isinstance(container, str):
        # str __contains__ includes substring match that we don't count as containment
        if strict_contains(container, item):
            return True
    elif isinstance(container, abc.Container) or isinstance(container, abc.Iterable):
        if item in container:
            return True

    # search matches more thoroughly in known containers
    if isinstance(container, abc.Mapping) and mapping_contains(container, item):
        return True

    # search matches in generic instances
    return instance_contains(container, item)


def flat_contains(container, item):
    # equality counts as containment and is usually non destructive
    if container == item:
        return True

    # iterating on a mapping is usually non destructive
    if isinstance(container, abc.Mapping):
        for content in container.values():
            if contains(content, item):
                return True

    # iterating on an itarator is destructive, but accounts form most of the sensible use cases
    if isinstance(container, abc.Iterable):
        for content in container:
            if contains(content, item):
                return True

    for _, content in inspect.getmembers(container):
        if contains(content, item):
            return True

    return contains(container, item)


class Container(object):
    def __init__(self, container):
        self.container = container

    def __contains__(self, item):
        return contains(self.container, item)


class FlatContainer(Container):
    def __contains__(self, item):
        return flat_contains(self.container, item)
