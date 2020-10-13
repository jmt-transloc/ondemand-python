from typing import List, Tuple, Union

from pages.ondemand.admin.edit_service.restricted_groups.group_row import GroupRow
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors, WebElement


class GroupRestrictionsModal(Component):
    """Objects and methods for the Restricted Groups modal."""

    ROOT_LOCATOR: Selector = Selectors.data_id('groups-modal-container')
    _manage_agency_groups_button: Selector = Selectors.data_id('groups-manage-button')
    _no_groups_message: Selector = Selectors.data_id('no-user-groups-message')
    _save_button: Selector = Selectors.data_id('save-groups-modal-button')
    _cancel_button: Selector = Selectors.data_id('cancel-groups-modal-button')

    @property
    def manage_agency_button(self) -> WebElement:
        return self.container.find_element(*self._manage_agency_groups_button)

    @property
    def save_button(self) -> WebElement:
        return self.container.find_element(*self._save_button)

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def no_user_groups_message(self) -> str:
        return self.container.find_element(*self._no_groups_message).text

    @property
    def groups_rows(self) -> List[GroupRow]:
        return [
            GroupRow(self.page, item)
            for item in self.container.find_elements(*GroupRow.ROOT_LOCATOR)
        ]

    def filter_group_rows(self, group: dict) -> Union[GroupRow, None]:
        """Filter all groups for a match with a group id.

        :param group: The group intended to be raised.
        """
        groups_list: Tuple[GroupRow, ...] = tuple(
            item for item in self.groups_rows if item.group_id == group['group_id']
        )

        if not groups_list:
            raise NoSuchElementException
        return groups_list[0]

    def surface_group_row(self, group: dict) -> GroupRow:
        """Raise a group row for later use.

        :param group: The group intended to be raised.
        """
        return self.filter_group_rows(group)
