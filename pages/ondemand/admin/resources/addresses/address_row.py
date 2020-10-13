from pages.ondemand.common.addresses.kebab_menu import KebabMenu
from utilities import Component, Selector, Selectors, WebElement


class AddressRow(Component):
    """Address Row component objects and methods for the Addresses Page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('address-row')
    _address_data: Selector = Selectors.data_id('address')
    _address_id: Selector = Selectors.data_id('row-id')
    _address_label: Selector = Selectors.data_id('address-label')
    _kebab_button: Selector = Selectors.data_id('kebab-button')

    @property
    def address_id(self) -> str:
        """Return the unique address ID for a service row.

        The get_attribute method is used instead of .text as the service_id is a hidden attribute.
        """
        return self.container.find_element(*self._address_id).get_attribute('innerText')

    @property
    def data(self) -> str:
        return (
            f'{self.container.find_element(*self._address_label).text}\n'
            f'{self.container.find_element(*self._address_data).text}'
        )

    @property
    def kebab_button(self) -> WebElement:
        return self.container.find_element(*self._kebab_button)

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    @property
    def label(self) -> str:
        return self.container.find_element(*self._address_label).text

    def open_kebab_menu(self) -> object:
        """Open the kebab menu for an address row."""
        self.kebab_button.click()

        return KebabMenu(self).wait_for_component_to_be_visible()
