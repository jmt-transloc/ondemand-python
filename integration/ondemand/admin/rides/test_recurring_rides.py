import pytest
from factory import Factory
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.rides.recurring_ride_table.subscription_row import SubscriptionRow
from pages.ondemand.admin.rides.ride_subscription_details_modal.scheduled_ride_row import (
    ScheduledRideRow,
)
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture
from utilities.api_helpers.recurring_rides import RecurringRidesAPI
from utilities.factories.fake import fake


class TestRecurringRides:
    """Battery of tests for the Rides page recurring rides functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Rides page recurring ride testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.API: RecurringRidesAPI = RecurringRidesAPI()
        self.details: Details = Details(selenium)
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_details_modal__cancel_all_rides(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then cancel all associated rides from its details modal.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

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
        row.kebab_menu.details_button.click()

        row.details_modal.cancel_all_rides(fake.text())

        assert row.details_modal.summary == '6 total trips: 1 canceled; 5 deleted'

    @pytest.mark.medium
    def test_details_modal__cancel_ride(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then cancel a booked ride from its details modal.

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
        row.kebab_menu.details_button.click()

        booked_ride: ScheduledRideRow = row.details_modal.scheduled_rides_list.scheduled_rides[0]
        booked_ride.cancel_ride(fake.text())

        assert row.details_modal.summary == '6 total trips: 1 canceled; 5 scheduled'

    @pytest.mark.medium
    def test_details_modal__delete_all_scheduled_rides(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Cancel a booked recurring ride, then delete all remaining rides from the details modal.

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
        row.kebab_menu.details_button.click()

        row.details_modal.delete_all_rides()

        assert row.details_modal.summary == '6 total trips: 1 canceled; 5 deleted'

    @pytest.mark.medium
    def test_details_modal__delete_ride(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then delete a scheduled ride from its details modal.

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
        row.kebab_menu.details_button.click()

        scheduled_ride: ScheduledRideRow = row.details_modal.scheduled_rides_list.scheduled_rides[1]
        scheduled_ride.delete_ride()

        assert scheduled_ride.status == 'DELETED'

    @pytest.mark.low
    def test_details_modal__booked_rides_feature_details_link(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Check that booked recurring rides feature a details page link.

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
        row.kebab_menu.details_button.click()

        booked_ride: ScheduledRideRow = row.details_modal.scheduled_rides_list.scheduled_rides[0]

        assert booked_ride.status == 'BOOKED' and booked_ride.details_link.visible

    @pytest.mark.low
    def test_kebab_menu__open_details_modal(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then open the Details modal from its kebab menu.

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
        row.kebab_menu.details_button.click()

        assert row.details_modal.visible

    @pytest.mark.medium
    def test_kebab_menu__delete_all_rides(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Cancel a booked recurring ride, then delete all remaining rides from its kebab menu.

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
    @pytest.mark.smoke
    def test_kebab_menu__cancel_all_rides(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then cancel all associated rides from its kebab menu.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

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

    @pytest.mark.low
    def test_ride_rows__row_features_ride_data(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, then verify its row matches ride data.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.create(service=service_with_recurring_rides)

        self.rides.visit()

        self.rides.sidebar.select_tab('Active')
        row: SubscriptionRow = self.rides.ride_subscription_table.surface_subscription_row(
            ride['ride_subscription_id'],
        )
        pickup: str = ride['ride']['pickup']['address']
        dropoff: str = ride['ride']['dropoff']['address']

        assert row.pick_up_address == pickup and row.drop_off_address == dropoff

    @pytest.mark.low
    def test_ride_rows__row_features_no_show_data(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, set a ride to 'No Show', then verify a success state.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.create(service=service_with_recurring_rides)
        self.API.set_no_show(ride)

        self.rides.visit()

        self.rides.sidebar.select_tab('Active')
        row: SubscriptionRow = self.rides.ride_subscription_table.surface_subscription_row(
            ride['ride_subscription_id'],
        )

        assert row.total_no_shows == '1 of 6'

    @pytest.mark.low
    def test_ride_rows__row_features_cancellation_data(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a recurring ride, set a ride to 'Cancelled', then verify a success state.

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

        assert row.total_cancels == '1 of 6'
