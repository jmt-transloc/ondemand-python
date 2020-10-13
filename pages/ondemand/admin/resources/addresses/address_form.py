from pages.ondemand.common.autocomplete_suggestions.autocomplete_suggestions import (
    AutocompleteSuggestions,
)
from utilities import Component, Selector, Selectors, WebElement


class AddressForm(Component):
    """Objects and methods for the Address Form component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('address-container')
    _address_field: Selector = Selectors.name('address')
    _cancel_button: Selector = Selectors.data_id('cancel-button')
    _delete_button: Selector = Selectors.data_id('delete-address-button')
    _label_field: Selector = Selectors.name('name')
    _save_button: Selector = Selectors.data_id('save-address-button')

    @property
    def address_field(self) -> WebElement:
        return self.container.find_element(*self._address_field)

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def delete_address_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def label_field(self) -> WebElement:
        return self.container.find_element(*self._label_field)

    @property
    def save_button(self) -> WebElement:
        return self.container.find_element(*self._save_button)

    @property
    def suggestions(self) -> AutocompleteSuggestions:
        return AutocompleteSuggestions(self)

    def fill_form(self, address: str, label: str) -> None:
        """Fill out an address form, then submit the form.

        :param address: The street address.
        :param label: The label for the address.
        """
        self.label_field.fill(label)
        self.address_field.fill(address)
        self.suggestions.select_suggestion(location=address)
