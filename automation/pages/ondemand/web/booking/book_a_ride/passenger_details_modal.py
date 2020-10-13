from utilities import Component, Selector, Selectors, WebElement


class PassengerDetailsModal(Component):
    """Objects and methods for the Passenger Details Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('passenger-details-container')
    _next_button: Selector = Selectors.data_id('next-button')
    _capacity_input: Selector = Selectors.data_id('capacity-select')
    _wheelchair_container: Selector = Selectors.data_id('wheelchair-container')

    @property
    def next_button(self) -> WebElement:
        return self.container.find_element(*self._next_button)

    @property
    def capacity_input(self) -> WebElement:
        return self.container.find_element(*self._capacity_input)

    @property
    def wheelchair_container(self) -> WebElement:
        return self.container.find_element(*self._wheelchair_container)

    def wheelchair_select(self) -> None:
        """Select the wheelchair input for a ride."""
        self.wheelchair_container.click()
