from datetime import datetime


def update_timestamp(func):
    """Method decorator to update updated_at timestamp"""
    def func_wrapper(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return func(self, *args, **kwargs)
    return func_wrapper


class MemberAlreadyInGroupError(Exception):
    pass

class MemberNotFoundInGroupError(Exception):
    pass


class Group(object):
    """
    A group of users
    """

    def __init__(self, short_name, **kwargs):
        self.short_name = short_name
        self._name = kwargs.get('name', short_name)
        self._description = kwargs.get('description')
        self.creator = kwargs.get('creator')
        self._created_at = datetime.utcnow()
        self.updated_at = self._created_at
        self._members = kwargs.get('members', [])

    @property
    def name(self):
        """The name of the group. Defaults to short_name if not given"""
        return self._name

    @name.setter
    @update_timestamp
    def name(self, value):
        self._name = value

    @name.deleter
    @update_timestamp
    def name(self):
        self._name = self.short_name

    @property
    def description(self):
        """Short description of the group"""
        return self._description

    @description.setter
    @update_timestamp
    def description(self, value):
        self._description = value

    @description.deleter
    @update_timestamp
    def description(self):
        del self._description

    @property
    def created_at(self):
        """
        When the group was created
        :returns: datetime object
        """
        return self._created_at

    @update_timestamp
    def add_member(self, member):
        """
        Add a member to the group
        :param: member - single member to add to the group
        :returns: list of members on success
        """
        if member not in self._members:
            self._members.append(member)
            return self._members
        else:
            raise MemberAlreadyInGroupError(
                "Member {} already in group".format(member))

    @update_timestamp
    def del_member(self, member):
        """
        Delete a member from the group
        :param: member - single member to delete from the group
        :returns: list of members on success
        """
        if member in self._members:
            self._members = list(filter(member.__ne__, self._members))
            return self._members
        else:
            raise MemberNotFoundInGroupError(
                "Member {} not found in group".format(member))

    def members(self):
        """
        Get members for the group
        :returns: list of members of the group
        """
        return self._members
