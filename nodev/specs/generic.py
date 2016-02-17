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
    return item in vars(container).values()


@contains.register(str)
def str_contains(container, item):
    return item in set(container)


@contains.register(abc.Container)
def container_contains(container, item):
    return item in container


@contains.register(abc.Iterator)
def iterator_contains(container, item):
    return item in container


@contains.register(abc.Mapping)
def mapping_contains(container, item):
    return item in container.values()


class Container(object):
    def __init__(self, container):
        self.container = container

    def __contains__(self, item):
        return contains(self.container, item)
