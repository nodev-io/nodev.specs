# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici.
#

from nodev.specs import generic


def test_container_contains():
    assert 'value' in generic.Container(['value'])
    assert 'other' not in generic.Container(['value'])


def test_iterator_contains():
    assert 'value' in generic.Container(iter(['value']))
    assert 'other' not in generic.Container(iter(['value']))


def test_mapping_contains():
    assert 'value' in generic.Container({'key': 'value'})
    assert 'other' not in generic.Container({'key': 'value'})
    assert 'value' not in generic.Container({'value': 'other'})


def test_object_contains():
    class C(object):
        pass
    obj = C()
    obj.attr = 'value'
    assert 'value' in generic.Container(obj)
    assert 'other' not in generic.Container(obj)
