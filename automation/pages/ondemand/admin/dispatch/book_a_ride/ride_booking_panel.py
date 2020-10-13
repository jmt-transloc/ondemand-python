from pages.ondemand.admin.dispatch.book_a_ride.future_ride_form import FutureRideForm
from pages.ondemand.admin.dispatch.book_a_ride.passenger_form import PassengerForm
from pages.ondemand.admin.dispatch.book_a_ride.recurring_rides.recurring_ride_form import (
    RecurringRideForm,
)
from pages.ondemand.admin.dispatch.book_a_ride.ride_form import RideForm
from pages.ondemand.admin.dispatch.book_a_ride.schedule_form import ScheduleForm
from utilities import Component, Selector, Selectors, WebElement


class RideBookingPanel(Component):
    """Objects and methods for the ride booking panel."""

    ROOT_LOCATOR: Selector = Selectors.data_id('book-a-ride-container')
    _book_a_ride_button: Selector = Selectors.data_id('book-a-ride-open')
    _close_book_a_ride_button: Selector = Selectors.data_id('book-a-ride-close')
    _submit_ride_button: Selector = Selectors.data_id('book-ride-button')

    @property
    def book_a_ride_button(self) -> WebElement:
        return self.container.find_element(*self._book_a_ride_button)

    @property
    def close_book_a_ride_button(self) -> WebElement:
        return self.container.find_element(*self._close_book_a_ride_button)

    @property
    def future_ride_form(self) -> FutureRideForm:
        return FutureRideForm(self)

    @property
    def passenger_form(self) -> PassengerForm:
        return PassengerForm(self)

    @property
    def recurring_ride_form(self) -> RecurringRideForm:
        return RecurringRideForm(self)

    @property
    def ride_form(self) -> RideForm:
        return RideForm(self)

    @property
    def schedule_form(self) -> ScheduleForm:
        return ScheduleForm(self)

    @property
    def submit_ride_button(self) -> WebElement:
        return self.container.find_element(*self._submit_ride_button)

    def open_book_a_ride_form(self) -> None:
        """Open the book a ride form, then check that the close element exists."""
        self.container.wait_until_visible(*self._book_a_ride_button)
        self.book_a_ride_button.click()

    def submit_ride_form(self) -> None:
        """Submit a ride form."""
        self.submit_ride_button.click()
