import factory
import pytest
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestRideDetails:
    """Battery of tests for the ride Details page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ride Details testing."""
        self.details: Details = Details(selenium)
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_navigation(self, ride_factory: factory, service: fixture) -> None:
        """Navigate to the ride Details page for an existing ride.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        ride: dict = ride_factory.create(service=service)
        ride_id: str = ride['ride_id']

        self.rides.visit()
        self.rides.navigate_to_details_by_button(ride)

        assert ride_id in self.details.driver.current_url
