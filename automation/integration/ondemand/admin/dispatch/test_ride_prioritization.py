import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pytest import fixture
from utilities.api_helpers.rides import RidesAPI


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchRidePrioritization:
    """Battery of tests for prioritizing a ride from the Dispatch page."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in Dispatch ride prioritization testing."""
        self.rides_api: RidesAPI = RidesAPI()

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Dispatch ride prioritization testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.medium
    def test_ride_prioritization__pick_up(self, ride_factory: Factory, service: fixture) -> None:
        """Prioritize the pick up of a 'Pending' ride, then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)

        self.dispatch.visit()

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        card.open_kebab_menu()

        try:
            card.kebab_menu.open_ride_prioritization_modal()
        except AttributeError:
            pytest.xfail('Prioritization cannot be tested. Another ride is currently prioritized.')

        card.prioritization_modal.prioritize_ride('pick up')

        assert card.pick_up_prioritized() is not False

    @pytest.mark.medium
    def test_ride_prioritization__entire_ride(
        self, ride_factory: Factory, service: fixture,
    ) -> None:
        """Prioritize the entirety of a 'Pending' ride, then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)

        self.dispatch.visit()

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        card.open_kebab_menu()

        try:
            card.kebab_menu.open_ride_prioritization_modal()
        except AttributeError:
            pytest.xfail('Prioritization cannot be tested. Another ride is currently prioritized.')

        card.prioritization_modal.prioritize_ride('entire ride')

        assert card.entire_ride_prioritized() is not False

    @pytest.mark.medium
    def test_ride_prioritization__drop_off(self, ride_factory: Factory, service: fixture) -> None:
        """Prioritize the drop off of an 'In Progress' ride, then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        self.rides_api.start_ride(ride)

        self.dispatch.visit()

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        card.open_kebab_menu()

        try:
            card.kebab_menu.open_ride_prioritization_modal()
        except AttributeError:
            pytest.xfail('Prioritization cannot be tested. Another ride is currently prioritized.')

        card.prioritization_modal.prioritize_ride('drop off')

        assert card.drop_off_prioritized() is not False

    @pytest.mark.high
    @pytest.mark.smoke
    def test_multiple_rides_cannot_be_prioritized(
        self, ride_factory: Factory, service: fixture,
    ) -> None:
        """Prioritize a ride, attempt to prioritize another, then check for a failure state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride_one: dict = ride_factory.create(service=service)
        ride_two: dict = ride_factory.create(service=service)

        self.dispatch.visit()

        card_one: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride_one)
        card_one.open_kebab_menu()

        try:
            card_one.kebab_menu.open_ride_prioritization_modal()
        except AttributeError:
            pytest.xfail('Prioritization cannot be tested. Another ride is currently prioritized.')

        card_one.prioritization_modal.prioritize_ride('pick up')

        card_two: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride_two)
        card_two.open_kebab_menu()

        assert card_two.kebab_menu.prioritize_disabled() is not False
