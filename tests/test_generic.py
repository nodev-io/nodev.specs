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


def test_str_contains():
    assert 'v' in generic.Container('value')
    assert 'k' not in generic.Container('value')
    assert 'value' not in generic.Container('other_value!!')


def test_instance_contains():
    # instance attributes
    class A(object):
        pass
    instance = A()
    instance.attr = 'value'
    assert 'value' in generic.Container(instance)
    assert 'other' not in generic.Container(instance)

    # instance properties
    class B(object):
        @property
        def attr(self):
            return 'value'
    instance = B()
    assert 'value' in generic.Container(instance)
    assert 'other' not in generic.Container(instance)

    # class attributes
    class C(object):
        attr = 'value'
    instance = C()
    assert 'value' in generic.Container(instance)
    assert 'other' not in generic.Container(instance)
