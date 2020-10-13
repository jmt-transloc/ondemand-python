from pages.ondemand.common.autocomplete_suggestions.autocomplete_suggestions import (
    AutocompleteSuggestions,
)
from utilities import Component, Selector, Selectors, WebElement


class AddressForm(Component):
    """Objects and methods for the Address Form component.

    The address form is used in both editing and creating addresses. It may be accessed by selecting
    'EDIT' from an address kebab menu or by selecting the FAB button for creating a new address.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('address-form-container')
    _button_container: Selector = Selectors.data_id('address-form-button-container')
    _cancel_button: Selector = Selectors.data_id('address-form-cancel-button')
    _label_input: Selector = Selectors.placeholder('Label')
    _location_input: Selector = Selectors.placeholder('Search for a location...')
    _places_autocomplete_suggestion: Selector = Selectors.data_id('places-autocomplete-suggestion')
    _save_button: Selector = Selectors.data_id('address-form-confirm-button')

    @property
    def button_container(self) -> WebElement:
        return self.container.find_element(*self._button_container)

    @property
    def cancel_button(self) -> WebElement:
        return self.button_container.find_element(*self._cancel_button)

    @property
    def label_input(self) -> WebElement:
        return self.container.find_element(*self._label_input)

    @property
    def location_input(self) -> WebElement:
        return self.container.find_element(*self._location_input)

    @property
    def save_button(self) -> WebElement:
        return self.button_container.find_element(*self._save_button)

    @property
    def suggestions(self) -> AutocompleteSuggestions:
        return AutocompleteSuggestions(self)

    def select_location(self, location: str) -> None:
        """Fill out an address location, then submit the location.

        :param location: The location for an address.
        """
        self.location_input.fill(location)
        self.suggestions.select_suggestion(location)
