from utilities import Component, Selector, Selectors, WebElement
from utilities.exceptions import RideTypeException


class ScheduleForm(Component):
    """Objects and methods for the Schedule form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-schedule-container')
    _asap_ride_button: Selector = Selectors.data_id('asap-ride-button')
    _future_ride_button: Selector = Selectors.data_id('future-ride-button')
    _recurring_ride_button: Selector = Selectors.data_id('recurring-ride-button')

    @property
    def asap_ride_button(self) -> WebElement:
        return self.container.find_element(*self._asap_ride_button)

    @property
    def future_ride_button(self) -> WebElement:
        return self.container.find_element(*self._future_ride_button)

    @property
    def recurring_ride_button(self) -> WebElement:
        return self.container.find_element(*self._recurring_ride_button)

    def select_ride_type(self, ride_type: str) -> None:
        """Select a ride type.

        Ride type defaults to ASAP within the OnDemand Admin application.

        :param ride_type: The type of ride to be submitted.
        """
        if ride_type == 'future':
            self.future_ride_button.click()
        elif ride_type == 'recurring':
            self.recurring_ride_button.click()
        elif ride_type != 'asap':
            raise RideTypeException(
                f'The ride type: {ride_type} is not supported.\n'
                f'Expected "asap", "future", or "recurring".',
            )
