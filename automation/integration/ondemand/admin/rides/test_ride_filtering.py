from typing import List

import pytest
from factory import Factory
from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture
from utilities.api_helpers.services import ServicesAPI


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestRideFiltering:
    """Battery of tests for Rides page filtering inputs."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all data used in Rides page filter testing."""
        self.rides: Rides = Rides(selenium)
        self.services_API: ServicesAPI = ServicesAPI()

    @pytest.mark.low
    def test_filter_by_rider_name(self, ride_factory: Factory, service: fixture) -> None:
        """Input a rider name to the filter field, then check for a success state."""
        ride: dict = ride_factory.create(service=service)
        rider_info: dict = ride['rider']
        rider_name: str = f'{rider_info["first_name"]} {rider_info["last_name"]}'

        self.rides.visit()
        self.rides.filters.filter_by_ride_info(rider_name)
        rows: List[RideRow] = self.rides.single_rides_table.ride_rows

        assert len(rows) == 1

    @pytest.mark.low
    @pytest.mark.parametrize('destination', ['pickup', 'dropoff'])
    def test_filter_by_destination(
        self, destination: str, ride_factory: Factory, service: fixture,
    ) -> None:
        """Input a destination to the filter field, then check for a success state.

        Parametrization is used in order to test for both pick up and drop off scenarios.
        """
        ride: dict = ride_factory.create(service=service)
        ride_destination: str = ride[destination]['address']

        self.rides.visit()
        self.rides.filters.filter_by_ride_info(ride_destination)
        row: RideRow = self.rides.single_rides_table.surface_ride_row(ride)

        assert row.visible is True

    @pytest.mark.low
    def test_filter_by_service(self, ride_factory: Factory, service_factory: Factory) -> None:
        """Check a service within the service filter field, then check for a success state.

        This test constructs two separate services and rides in order to ensure that the core
        functionality can be tested in earnest. Both services are manually torn down at the
        end of this test.
        """
        service_one: dict = service_factory.create()
        service_two: dict = service_factory.create()
        ride: dict = ride_factory.create(service=service_one)
        ride_factory.create(service=service_two)

        self.rides.visit()

        self.rides.filters.filter_service_by_id(service_one['service_id'])
        row: RideRow = self.rides.single_rides_table.surface_ride_row(ride)

        assert row is None

        self.services_API.delete_service(service_one)
        self.services_API.delete_service(service_two)
