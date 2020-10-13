import pytest
from pytest import fixture
from utilities.models.data_models import Ride, set_empty_list, set_ride_drop_off, set_ride_pick_up


@pytest.mark.model
@pytest.mark.unit
class TestRide:
    """Battery of tests for Ride data model functionality."""

    @pytest.fixture
    def valid_ride(self) -> Ride:
        """Create a valid Ride."""
        ride: Ride = Ride(
            rider={'first_name': 'Test', 'last_name': 'Rider', 'email': 'test@testing.com'},
        )

        yield ride

    @pytest.mark.low
    def test_build__override_default_values(self, valid_ride: fixture) -> None:
        """Check that default values may be overridden post-build."""
        ride: Ride = valid_ride
        ride.wheelchair = True

        assert ride.wheelchair is True

    @pytest.mark.low
    def test_build__requires_rider_param(self) -> None:
        """Check that the Ride data model requires a rider param."""
        with pytest.raises(TypeError) as e:
            Ride()  # type: ignore
        assert "required positional argument: 'rider'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_ride: fixture) -> None:
        """Check that building a ride sets default values."""
        ride: Ride = valid_ride

        assert (
            ride.service_type == 'ondemand'
            and ride.source == 'dispatcher'
            and ride.status == 'pending'
            and ride.capacity == 1
            and ride.wheelchair is False
        )

    @pytest.mark.low
    def test_build__set_drop_off(self, valid_ride: fixture) -> None:
        """Check that building a ride sets a drop off location."""
        ride: Ride = valid_ride

        assert ride.dropoff == set_ride_drop_off()

    @pytest.mark.low
    def test_build__set_empty_fields(self, valid_ride: fixture) -> None:
        """Check that building a ride sets empty lists."""
        ride: Ride = valid_ride

        assert ride.messages == set_empty_list()

    @pytest.mark.low
    def test_build__set_none_values(self, valid_ride: fixture) -> None:
        """Check that building a ride sets None values."""
        ride: Ride = valid_ride

        assert (
            ride.ride_id is None
            and ride.fare is None
            and ride.note is None
            and ride.service_id is None
            and ride.terminal_reason is None
        )

    @pytest.mark.low
    def test_build__set_pick_up(self, valid_ride: fixture) -> None:
        """Check that building a ride sets a pick up location."""
        ride: Ride = valid_ride

        assert ride.pickup == set_ride_pick_up()

    @pytest.mark.low
    def test_build__valid_input(self, valid_ride: fixture) -> None:
        """Build a ride with valid input."""
        ride: Ride = valid_ride

        assert ride.rider['first_name'] == 'Test' and ride.rider['last_name'] == 'Rider'

    @pytest.mark.low
    def test_model__features_full_rider_name(self, valid_ride: fixture) -> None:
        """Check that the Ride data model features a full rider name property."""
        ride: Ride = valid_ride

        assert ride.full_name == 'Test Rider'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        ride: Ride = Ride(
            rider={'first_name': 'Test', 'last_name': 'Rider', 'email': 'test@testing.com'},
            wheelchair=True,
        )

        assert ride.wheelchair is True
