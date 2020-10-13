import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pytest import fixture
from utilities.api_helpers.rides import RidesAPI


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchRideFilters:
    """Battery of tests for Dispatch page ride filtering.

    Rides which have been flagged as 'Needs Attention' cannot be tested through automated means as
    manipulating the 'created_at' field defaults to the present time in UTC format. Therefore,
    testing 'Needs Attention' functionality will have to be manual only.
    """

    @pytest.fixture(autouse=True)
    def set_apis(self) -> None:
        """Instantiate all APIs used in ride filter testing."""
        self.rides_api: RidesAPI = RidesAPI()

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ride filter testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.medium
    def test_filters__upcoming(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Create a future same-day ride, select 'Upcoming', then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service_with_in_advance: An in-advance service yielded by the API.
        """
        future_ride: dict = ride_factory.create(
            same_day_future_ride=True, service=service_with_in_advance,
        )

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('Upcoming')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(future_ride)
        assert 'Requested' in card.ride_status

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_filters__complete__completed(self, ride_factory: Factory, service: fixture) -> None:
        """Create and complete a ride, select 'Complete', then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        self.rides_api.complete_ride(ride)

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('Complete')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'Completed'

    @pytest.mark.medium
    def test_filters__complete__cancelled(self, ride_factory: Factory, service: fixture) -> None:
        """Create and cancel a ride, select 'Complete', then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        self.rides_api.cancel_ride(ride)

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('Complete')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'Canceled'

    @pytest.mark.medium
    def test_filters__in_progress__pending(self, ride_factory: Factory, service: fixture) -> None:
        """Create a ride, select 'In Progress', then check for a success state.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('In Progress')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'Pending Vehicle Assignment'

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_filters__in_progress__on_vehicle(
        self, ride_factory: Factory, service: fixture,
    ) -> None:
        """Create a ride, place it onto a vehicle, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)
        self.rides_api.start_ride(ride)

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('In Progress')
        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'On Vehicle'
