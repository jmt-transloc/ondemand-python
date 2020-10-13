import pytest
from factory import Factory
from pages.ondemand.admin.rides.recurring_ride_table.subscription_row import SubscriptionRow
from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture
from utilities.api_helpers.recurring_rides import RecurringRidesAPI
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.role_dispatcher
@pytest.mark.ui
class TestDispatcherPermissions:
    """Battery of tests for Dispatcher role permissions on the Rides page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Dispatcher role Rides page testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.API: RecurringRidesAPI = RecurringRidesAPI()
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    def test_recurring_rides__access(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """As a Dispatcher, check to ensure that recurring rides are available for view.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        recurring_ride_factory.create(service=service_with_recurring_rides)

        self.rides.visit()

        self.rides.sidebar.container.is_text_visible('Recurring Rides')
        assert 'Recurring Rides' in self.rides.sidebar.container.html

    @pytest.mark.medium
    def test_update_rides__cancel(self, ride_factory: Factory, service: fixture) -> None:
        """As a Dispatcher, check to ensure that rides may be cancelled."""
        cancellation_reason: str = fake.sentence(nb_words=3)
        ride: dict = ride_factory.create(service=service)

        self.rides.visit()

        self.rides.cancel_ride(cancellation_reason, ride)

        row: RideRow = self.rides.single_rides_table.surface_ride_row(ride)
        assert row.ride_status == 'Canceled'

    @pytest.mark.medium
    def test_update_recurring_rides__delete_all(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """As a Dispatcher, check to ensure that recurring rides may be deleted.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.create(service=service_with_recurring_rides)
        self.API.cancel_booked_ride(ride)

        self.rides.visit()

        self.rides.sidebar.select_tab('Active')
        row: SubscriptionRow = self.rides.ride_subscription_table.surface_subscription_row(
            ride['ride_subscription_id'],
        )
        row.open_kebab_menu()
        row.kebab_menu.cancel_all_button.click()

        row.deletion_modal.confirm_button.click()

        assert row.total_cancels == '1 of 6'

    @pytest.mark.medium
    def test_update_recurring_rides__cancel_all(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """As a Dispatcher, check to ensure that recurring rides may be cancelled.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.create(service=service_with_recurring_rides)

        self.rides.visit()

        self.rides.sidebar.select_tab('Active')
        row: SubscriptionRow = self.rides.ride_subscription_table.surface_subscription_row(
            ride['ride_subscription_id'],
        )
        row.open_kebab_menu()
        row.kebab_menu.cancel_all_button.click()

        row.cancellation_modal.cancel_ride(fake.text())
        assert row.total_cancels == '1 of 6'
