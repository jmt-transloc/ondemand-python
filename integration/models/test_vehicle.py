import pytest
from pytest import fixture
from utilities.models.data_models import set_vehicle_color, Vehicle


@pytest.mark.model
@pytest.mark.unit
class TestVehicle:
    """Battery of tests for Vehicle data model functionality."""

    @pytest.fixture
    def valid_vehicle(self) -> Vehicle:
        """Create a valid Vehicle."""
        vehicle: Vehicle = Vehicle(call_name='Testing Vehicle')

        yield vehicle

    @pytest.mark.low
    def test_build__override_default_values(self, valid_vehicle: fixture) -> None:
        """Check that default values may be overridden post-build.

        :param valid_vehicle: A valid Vehicle object for testing.
        """
        valid_vehicle.call_name = 'New Vehicle'

        assert valid_vehicle.call_name == 'New Vehicle'

    @pytest.mark.low
    def test_build__requires_call_name_param(self) -> None:
        """Check that the Vehicle data model requires a call_name param."""
        with pytest.raises(TypeError) as e:
            Vehicle()  # type: ignore
        assert "required positional argument: 'call_name'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_vehicle: fixture) -> None:
        """Check that the Vehicle data model sets default values.

        :param valid_vehicle: A valid Vehicle object for testing.
        """
        assert (
            valid_vehicle.capacity == 1
            and valid_vehicle.eligible is True
            and valid_vehicle.enabled is True
            and valid_vehicle.wheelchair_capacity == 0
            and valid_vehicle.wheelchair_impact == 1
        )

    @pytest.mark.low
    def test_build__set_none_values(self, valid_vehicle: fixture) -> None:
        """Check that the Vehicle data model sets None values.

        :param valid_vehicle: A valid Vehicle object for testing.
        """
        assert valid_vehicle.vehicle_id is None

    @pytest.mark.low
    def test_build__set_vehicle_color(self, valid_vehicle: fixture) -> None:
        """Check that the Vehicle data model sets a vehicle color.

        :param valid_vehicle: A valid Vehicle object for testing.
        """
        assert valid_vehicle.color == set_vehicle_color() and set_vehicle_color() == '1e88e5'

    @pytest.mark.low
    def test_build__valid_input(self, valid_vehicle: fixture) -> None:
        """Build a Vehicle with valid input.

        :param valid_vehicle: A valid Vehicle object for testing.
        """
        assert valid_vehicle.call_name == 'Testing Vehicle'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        vehicle: Vehicle = Vehicle(call_name='Testing', enabled=False, capacity=10)

        assert (
            vehicle.call_name == 'Testing' and vehicle.enabled is False and vehicle.capacity == 10
        )
