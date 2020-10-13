from datetime import date, timedelta

import pytest
from utilities.api_helpers.services import ServicesAPI
from utilities.constants.common import USERS
from utilities.factories.rides import RideFactory
from utilities.factories.services import ServiceFactory


@pytest.mark.factory
class TestRideFactory:
    """Battery of tests for RideFactory functionality."""

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that RideFactory values may be overridden post-build."""
        ride: dict = RideFactory.build()
        default_ride_status: str = ride['status']

        ride['status'] = 'In Progress'

        assert ride['status'] != default_ride_status

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__requires_no_params(self) -> None:
        """Check that the RideFactory build method does not require params."""
        ride: dict = RideFactory.build()

        assert ride is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__account_ride(self) -> None:
        """Check that an account ride is built from the RideFactory."""
        account_ride: dict = RideFactory.build(account_ride=True)

        assert (
            account_ride['rider']['username'] == USERS.USERNAME
            and account_ride['rider']['email'] == USERS.EMAIL
        )

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__future_ride(self) -> None:
        """Check that a future ride is built from the RideFactory."""
        future_ride: dict = RideFactory.build(future_ride=True)
        expected_pickup: str = future_ride['pickup']['timestamp']

        assert date.isoformat(date.today() + timedelta(days=1)) in expected_pickup

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__hub_ride(self) -> None:
        """Check that a hub ride is built from the RideFactory."""
        hub_ride: dict = RideFactory.build(hub_ride=True)

        assert hub_ride['pickup']['address'] == 'Stop #300 - TransLoc Office'

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__ride_with_note(self) -> None:
        """Check that a ride with note is built from the RideFactory."""
        ride_with_note: dict = RideFactory.build(ride_with_note=True)

        assert ride_with_note['note'] is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__same_day_future_ride(self) -> None:
        """Check that a same day future ride is built from the RideFactory."""
        same_day_future_ride: dict = RideFactory.build(same_day_future_ride=True)

        assert (
            date.isoformat(date.today() + timedelta(hours=3))
            in same_day_future_ride['pickup']['timestamp']
        )

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__returns_type_dict(self) -> None:
        """Check that a dictionary type is built from the RideFactory build method."""
        ride = RideFactory.build()

        assert type(ride) == dict

    @pytest.mark.high
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_ride(self) -> None:
        """Check that a new Ride is returned from the RideFactory build method."""
        ride_one: dict = RideFactory.build()
        ride_two: dict = RideFactory.build()

        assert ride_one != ride_two

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__returns_type_dict(self) -> None:
        """Check that a dictionary is created from the RideFactory create method."""
        services_api: ServicesAPI = ServicesAPI()
        service: dict = ServiceFactory.create()
        ride = RideFactory.create(service=service)

        assert type(ride) == dict

        services_api.delete_service(service)

    @pytest.mark.low
    @pytest.mark.unit
    def test_create__requires_service_param(self) -> None:
        """Check that the RideFactory create method requires a service param."""
        with pytest.raises(TypeError) as e:
            RideFactory.create()  # type: ignore
        assert "required positional argument: 'service'" in str(e.value)
