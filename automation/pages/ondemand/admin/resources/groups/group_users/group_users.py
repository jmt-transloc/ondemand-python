from typing import Union

from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.resources.groups.group_users.bulk_import_users.bulk_import_users import (
    BulkImportUsers,
)
from pages.ondemand.admin.resources.groups.group_users.deletion_modal import DeletionModal
from pages.ondemand.admin.resources.groups.group_users.group_user_form import GroupUserForm
from pages.ondemand.admin.resources.groups.group_users.group_user_list import GroupUserList
from pages.ondemand.admin.resources.groups.group_users.group_user_row import GroupUserRow
from utilities import Selector, Selectors, WebElement


class GroupUsers(Base):
    """Objects and methods for the Groups Users page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('rider-editor-container')
    _back_button: Selector = Selectors.data_id('back-button')
    _fab_button: Selector = Selectors.data_id('new-button')
    _user_import_button: Selector = Selectors.data_id('user-import-button')

    @property
    def back_button(self) -> WebElement:
        return self.driver.find_element(*self._back_button)

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def group_id(self) -> str:
        """Return a group ID parsed from the Group Users page URL."""
        id = self.driver.current_url.replace(f'{Base.URL_PATH}/resources/groups/', '')

        if '?' in self.driver.current_url:
            return id[: id.find('/users')]
        return id

    @property
    def group_user_form(self) -> GroupUserForm:
        return GroupUserForm(self)

    @property
    def group_user_list(self) -> GroupUserList:
        return GroupUserList(self)

    @property
    def user_import_button(self) -> WebElement:
        return self.driver.find_element(*self._user_import_button)

    def add_user(self, user: dict) -> None:
        """Add a new user using the Group User Form component.

        :param user: The user yielded from a user fixture.
        """
        self.group_user_form.fill_form(email=user['email'])
        row = self.group_user_list.surface_user_row(user, wait_for_row=True)
        row.add_button.click()

    def find_user(self, user: dict) -> Union[GroupUserRow, None]:
        """Find a user in the groups UI.

        :param user: The user yielded from a user fixture.
        """
        self.group_user_form.fill_form(email=user['email'])
        return self.group_user_list.surface_user_row(user, wait_for_row=True)

    def navigate_to_bulk_import(self) -> BulkImportUsers:
        """Navigate to the Bulk Import Users page."""
        self.user_import_button.click()

        return BulkImportUsers(self)

    def remove_user(self, user: dict) -> None:
        """Delete a user and confirming deletion.

        :param user: A object yielded from a user factory.
        """
        row = self.group_user_list.surface_user_row(user, wait_for_row=True)
        row.remove_button.click()

        self.deletion_modal.wait_for_component_to_be_visible()
        self.deletion_modal.confirm_removal()
