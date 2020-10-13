import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchAsapRides:
    """Battery of tests for Dispatch page ASAP ride booking functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ASAP ride testing."""
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking(self, ride_factory: Factory, service: fixture) -> None:
        """Input valid ride information for an asap ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.build()
        rider: dict = ride['rider']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service, ride=ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        card = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.rider_name == rider_name

    @pytest.mark.low
    def test_booking__with_note(self, ride_factory: Factory, service: fixture) -> None:
        """Create a valid ride with driver note, then check for the note after creation.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.build(ride_with_note=True)
        note: str = ride['note']

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service, ride=ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.note == f'Driver Note: {note}'
