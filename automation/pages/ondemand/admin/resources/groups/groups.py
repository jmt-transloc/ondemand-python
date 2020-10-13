from pages.ondemand.admin.resources.groups.deletion_modal import DeletionModal
from pages.ondemand.admin.resources.groups.group_form import GroupForm
from pages.ondemand.admin.resources.groups.group_list import GroupsList
from pages.ondemand.admin.resources.groups.group_users.group_users import GroupUsers
from pages.ondemand.admin.resources.resources import Resources
from utilities import Selector, Selectors, WebElement


class Groups(Resources):
    """Objects and methods for the Groups page."""

    URL_PATH = f'{Resources.URL_PATH}/groups'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
    _fab_button: Selector = Selectors.data_id('new-button')

    @property
    def groups_form(self) -> GroupForm:
        return GroupForm(self)

    @property
    def groups_list(self) -> GroupsList:
        return GroupsList(self)

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def fab_button(self) -> WebElement:
        return self.driver.find_element(*self._fab_button)

    def add_new_group(self, group: dict) -> None:
        """Add a new group using the Group Form component.

        :param group: The group yielded from a group fixture.
        """
        self.fab_button.click()

        self.groups_form.wait_for_component_to_be_visible()
        self.groups_form.fill_form(name=group['name'])
        self.groups_form.save_button.click()

        self.driver.wait_until_not_present(*GroupForm.ROOT_LOCATOR, wait_time=4)

    def delete_group__kebab(self, group: dict) -> None:
        """Delete a group by opening a row kebab, then selecting and confirming deletion.

        :param group: A object yielded from a group factory.
        """
        row = self.groups_list.surface_group_row(group)

        row.open_kebab_menu()
        row.kebab_menu.delete_group()

        self.deletion_modal.wait_for_component_to_be_visible()
        self.deletion_modal.confirm_group_deletion()

    def delete_group__form(self) -> None:
        """Delete a group by opening a row kebab, then selecting and confirming deletion."""
        self.groups_form.delete_group_button.click()
        self.deletion_modal.wait_for_component_to_be_visible()

    def edit_group(self, new_name: str) -> None:
        """Process a group edit by changing the label property.

        :param new_name: The new label for an existing group.
        """
        self.groups_form.fill_form(name=new_name)
        self.groups_form.save_button.click()

        self.driver.wait_until_not_visible(*GroupForm.ROOT_LOCATOR, wait_time=4)

    def open_edit_group(self, group: dict) -> None:
        """Edit a group by opening a row kebab, then selecting edit.

        :param group: The group yielded from an group fixture.
        """
        row = self.groups_list.surface_group_row(group)

        row.open_kebab_menu()
        row.kebab_menu.edit_group()

    def open_manage_users(self, group: dict) -> None:
        """Manage group users by opening a row kebab, then selecting manage.

        :param group: The group yielded from an group fixture.
        """
        row = self.groups_list.surface_group_row(group)

        row.open_kebab_menu()
        row.kebab_menu.edit_group()

    def navigate_to_manage_users(self, group: dict) -> object:
        """Navigate to the group users page for a specific service using a direct URL.

        :param group: The group intended for navigation.
        """
        group_id: int = group['group_id']
        group_users_url = f'{self.URL_PATH}/{group_id}/users'
        self.driver.get(group_users_url)

        return GroupUsers(self.driver, group_users_url).wait_for_page_to_load()
