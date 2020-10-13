from pages.ondemand.admin.resources.addresses.address_form import AddressForm
from pages.ondemand.admin.resources.resources import Resources
from pages.ondemand.common.addresses.addresses_list import AddressesList
from pages.ondemand.common.addresses.deletion_modal import DeletionModal
from utilities import Selector, Selectors, WebElement


class Addresses(Resources):
    """Objects and methods for the Addresses page.

    The addresses page may be accessed by selecting the 'Addresses' tab from the side navigation
    panel on the 'Resources' page.
    """

    URL_PATH = f'{Resources.URL_PATH}/addresses'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
    _fab_button: Selector = Selectors.data_id('new-button')

    @property
    def address_form(self) -> AddressForm:
        return AddressForm(self)

    @property
    def addresses_list(self) -> AddressesList:
        return AddressesList(self)

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def fab_button(self) -> WebElement:
        return self.driver.find_element(*self._fab_button)

    def add_new_address(self, address: dict) -> None:
        """Add a new address using the Address Form component.

        :param address: The address yielded from an address fixture.
        """
        self.fab_button.click()

        self.address_form.wait_for_component_to_be_present()
        self.address_form.fill_form(label=address['name'], address=address['address'])

        self.address_form.save_button.click()

        self.driver.wait_until_not_present(*AddressForm.ROOT_LOCATOR, wait_time=4)

    def delete_address(self, address: dict) -> None:
        """Delete an address by opening a row kebab, then selecting and confirming deletion.

        :param address: An address object yielded from an address factory.
        """
        row = self.addresses_list.surface_address_row(address)
        row.container.scroll_to()
        row.open_kebab_menu()
        row.kebab_menu.delete_address()

        self.deletion_modal.confirm_address_deletion()

    def edit_address(self, new_label: str) -> None:
        """Process an address edit by changing the label property.

        :param new_label: The new label for an existing address.
        """
        self.address_form.label_field.fill(new_label)
        self.address_form.save_button.click()

        self.driver.wait_until_not_present(*AddressForm.ROOT_LOCATOR, wait_time=4)

    def open_edit_address(self, address: dict) -> None:
        """Edit an address by opening a row kebab, then selecting edit.

        :param address: The address yielded from an address fixture.
        """
        row = self.addresses_list.surface_address_row(address)
        row.container.scroll_to()
        row.open_kebab_menu()
        row.kebab_menu.edit_address()
