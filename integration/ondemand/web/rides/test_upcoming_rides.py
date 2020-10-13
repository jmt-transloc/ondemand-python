import pytest
from pages.ondemand.web.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_web
@pytest.mark.ui
class TestUpcomingRides:
    """Battery of tests for Rides page upcoming rides functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in upcoming ride testing."""
        self.rides: Rides = Rides(selenium)

    @pytest.mark.low
    def test_rides_appear_in_my_rides(self, ride_factory: fixture, service: fixture) -> None:
        """Build an API ride, then check that the ride appears in the Upcoming tab."""
        ride: dict = ride_factory.create(account_ride=True, service=service)

        self.rides.visit()

        row = self.rides.rides_list.surface_ride_row(ride['ride_id'])
        assert row.ride_id == ride['ride_id']
