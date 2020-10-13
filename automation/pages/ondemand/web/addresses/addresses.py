from pages.ondemand.common.addresses.addresses_list import AddressesList
from pages.ondemand.common.addresses.deletion_modal import DeletionModal
from pages.ondemand.web.addresses.address_form import AddressForm
from pages.ondemand.web.base.base import Base
from utilities import Selector, Selectors, WebElement


class Addresses(Base):
    """Objects and methods for the Addresses page.

    The addresses page may be accessed by selecting the 'My Addresses' tab from any location
    within the OnDemand Web application.
    """

    URL_PATH = f'{Base.URL_PATH}/addresses'
    ROOT_LOCATOR: Selector = Selectors.data_id('addresses-page-container')
    _new_address_button: Selector = Selectors.data_id('new-address-button')
    _no_addresses_message: Selector = Selectors.data_id('no-addresses-message')

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
    def new_address_button(self) -> WebElement:
        return self.driver.find_element(*self._new_address_button)

    @property
    def no_addresses_message(self) -> WebElement:
        return self.driver.find_element(*self._no_addresses_message)

    def add_new_address(self, address: dict) -> None:
        """Add a new address using the Address Form component.

        :param address: The address yielded from an address fixture.
        """
        self.new_address_button.click()

        self.address_form.select_location(address['address'])
        self.address_form.label_input.fill(address['name'])

        self.address_form.save_button.click()

    def delete_address(self, address: dict) -> None:
        """Delete an address by opening a row kebab, then selecting and confirming deletion.

        :param address: An address object yielded from an address factory.
        """
        row = self.addresses_list.surface_address_row(address)

        row.open_kebab_menu()
        row.kebab_menu.delete_address()

        self.deletion_modal.confirm_address_deletion()

    def edit_address(self, new_label: str) -> None:
        """Process an address edit by changing the label property.

        :param new_label: The new label for an existing address.
        """
        self.address_form.label_input.fill(new_label)
        self.address_form.save_button.click()

    def open_edit_address(self, address: dict) -> None:
        """Edit an address by opening a row kebab, then selecting edit.

        :param address: The address yielded from an address fixture.
        """
        row = self.addresses_list.surface_address_row(address)

        row.open_kebab_menu()
        row.kebab_menu.edit_address()
