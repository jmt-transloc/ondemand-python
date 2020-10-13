import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pytest import fixture
from utilities.api_helpers.rides import RidesAPI
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestDispatchCancellation:
    """Battery of tests for cancelling a ride from the Dispatch page."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in Dispatch page cancellation testing."""
        self.rides_api: RidesAPI = RidesAPI()

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Dispatch page cancellation testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_cancel_ride__asap(self, ride_factory: Factory, service: fixture) -> None:
        """Cancel an existing ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        cancellation_reason: str = fake.sentence(nb_words=3)
        ride: dict = ride_factory.create(service=service)

        self.dispatch.visit()

        self.dispatch.cancel_ride(cancel_reason=cancellation_reason, ride=ride)
        self.dispatch.ride_filters.select_filter('Complete')

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'Canceled'

    @pytest.mark.medium
    def test_cancel_ride__upcoming(
        self, ride_factory: Factory, service_with_in_advance: fixture,
    ) -> None:
        """Cancel an upcoming ride, then check for a success state."""
        cancellation_reason: str = fake.sentence(nb_words=3)
        ride: dict = ride_factory.create(
            same_day_future_ride=True, service=service_with_in_advance,
        )

        self.dispatch.visit()

        self.dispatch.ride_filters.select_filter('Upcoming')
        self.dispatch.cancel_ride(cancel_reason=cancellation_reason, ride=ride)
        self.dispatch.ride_filters.select_filter('Complete')

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.ride_status == 'Canceled'

    @pytest.mark.high
    @pytest.mark.smoke
    def test_in_progress_rides_cannot_cancel(self, ride_factory: Factory, service: fixture) -> None:
        """Progress a ride to 'On Vehicle', attempt to cancel, then check for a failure state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        ride: dict = ride_factory.create(service=service)
        self.rides_api.start_ride(ride)

        self.dispatch.visit()

        card: RideCard = self.dispatch.ride_card_panel.surface_ride_card(ride)
        card.open_kebab_menu()

        assert card.kebab_menu.cancel_ride_button is None
