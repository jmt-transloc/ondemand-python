import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchRiderSearch:
    """Battery of tests for Dispatch page rider search."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in rider search testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.low
    def test_rider_search__name(self, ride_factory: Factory, service: fixture) -> None:
        """Create a ride and find it by searching the rider's name.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        rider: dict = ride['rider']
        ride_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()

        self.dispatch.rider_search.fill_search_field(input_type='name', ride=ride)

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.rider_name == ride_name

    @pytest.mark.low
    def test_rider_search__email(self, ride_factory: Factory, service: fixture) -> None:
        """Create a ride and find it by searching the rider's email.

        account_ride=True is passed to indicate the use of an existing rider account.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service, superuser_account_ride=True)
        rider: dict = ride['rider']
        ride_email = f'{rider["email"]}'

        self.dispatch.visit()

        self.dispatch.rider_search.fill_search_field(input_type='email', ride=ride)

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.email == ride_email

    @pytest.mark.low
    def test_rider_search__phone_number(self, ride_factory: Factory, service: fixture) -> None:
        """Create a ride and find it by searching the rider's phone number.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        rider: dict = ride['rider']
        ride_phone = f'{rider["phone"]}'

        self.dispatch.visit()

        self.dispatch.rider_search.fill_search_field(input_type='phone', ride=ride)

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.phone == ride_phone
