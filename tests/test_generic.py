# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici.
#

from nodev.specs import generic


def test_mapping_contains(mapping_contains=generic.mapping_contains):
    assert mapping_contains({'key': 'value'}, 'key')
    assert mapping_contains({'key': 'value'}, 'value')
    assert not mapping_contains({'key': 'value'}, 'other')


def test_strict_contains(strict_contains=generic.strict_contains):
    assert strict_contains('value', 'v')
    assert not strict_contains('value', 'k')
    assert not strict_contains('value', 'val')


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


def test_contains(contains=generic.contains):
    assert contains('value', 'value')
    test_strict_contains(generic.contains)
    assert contains(['value'], 'value')
    assert contains(iter(['value']), 'value')
    test_mapping_contains(contains)
    test_instance_contains_attributes(contains)
    test_instance_contains_properties(contains)


def test_flat_contains(flat_contains=generic.flat_contains):
    test_contains(flat_contains)
    assert flat_contains([('key', 'value')], 'value')
    assert flat_contains({'key': ['value']}, 'value')

    class C(object):
        attr = {'key': 'value'}

    assert flat_contains(C(), 'value')


def test_container(container=generic.Container):
    assert 'value' in container('value')
    assert 'other' not in container('value')

    assert 'value' in container(iter(['value']))
    assert 'other' not in container(iter(['value']))

    assert 'value' in container({'key': 'value'})
    assert 'other' not in container({'key': 'value'})

    assert 'v' in container('value')
    assert 'k' not in container('value')

    # instance attributes
    class A(object):
        pass
    instance = A()
    instance.attr = 'value'
    assert 'value' in container(instance)
    assert 'other' not in container(instance)

    # instance properties
    class B(object):
        @property
        def attr(self):
            return 'value'
    instance = B()
    assert 'value' in container(instance)
    assert 'other' not in container(instance)

    # class attributes
    class C(object):
        attr = 'value'
    instance = C()
    assert 'value' in container(instance)
    assert 'other' not in container(instance)


def test_flat_container():
    test_container(generic.FlatContainer)

    assert 'value' in generic.FlatContainer([('value', 0)])
    assert 'value' in generic.FlatContainer(iter([('value', 0)]))