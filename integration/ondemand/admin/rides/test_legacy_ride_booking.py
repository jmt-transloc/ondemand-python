import factory
import pytest
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.legacy_rides.legacy_ride_booking import LegacyRideBooking
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestLegacyAsapRides:
    """Battery of tests for legacy ASAP ride booking functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ASAP ride testing."""
        self.details = Details(selenium)
        self.legacy_rides = LegacyRideBooking(selenium)
        self.rides = Rides(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking(self, ride_factory: factory, service: fixture) -> None:
        """Input valid ride information for an asap ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param service: Instantiation of a service.
        """
        ride: dict = ride_factory.build()
        rider = ride['rider']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.rides.visit()
        self.rides.navigate_to_legacy_ride_booking()
        self.legacy_rides.fill_ride_form(service, ride=ride)
        self.legacy_rides.submit_ride_form()

        assert self.details.info_card.ride_name == rider_name

    @pytest.mark.medium
    def test_booking__pay_fare(self, service_with_fare: fixture, ride_factory: factory) -> None:
        """Input valid ride info while paying for fare, then check for a success state.

        :param service_with_fare: Instantiation of a service with a fare.
        """
        ride: dict = ride_factory.build()

        self.rides.visit()
        self.rides.navigate_to_legacy_ride_booking()
        self.legacy_rides.fill_ride_form(service_with_fare, ride=ride)
        self.legacy_rides.pay_ride_fee(method='cash')
        self.legacy_rides.submit_ride_form()

        assert self.details.info_card.ride_fare == 'Fare: $2.00'

    @pytest.mark.medium
    def test_booking__waive_fare(self, service_with_fare: fixture, ride_factory: factory) -> None:
        """Input valid ride info while waiving fare, then check for a success state.

        :param service_with_fare: Instantiation of a service with a fare
        """
        ride: dict = ride_factory.build()

        self.rides.visit()
        self.rides.navigate_to_legacy_ride_booking()
        self.legacy_rides.fill_ride_form(service_with_fare, ride=ride)
        self.legacy_rides.pay_ride_fee(method='waive')
        self.legacy_rides.submit_ride_form()

        assert self.details.info_card.ride_fare == 'Fare paid on vehicle: $0.00'

    @pytest.mark.low
    def test_booking_with_note(self, ride_factory: factory, service: fixture) -> None:
        """Input valid ride info with a driver note, then check for the note after creation.

        :param service: Instantiation of a service.
        """
        ride_with_note: dict = ride_factory.build(note=fake.sentence(nb_words=3))
        note: str = ride_with_note['note']

        self.rides.visit()
        self.rides.navigate_to_legacy_ride_booking()
        self.legacy_rides.fill_ride_form(service, ride=ride_with_note)
        self.legacy_rides.submit_ride_form()

        assert self.details.info_card.ride_note == f'Note: {note}'
