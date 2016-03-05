# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici.
#

from nodev.specs import generic


def test_mapping_contains(mapping_contains=generic.mapping_contains):
    assert mapping_contains({'key': 'value'}, 'key')
    assert mapping_contains({'key': 'value'}, 'value')
    assert not mapping_contains({'key': 'value'}, 'other')


def test_str_strict_contains(str_strict_contains=generic.str_strict_contains):
    assert str_strict_contains('value', 'v')
    assert not str_strict_contains('value', 'k')
    assert not str_strict_contains('value', 'val')


def test_instance_contains_attributes(instance_contains=generic.instance_contains):
    # instance attribute
    class A(object):
        pass
    instance = A()
    instance.attr = 'value'
    assert instance_contains(instance, 'value')
    assert not instance_contains(instance, 'other')

    # class attribute
    class C(object):
        attr = 'value'
    instance = C()
    assert instance_contains(instance, 'value')
    assert not instance_contains(instance, 'other')


def test_instance_contains_properties(instance_contains=generic.instance_contains):
    class B(object):
        @property
        def attr(self):
            return 'value'
    instance = B()
    assert instance_contains(instance, 'value')
    assert not instance_contains(instance, 'other')


def test_instance_contains_methods():
    class B(object):
        def attr(self):
            return 'value'
    instance = B()
    assert generic.instance_contains(instance, 'value')
    assert not generic.instance_contains(instance, 'other')


def test_contains():
    assert generic.contains('value', 'value')
    test_str_strict_contains(generic.contains)
    assert generic.contains(['value'], 'value')
    assert generic.contains(iter(['value']), 'value')
    test_mapping_contains(generic.contains)
    test_instance_contains_properties(generic.contains)


def test_container():
    assert 'value' in generic.Container('value')
    assert 'other' not in generic.Container('value')

    assert 'value' in generic.Container(iter(['value']))
    assert 'other' not in generic.Container(iter(['value']))

    assert 'value' in generic.Container({'key': 'value'})
    assert 'other' not in generic.Container({'key': 'value'})

    assert 'v' in generic.Container('value')
    assert 'k' not in generic.Container('value')

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
