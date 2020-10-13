from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.legacy_rides.legacy_ride_booking import LegacyRideBooking
from pages.ondemand.admin.rides.filters import Filters
from pages.ondemand.admin.rides.recurring_ride_table.ride_subscription_table import (
    RideSubscriptionTable,
)
from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from pages.ondemand.admin.rides.ride_tables.single_rides_table import SingleRidesTable
from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from pages.ondemand.common.navigation_tabs.tabs import Tabs
from utilities import Selector, Selectors, WebElement
from utilities.constants.ondemand import Admin


class Rides(Base):
    """Rides Page objects and methods for the OnDemand Admin application.

    The Rides Page features all pending, current, and completed rides for the selected agency. Rides
    may be filtered by service or by ride type (pending, requested, on vehicle, etc). Ride listings
    are further separated into Single Rides and Recurring Rides.
    """

    URL_PATH: str = f'{Base.URL_PATH}/rides'

    _booking_button: Selector = Selectors.data_id('new-button')
    _details_button: Selector = Selectors.data_id('details-button')

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def filters(self) -> Filters:
        return Filters(self)

    @property
    def sidebar(self) -> Tabs:
        return Tabs(
            self, tabs=[tab for tab in Admin.RIDES_TABS], selector='sidebar-navigation-container',
        )

    @property
    def ride_booking_button(self) -> WebElement:
        return self.driver.find_element(*self._booking_button)

    @property
    def ride_subscription_table(self) -> RideSubscriptionTable:
        return RideSubscriptionTable(self)

    @property
    def single_rides_table(self) -> SingleRidesTable:
        return SingleRidesTable(self)

    def cancel_ride(self, cancel_reason: str, ride: dict) -> None:
        """Cancel a ride that matches a ride object.

        :param cancel_reason: The required cancellation reason.
        :param ride: The ride yielded from a ride fixture.
        """
        row: RideRow = self.single_rides_table.surface_ride_row(ride)
        row.ride_cancel_button.click()

        self.cancellation_modal.cancel_ride(cancel_reason)

        row.container.wait_until_not_present(*Selectors.data_id('ride-cancel-button'), wait_time=4)

    def navigate_to_details_by_button(self, ride: dict) -> object:
        """Navigate to the Details page for a specific ride using the Details button.

        :param ride: The ride yielded from a ride fixture.
        """
        row = self.single_rides_table.surface_ride_row(ride)
        row.container.wait_until_visible(*Selectors.data_id('ride-details-button')).click()

        return Details(self.driver).wait_for_page_to_load()

    def navigate_to_details_by_ride_id(self, ride: dict) -> object:
        """Navigate to the Details Page for a specific ride using a direct URL.

        This is a useful method for bypassing the application work flows following creation of a
        ride using the API.

        :param ride: The ride yielded from a ride fixture.
        """
        ride_id: int = ride['ride_id']
        ride_url: str = f'{self.URL_PATH}/{ride_id}'
        self.driver.get(ride_url)

        return Details(self.driver, ride_url).wait_for_page_to_load()

    def navigate_to_legacy_ride_booking(self) -> object:
        """Navigate to the Legacy Ride Booking page."""
        self.ride_booking_button.click()

        return LegacyRideBooking(self.driver).wait_for_page_to_load()
