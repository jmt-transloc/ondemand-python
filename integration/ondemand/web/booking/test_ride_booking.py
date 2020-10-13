import pytest
from environs import Env
from pages.ondemand.web.booking.booking import Booking
from pytest import fixture
from utilities.models.data_models import Ride


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


@pytest.mark.ondemand_web
@pytest.mark.ui
class TestBookingAsapRides:
    """Battery of tests for Booking page ASAP ride booking functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ASAP ride testing."""
        self.booking: Booking = Booking(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking(self, ride_factory: fixture, service: fixture) -> None:
        """Input valid ride information for an asap ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        ride: Ride = ride_factory.build()

        self.booking.visit()

        if self.booking.agency_select_modal.loaded:
            self.booking.agency_select_modal.select_agency(AGENCY)

        if self.booking.service_select_modal.loaded:
            service_id = service['service_id']

            self.booking.service_select_modal.select_service_by_id(service_id)
        self.booking.pick_up_time_modal.submit_pickup_time()
        self.booking.fill_ride_form(ride)

        self.booking.ride_details_modal.submit_ride()

        assert (
            self.booking.ride_overview_modal.drop_off == ride.dropoff['address']
            and self.booking.ride_overview_modal.pick_up == ride.pickup['address']
        )
