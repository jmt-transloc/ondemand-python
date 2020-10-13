from utilities import Component, Selector, Selectors, WebElement


class PickupTimeModal(Component):
    """Objects and methods for the Pickup Time Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('pickup-time-modal-container')
    _asap_ride_radio: Selector = Selectors.value('use-now')
    _future_ride_radio: Selector = Selectors.value('use-later')
    _back_button: Selector = Selectors.data_id('pickup-time-modal-back-button')
    _continue_button: Selector = Selectors.data_id('pickup-time-modal-continue-button')
    _date_field: Selector = Selectors.data_id('pickup-time-modal-date-field')
    _time_field: Selector = Selectors.data_id('pickup-time-modal-time-field')

    @property
    def asap_ride_button(self) -> WebElement:
        return self.container.find_element(*self._asap_ride_radio)

    @property
    def back_button(self) -> WebElement:
        return self.container.find_element(*self._back_button)

    @property
    def continue_button(self) -> WebElement:
        return self.container.find_element(*self._continue_button)

    @property
    def date_field(self) -> WebElement:
        return self.container.find_element(*self._date_field)

    @property
    def future_ride_button(self) -> WebElement:
        return self.container.find_element(*self._future_ride_radio)

    @property
    def time_field(self) -> WebElement:
        return self.container.find_element(*self._time_field)

    def submit_pickup_time(self) -> None:
        """Submit a selected pick up time."""
        self.continue_button.click()
