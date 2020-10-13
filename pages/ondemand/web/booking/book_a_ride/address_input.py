from pages.ondemand.common.autocomplete_suggestions.autocomplete_suggestions import (
    AutocompleteSuggestions,
)
from utilities import Component, Selector, Selectors, WebElement


class AddressInput(Component):
    """Objects and methods for the Address Input component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-request-search')
    _pick_up_field: Selector = Selectors.value('Custom Pickup')
    _pick_up_submit: Selector = Selectors.data_id('pickup-submit')
    _drop_off_field: Selector = Selectors.value('Custom Drop-off')
    _drop_off_submit: Selector = Selectors.data_id('dropoff-submit')

    @property
    def drop_off_field(self) -> WebElement:
        return self.container.find_element(*self._drop_off_field)

    @property
    def drop_off_submit(self) -> WebElement:
        """Return the submit button.

        self.page.driver is used as the button exists outside of the address input container.
        """
        return self.page.driver.find_element(*self._drop_off_submit)

    @property
    def pick_up_field(self) -> WebElement:
        return self.container.find_element(*self._pick_up_field)

    @property
    def pick_up_submit(self) -> WebElement:
        """Return the submit button.

        self.page.driver is used as the button exists outside of the address input container.
        """
        return self.page.driver.find_element(*self._pick_up_submit)

    @property
    def suggestions(self) -> AutocompleteSuggestions:
        return AutocompleteSuggestions(self)

    def select_drop_off_location(self, drop_off: str) -> None:
        """Fill out a drop off location, then submit the location.

        :param drop_off: The drop off location for a ride.
        """
        self.drop_off_field.fill(drop_off)
        self.suggestions.select_suggestion(drop_off)

        self.drop_off_submit.click()

    def select_pick_up_location(self, pick_up: str) -> None:
        """Fill out a pick up location, then submit the location.

        :param pick_up: The pick up location for a ride.
        """
        self.pick_up_field.fill(pick_up)
        self.suggestions.select_suggestion(pick_up)

        self.pick_up_submit.click()
