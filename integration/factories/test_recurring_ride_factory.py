from datetime import date, timedelta
from typing import Generator

import pytest
from pytest import fixture
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.recurring_rides import RecurringRideFactory
from utilities.factories.services import ServiceFactory


@pytest.mark.factory
class TestRecurringRideFactory:
    """Battery of tests for RecurringRideFactory functionality."""

    @pytest.fixture
    def service(self) -> Generator[dict, None, None]:
        """Instantiate a recurring ride service."""
        services_api: ServicesAPI = ServicesAPI()
        service: dict = ServiceFactory.create(recurring_ride_service=True)

        yield service

        services_api.delete_service(service)

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__generate_ride_object(self) -> None:
        """Check that the RecurringRideFactory build method generates a ride object."""
        ride: dict = RecurringRideFactory.build()

        assert ride['ride'] is not None

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__generate_rides_list(self) -> None:
        """Check that the RecurringRideFactory build method generates a rides list."""
        ride: dict = RecurringRideFactory.build()

        assert ride['rides'] is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that RecurringRideFactory values may be overridden post-build."""
        ride: dict = RecurringRideFactory.build()
        default_ride_status: str = ride['ride']['status']
        ride['ride']['status'] = 'In Progress'

        assert ride['ride']['status'] != default_ride_status

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__future_recurring_ride(self) -> None:
        """Check that a future recurring ride is built from the RecurringRideFactory."""
        future_ride: dict = RecurringRideFactory.build(future_recurring_ride=True)
        expected_pickup: str = future_ride['ride']['pickup']['timestamp']

        assert date.isoformat(date.today() + timedelta(days=1)) in expected_pickup

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__ride_with_note(self) -> None:
        """Check that a ride with note is built from the RecurringRideFactory."""
        ride_with_note: dict = RecurringRideFactory.build(ride_with_note=True)

        assert ride_with_note['ride']['note'] is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__same_day_future_ride(self) -> None:
        """Check that a same day future recurring ride is built from the RecurringRideFactory."""
        same_day_future_ride: dict = RecurringRideFactory.build(same_day_future_recurring_ride=True)

        assert (
            date.isoformat(date.today() + timedelta(hours=3))
            in same_day_future_ride['ride']['pickup']['timestamp']
        )

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__requires_no_params(self) -> None:
        """Check that the RecurringRideFactory build method does not require params."""
        ride: dict = RecurringRideFactory.build()

        assert ride is not None

    @pytest.mark.high
    @pytest.mark.unit
    def test_build__returns_type_recurring_dict(self) -> None:
        """Check that a dictionary type is built from the RecurringRideFactory build method."""
        ride = RecurringRideFactory.build()

        assert type(ride) == dict

    @pytest.mark.high
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_recurring_ride(self) -> None:
        """Check that a new RecurringRide is returned from the RideFactory build method."""
        ride_one: dict = RecurringRideFactory.build()
        ride_two: dict = RecurringRideFactory.build()

        assert ride_one != ride_two

    @pytest.mark.high
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_ride_object(self) -> None:
        """Check that a new ride object is returned from the RideFactory build method."""
        ride_one: dict = RecurringRideFactory.build()
        ride_two: dict = RecurringRideFactory.build()

        assert ride_one['ride'] != ride_two['ride']

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__params__future_recurring_ride(self, service: fixture) -> None:
        """Check that a future recurring ride is created from the RecurringRideFactory.

        :param service: A recurring ride service.
        """
        ride = RecurringRideFactory.create(service=service, future_recurring_ride=True)
        expected_pickup: str = ride['ride']['pickup']['timestamp']

        assert date.isoformat(date.today() + timedelta(days=1)) in expected_pickup

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__params__ride_with_note(self, service: fixture) -> None:
        """Check that a ride with note is created from the RecurringRideFactory.

        :param service: A recurring ride service.
        """
        ride: dict = RecurringRideFactory.create(service=service, ride_with_note=True)

        assert ride['ride']['note'] is not None

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__params__same_day_future_ride(self, service: fixture) -> None:
        """Check that a same day future recurring ride is created from the RecurringRideFactory.

        :param service: A recurring ride service.
        """
        ride: dict = RecurringRideFactory.create(
            service=service, same_day_future_recurring_ride=True,
        )
        expected_pickup: str = ride['ride']['pickup']['timestamp']

        assert date.isoformat(date.today() + timedelta(hours=3)) in expected_pickup

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__returns_type_dict(self, service: fixture) -> None:
        """Check that a dictionary is created from the RecurringRideFactory.

        :param service: A recurring ride service.
        """
        ride: dict = RecurringRideFactory.create(service=service)

        assert type(ride) == dict

    @pytest.mark.low
    @pytest.mark.unit
    def test_create__requires_service_param(self) -> None:
        """Check that the RecurringRideFactory create method requires a service param."""
        with pytest.raises(TypeError) as e:
            RecurringRideFactory.create()  # type: ignore
        assert "required positional argument: 'service'" in str(e.value)
