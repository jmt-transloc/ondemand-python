from pages.ondemand.admin.resources.groups.deletion_modal import DeletionModal
from pages.ondemand.admin.resources.groups.group_form import GroupForm
from pages.ondemand.admin.resources.groups.group_users.group_user_form import GroupUserForm
from utilities import Component, Selector, Selectors, WebElement


class KebabMenu(Component):
    """Objects and methods for the Kebab Menu component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('kebab-menu-container')
    _delete_button: Selector = Selectors.data_id('delete-group')
    _edit_button: Selector = Selectors.data_id('edit-group')
    _manage_button: Selector = Selectors.data_id('manage-users-item')

    @property
    def delete_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def edit_button(self) -> WebElement:
        return self.container.find_element(*self._edit_button)

    @property
    def manage_button(self) -> WebElement:
        return self.container.find_element(*self._manage_button)

    def delete_group(self) -> object:
        """Open the deletion modal for a group row."""
        self.delete_button.click()

        return DeletionModal(self).wait_for_component_to_be_visible()

    def edit_group(self) -> object:
        """Open the edit group form for a group row."""
        self.edit_button.click()

        return GroupForm(self).wait_for_component_to_be_visible()

    def manage_group_users(self) -> object:
        """Open the edit group form for a group row."""
        self.manage_button.click()

        return GroupUserForm(self).wait_for_component_to_be_visible()
