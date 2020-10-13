import pytest
from utilities.api_helpers.vehicles import VehiclesAPI
from utilities.factories.vehicles import VehicleFactory


@pytest.mark.factory
class TestVehicleFactory:
    """Battery of tests for VehicleFactory functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs for VehicleFactory testing."""
        self.api: VehiclesAPI = VehiclesAPI()

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that VehicleFactory values may be overridden post-build."""
        vehicle: dict = VehicleFactory.build()
        default_vehicle_name: str = vehicle['call_name']
        vehicle['call_name'] = 'Test Vehicle'

        assert vehicle['call_name'] != default_vehicle_name

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__params__wheelchair_vehicle(self) -> None:
        """Check that the VehicleFactory build method generates wheelchair vehicles."""
        vehicle: dict = VehicleFactory.build(wheelchair_vehicle=True)

        assert vehicle['wheelchair_capacity'] == 2 and vehicle['wheelchair_impact'] == 2

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__requires_no_params(self) -> None:
        """Check that the VehicleFactory build method does not require params."""
        vehicle: dict = VehicleFactory.build()

        assert vehicle is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__returns_type_dict(self) -> None:
        """Check that the VehicleFactory build method returns a dictionary."""
        vehicle = VehicleFactory.build()

        assert type(vehicle) == dict

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_vehicle(self) -> None:
        """Check that a new Vehicle is returned from the VehicleFactory build method."""
        vehicle_one: dict = VehicleFactory.build()
        vehicle_two: dict = VehicleFactory.build()

        assert vehicle_one != vehicle_two

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__params__wheelchair_vehicle(self) -> None:
        """Check that the VehicleFactory create method generates wheelchair vehicles."""
        vehicle: dict = VehicleFactory.create(wheelchair_vehicle=True)

        assert vehicle['wheelchair_capacity'] == 2 and vehicle['wheelchair_impact'] == 2

        self.api.delete_vehicle(vehicle)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__returns_type_dict(self) -> None:
        """Check that the VehicleFactory create method returns a dictionary."""
        vehicle: dict = VehicleFactory.create()

        assert type(vehicle) == dict

        self.api.delete_vehicle(vehicle)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__requires_no_params(self) -> None:
        """Check that the VehicleFactory create method does not require params."""
        vehicle: dict = VehicleFactory.create()

        assert vehicle is not None

        self.api.delete_vehicle(vehicle)
