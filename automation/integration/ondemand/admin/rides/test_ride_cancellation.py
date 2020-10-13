import factory
import pytest
from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestRideCancellation:
    """Battery of tests for cancelling a ride from the Rides page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all data used in Rides page cancellation testing."""
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_cancel_ride(self, ride_factory: factory, service: fixture) -> None:
        """Cancel an existing ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        cancellation_reason: str = fake.sentence(nb_words=3)
        ride: dict = ride_factory.create(service=service)

        self.rides.visit()

        self.rides.cancel_ride(cancellation_reason, ride)

        row: RideRow = self.rides.single_rides_table.surface_ride_row(ride)
        assert row.ride_status == 'Canceled'
