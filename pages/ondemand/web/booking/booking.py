from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from pages.ondemand.web.agency.agency_select.agency_select import AgencySelectModal
from pages.ondemand.web.base.base import Base
from pages.ondemand.web.booking.book_a_ride.address_input import AddressInput
from pages.ondemand.web.booking.book_a_ride.passenger_details_modal import PassengerDetailsModal
from pages.ondemand.web.booking.book_a_ride.ride_details_modal import RideDetailsModal
from pages.ondemand.web.booking.book_a_ride.ride_overview_modal import RideOverviewModal
from pages.ondemand.web.booking.book_a_ride.ride_share_modal import RideShareModal
from pages.ondemand.web.booking.pickup_time_modal.pickup_time_modal import PickupTimeModal
from pages.ondemand.web.booking.service_select.service_select_modal import ServiceSelectModal
from utilities import Selector, Selectors
from utilities.models.data_models import Ride


class Booking(Base):
    """Objects and methods for the Booking page.

    The booking page may be accessed by selecting the 'Book a Ride' tab from any location
    within the OnDemand Web application.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-request-page-container')

    @property
    def address_input(self) -> AddressInput:
        return AddressInput(self)

    @property
    def agency_select_modal(self) -> AgencySelectModal:
        return AgencySelectModal(self)

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def passenger_details_modal(self) -> PassengerDetailsModal:
        return PassengerDetailsModal(self)

    @property
    def pick_up_time_modal(self) -> PickupTimeModal:
        return PickupTimeModal(self)

    @property
    def ride_details_modal(self) -> RideDetailsModal:
        return RideDetailsModal(self)

    @property
    def ride_overview_modal(self) -> RideOverviewModal:
        return RideOverviewModal(self)

    @property
    def ride_share_modal(self) -> RideShareModal:
        return RideShareModal(self)

    @property
    def service_select_modal(self) -> ServiceSelectModal:
        return ServiceSelectModal(self)

    def fill_ride_form(self, ride: Ride) -> None:
        """Fill out the Booking page ride form.

        :param ride: The ride yielded from a ride fixture.
        """
        self.address_input.select_pick_up_location(ride.pickup['address'])
        self.address_input.select_drop_off_location(ride.dropoff['address'])

        self.passenger_details_modal.next_button.click()
        self.ride_share_modal.check_for_modal()
