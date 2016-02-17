
from nodev.specs import generic


def test_iterable_contains():
    assert 'value' in generic.Container(['value'])


def test_mapping_contains():
    assert 'value' in generic.Container({'key': 'value'})


def test_object_contains():
    class C(object):
        pass
    obj = C()
    obj.attr = 'value'
    assert 'value' in generic.Container(obj)
