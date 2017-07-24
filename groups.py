from errbot import BotPlugin, botcmd, arg_botcmd
from group import Group

class GroupAlreadyExistsError(Exception):
    pass


class Groups(BotPlugin):
    """
    Group is an Errbot plugin for interacting and managing groups of users
    """
    def activate(self):
        """
        Triggers on plugin activation
        You should delete it if you're not using it to override any default behaviour
        """
        super(Groups, self).activate()
        if not 'groups' in self:
            self['groups'] = []


    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def group_names(self):
        """
        :returns: Tuple of group names
        """
        return tuple(g.name for g in self['groups'])

    def group_short_names(self):
        """
        :returns: Tuple of group short_names
        """
        return tuple(g.short_name for g in self['groups'])

    def groups(self):
        """
        :returns: A list containing all group objects
        """
        return self['groups']

    def create_group(self, short_name, *args, **kwargs):
        """
        Create a group (and then add it to the store)
        :param: short_name - short name of the group
        :returns: group
        """
        _group = Group(short_name, *args, **kwargs)
        result = self._add_group(_group)
        return result


    @arg_botcmd('short_name', type=str)
    @arg_botcmd('--full-name', dest='full_name', type=str)
    @arg_botcmd('--description', dest='description', type=str)
    @arg_botcmd('--members', dest='members', type=list)
    def group_create(self, msg, short_name, full_name=None,
                     description=None, members=None):
        """Create a group"""
        result = self.create_group(
            short_name, name=full_name,
            description=description, members=members)
        return "Group {} created!".format(result.short_name)

    @botcmd()
    def group_list(self, msg, args):
        """List groups"""
        return self.group_names()

    def _add_group(self, group: Group):
        """
        Add a Group object to the store
        :param: group - a Group
        """
        if (group.short_name not in self.group_short_names()) and \
            (group.name not in self.group_names()):
            # TODO - do we need to store with mutable context manager?
            with self.mutable('groups') as g:
                g = self['groups'].append(group)
            self.log.info("Group created: {}".format(group.short_name))
            return group
        else:
            raise GroupAlreadyExistsError('Group {} already exists'.format(
                group.name))
