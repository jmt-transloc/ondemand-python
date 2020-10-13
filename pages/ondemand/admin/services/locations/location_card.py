from utilities import Component, Selector, Selectors, WebElement


class LocationCard(Component):
    """Objects and methods for the Location Card component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('location-card')
    _card_id: Selector = Selectors.data_id('card-id')
    _drop_off_field: Selector = Selectors.data_id('dropoff-checkbox')
    _hub_field: Selector = Selectors.data_id('hub-checkbox')
    _input: Selector = Selectors.tag('input')
    _label: Selector = Selectors.data_id('location-card-label')
    _pick_up_field: Selector = Selectors.data_id('pickup-checkbox')

    @property
    def card_id(self) -> str:
        """Return the unique address ID for a location card.

        The get_attribute method is used instead of .text as the service_id is a hidden attribute.
        """
        return self.container.find_element(*self._card_id).get_attribute('innerText')

    @property
    def drop_off_checkbox(self) -> WebElement:
        return self.drop_off_field.find_element(*self._input)

    @property
    def drop_off_field(self) -> WebElement:
        return self.container.find_element(*self._drop_off_field)

    @property
    def hub_checkbox(self) -> WebElement:
        return self.hub_field.find_element(*self._input)

    @property
    def hub_field(self) -> WebElement:
        return self.container.find_element(*self._hub_field)

    @property
    def label(self) -> str:
        return self.container.find_element(*self._label).text

    @property
    def pick_up_checkbox(self) -> WebElement:
        return self.pick_up_field.find_element(*self._input)

    @property
    def pick_up_field(self) -> WebElement:
        return self.container.find_element(*self._pick_up_field)

    def hub_card(self) -> WebElement:
        """Run a check to see whether a card is a hub card or not."""
        return self.container.wait_until_present(*self._hub_field)
