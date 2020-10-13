from datetime import datetime

from utilities import Component, Selector, Selectors, WebElement


class FutureRideForm(Component):
    """Objects and methods for the future ride form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('future-ride-container')
    _date_field: Selector = Selectors.name('pickupDate')
    _time_field: Selector = Selectors.name('time')

    @property
    def date_field(self) -> WebElement:
        return self.container.find_element(*self._date_field)

    @property
    def time_field(self) -> WebElement:
        return self.container.find_element(*self._time_field)

    def fill_future_ride_form(self, ride: dict) -> None:
        """Fill out the future ride form.

        :param ride: The ride yielded from a ride fixture.
        """
        ride_time: datetime = datetime.strptime(
            ride['pickup']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ',
        )

        self.time_field.fill_picker_input(ride_time.strftime('%I:%M %p'))
        self.date_field.fill_picker_input(ride_time.strftime('%m-%d-%Y'))
