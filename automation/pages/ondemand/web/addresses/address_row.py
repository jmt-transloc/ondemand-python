from pages.ondemand.common.addresses.kebab_menu import KebabMenu
from utilities import Component, Selector, Selectors, WebElement


class AddressRow(Component):
    """Objects and methods for the Address Row component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('address-list-row')
    _address_id: Selector = Selectors.data_id('address-row-id')
    _data: Selector = Selectors.data_id('address-row-data')
    _kebab_button: Selector = Selectors.data_id('address-row-kebab-button')

    @property
    def address_id(self) -> str:
        """Return the unique address ID for an address row.

        The get_attribute method is used instead of .text as the ride_id is a hidden attribute.
        """
        return self.container.find_element(*self._address_id).get_attribute('innerText')

    @property
    def data(self) -> str:
        return self.container.find_element(*self._data).text

    @property
    def kebab_button(self) -> WebElement:
        return self.container.find_element(*self._kebab_button)

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    def open_kebab_menu(self) -> object:
        """Open the kebab menu for an address row."""
        self.kebab_button.click()

        return KebabMenu(self).wait_for_component_to_be_present()
