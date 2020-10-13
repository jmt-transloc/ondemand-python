from pages.ondemand.admin.resources.groups.kebab_menu import KebabMenu
from utilities import Component, Selector, Selectors, WebElement


class GroupRow(Component):
    """Group Row component objects and methods for the Group Page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('group-row')
    _group_id: Selector = Selectors.data_id('row-id')
    _group_name: Selector = Selectors.data_id('group-name')
    _kebab_button: Selector = Selectors.data_id('kebab-button')

    @property
    def group_id(self) -> str:
        """Return the unique group ID for a group row.

        The get_attribute method is used instead of .text as the row_id is a hidden attribute.
        """
        return self.container.find_element(*self._group_id).get_attribute('innerText')

    @property
    def kebab_button(self) -> WebElement:
        return self.container.find_element(*self._kebab_button)

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    @property
    def name(self) -> str:
        return self.container.find_element(*self._group_name).text

    def open_kebab_menu(self) -> object:
        """Open the kebab menu for an address row."""
        self.kebab_button.click()

        return KebabMenu(self).wait_for_component_to_be_visible()
