import pytest
from factory import Factory
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.role_admin
@pytest.mark.ui
class TestAdminPermissions:
    """Battery of tests for Admin role permissions on the Rides page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Admin role Rides page testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    def test_recurring_rides__access(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """As an Admin, check to ensure that recurring rides are available for view.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        recurring_ride_factory.create(service=service_with_recurring_rides)

        self.rides.visit()

        self.rides.sidebar.container.is_text_visible('Recurring Rides')
        assert 'Recurring Rides' in self.rides.sidebar.container.html
