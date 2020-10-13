from typing import Tuple, Union

from pages.ondemand.admin.resources.groups.group_row import GroupRow
from utilities import Component, Selector, Selectors, WebElements


class GroupsList(Component):
    """Objects and methods for the Groups List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('group-list-container')

    @property
    def groups_rows(self) -> Tuple:
        """Return a tuple of groups rows within the list container.
        """
        rows: WebElements = self.container.find_elements(*GroupRow.ROOT_LOCATOR)
        return tuple(GroupRow(self, element) for element in rows)

    def filter_rows(self, group: dict, group_name: str = None) -> Union[GroupRow, None]:
        """Filter all group rows for a match with a group name.

        :param group_name: An optional name for a group.
        :param group: A group object yielded from a group fixture.
        """
        name: str = group['name'] if group_name is None else group_name
        group_list: list = [row for row in self.groups_rows if name == row.name]

        if not group_list:
            return None
        return group_list[0]

    def surface_group_row(self, group: dict, group_name: str = None) -> Union[GroupRow, None]:
        """Raise a group row that matches a group name.

        :param group_name: An optional name for a group.
        :param group: A group object yielded from a group fixture.
        """
        return self.filter_rows(group, group_name=group_name)
