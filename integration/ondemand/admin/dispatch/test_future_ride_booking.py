from datetime import datetime

import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchFutureRides:
    """Battery of tests for Dispatch page future ride booking functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in future ride testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)
        self.rides: Rides = Rides(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking__future_day(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Input valid ride information for a future next day ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service_with_in_advance: An in-advance service yielded by the API.
        """
        ride: dict = ride_factory.build(future_ride=True)
        rider: dict = ride['rider']
        ride_pickup: str = ride['pickup']['timestamp']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'
        ride_time: datetime = datetime.strptime(ride_pickup, '%Y-%m-%dT%H:%M:%S.%fZ')

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service=service_with_in_advance, ride=ride)
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('future')
        self.dispatch.fill_future_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        self.rides.visit()

        self.rides.filters.filter_by_date(ride_time.strftime('%m-%d-%Y'))

        row: RideRow = self.rides.single_rides_table.surface_ride_row(ride)
        assert row.ride_name == rider_name

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking__same_day__future_time(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Input valid ride information for a future same day ride, then check for success.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service_with_in_advance: An in-advance service yielded by the API.
        """
        ride: dict = ride_factory.build(same_day_future_ride=True)
        rider: dict = ride['rider']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service=service_with_in_advance, ride=ride)
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('future')
        self.dispatch.fill_future_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        self.dispatch.ride_filters.select_filter('Upcoming')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.rider_name == rider_name

    @pytest.mark.low
    def test_booking__with_note(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Create a valid future ride with driver note, then check for the note after creation.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service_with_in_advance: An in-advance service yielded by the API.
        """
        ride: dict = ride_factory.build(same_day_future_ride=True, ride_with_note=True)
        note: str = ride['note']

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service=service_with_in_advance, ride=ride)
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('future')
        self.dispatch.fill_future_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        self.dispatch.ride_filters.select_filter('Upcoming')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.note == f'Driver Note: {note}'

    @pytest.mark.low
    def test_future_rides_require_enabled_service(
        self, ride_factory: Factory, service: fixture,
    ) -> None:
        """Attempt to book with an non-future rides service, then check for an error state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: An non-in-advance service yielded by the API.
        """
        ride: dict = ride_factory.build()

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service, ride=ride)
        assert self.dispatch.ride_booking_panel.schedule_form.loaded is False

    @pytest.mark.low
    def test_same_day_rides_appear_in_upcoming_filter(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Create a valid same day future ride, then check upcoming rides for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service_with_in_advance: An in-advance service yielded by the API.
        """
        ride: dict = ride_factory.create(
            same_day_future_ride=True, service=service_with_in_advance,
        )
        rider: dict = ride['rider']
        rider_name: str = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('Upcoming')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.rider_name == rider_name
