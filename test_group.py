# -*- coding:utf8 -*-
import datetime
import pytest
from freezegun import freeze_time

from group import Group

@pytest.fixture
def foo_group():
    return Group('foo_group', description="A group of foos", creator="Tyler")

def test_set_group_name():
    """"Assert behavior on group name & short_name"""
    test_group = foo_group()
    assert test_group.name == "foo_group"
    test_group.name = "A group of bars"
    assert test_group.name == "A group of bars"
    assert test_group.short_name == "foo_group"

def test_add_member():
    """Test adding a member to an ampty group"""
    test_group = foo_group()
    assert len(test_group.members()) == 0
    test_group.add_member('foo')
    assert len(test_group.members()) == 1
    assert test_group.members()[0] == 'foo'

def test_del_member():
    """Test deleting a member from a group created with two members"""
    test_group = Group('foo_bar_group',
                       description="A group of foos and bars",
                       creator="Tailor", members=['foo', 'bar'])
    assert len(test_group.members()) == 2
    assert test_group.members()[0] == 'foo'
    test_group.del_member('foo')
    assert len(test_group.members()) == 1
    assert test_group.members()[0] == 'bar'


def test_updated_at_on_description_change():
    """
    Test that the updated_at decorator results in the updated_at timestamp
    getting updated when we update the description

    """
    test_group = foo_group()
    with freeze_time("2018-01-14"):
        test_group.description = "A very timely group"
        assert test_group.updated_at == datetime.datetime(2018, 1, 14)

