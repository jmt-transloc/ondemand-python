from pages.ondemand.admin.resources.addresses.address_form import AddressForm as AdminAddressForm
from pages.ondemand.common.addresses.deletion_modal import DeletionModal
from pages.ondemand.web.addresses.address_form import AddressForm as WebAddressForm
from utilities import Component, Selector, Selectors, WebElement


class KebabMenu(Component):
    """Objects and methods for the Kebab Menu component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('kebab-menu-container')
    _delete_button: Selector = Selectors.data_id('delete-address')
    _edit_button: Selector = Selectors.data_id('edit-address')

    @property
    def delete_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def edit_button(self) -> WebElement:
        return self.container.find_element(*self._edit_button)

    def delete_address(self) -> object:
        """Open the deletion modal for an address row."""
        self.delete_button.click()

        return DeletionModal(self).wait_for_component_to_be_present()

    def edit_address(self) -> object:
        """Open the edit address form for an address row.

        A conditional check for whether the URL contains 'admin' allows this method to be used in
        both OnDemand Web and OnDemand Admin.
        """
        self.edit_button.click()

        if 'admin' not in self.driver.current_url:
            return WebAddressForm(self).wait_for_component_to_be_present()
        return AdminAddressForm(self).wait_for_component_to_be_present()
