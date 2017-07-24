# -*- coding:utf8 -*-
from errbot.backends.test import testbot
import pytest
from group import Group
import groups

@pytest.fixture
def foo_group():
    return Group('foo_group', description="A group of foos", creator="Tyler")

class TestGroups(object):

    extra_plugin_dir = '.'

    def fetch_plugin(self, testbot):
        return testbot.bot.plugin_manager.get_plugin_obj_by_name(
            'Groups')

    def test_groups(self, testbot):
        plugin = self.fetch_plugin(testbot)
        result = plugin.groups()
        assert result == []


    def test_cant__add_group_short_name_twice(self, testbot):
        """
        Assert that we cannot add two groups with the same short_name twice
        """
        plugin = self.fetch_plugin(testbot)
        group_1 = foo_group()
        group_2 = Group(
            'foo_group',
            description="An alternative group of foos",
            name="The Alternative Foos"
        )
        plugin._add_group(group_1)
        assert len(plugin.groups()) == 1
        # yapsy subclasses our custom exception class so we match for
        # superclass instead
        with pytest.raises(Exception) as e:
            plugin._add_group(group_2)
        assert str(e.value) == "Group {} already exists".format(
            group_2.name)

    def test_cant__add_group_name_twice(self, testbot):
        """
        Assert that we cannot add two groups with the same name twice
        """
        plugin = self.fetch_plugin(testbot)
        group_1 = foo_group()
        group_2 = Group(
            'foo_alt_group',
            name='foo_group',
            description="An alternative group of foos",
        )
        plugin._add_group(group_1)
        assert len(plugin.groups()) == 1
        # yapsy subclasses our custom exception class so we match for
        # superclass instead
        with pytest.raises(Exception) as e:
            plugin._add_group(group_2)
        assert str(e.value) == "Group {} already exists".format(
            group_2.name)