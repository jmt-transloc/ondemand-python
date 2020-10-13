from typing import Generator

import pytest
from pytest import fixture
from requests import HTTPError
from utilities.api_helpers.vehicles import VehiclesAPI
from utilities.factories.vehicles import VehicleFactory


@pytest.mark.api
class TestVehiclesAPI:
    """Battery of tests for VehiclesAPI functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in VehiclesAPI testing."""
        self.api: VehiclesAPI = VehiclesAPI()

    @pytest.fixture
    def build_vehicle(self) -> Generator[dict, None, None]:
        """Build a Vehicle object for VehiclesAPI method testing.

        This vehicle should be used in testing API creation methods.
        """
        vehicle: dict = VehicleFactory.build()

        yield vehicle

    @pytest.fixture
    def create_vehicle(self) -> Generator[dict, None, None]:
        """Create a Vehicle object for VehiclesAPI method testing.

        This vehicle should be used in testing API deletion methods.
        """
        vehicle: dict = VehicleFactory.create()

        yield vehicle

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_vehicle__failure__invalid_input(self) -> None:
        """Check that the create_vehicle method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.api.create_vehicle(vehicle_data=111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_vehicle__failure__vehicle_data_required(self) -> None:
        """Check that the create_vehicle method fails without a vehicle_data param."""
        with pytest.raises(TypeError) as e:
            self.api.create_vehicle()  # type: ignore
        assert "required positional argument: 'vehicle_data'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_create_vehicle__success(self, build_vehicle: fixture) -> None:
        """Check that a Vehicle may be created.

        :param build_vehicle: A Vehicle object for testing.
        """
        try:
            self.api.create_vehicle(build_vehicle)
            self.api.delete_vehicle(build_vehicle)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create_vehicle__success__wheelchair_vehicle(self) -> None:
        """Check that a wheelchair Vehicle may be created."""
        vehicle_data: dict = VehicleFactory.build(wheelchair_vehicle=True)

        try:
            vehicle: dict = self.api.create_vehicle(vehicle_data)

            assert vehicle['wheelchair_capacity'] == 2 and vehicle['wheelchair_impact'] == 2

            self.api.delete_vehicle(vehicle)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create_vehicle__success__returns_type_dict(self, build_vehicle: fixture) -> None:
        """Check that the create_vehicle method returns a dictionary.

        :param build_vehicle: A Vehicle object for testing.
        """
        vehicle = self.api.create_vehicle(build_vehicle)

        assert type(vehicle) == dict

        self.api.delete_vehicle(vehicle)

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_vehicle__failure__invalid_input(self) -> None:
        """Check that the delete_vehicle method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.api.delete_vehicle(vehicle={'vehicle_id': 1})

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_vehicle__failure__region_required(self) -> None:
        """Check that the delete_vehicle method fails without a vehicle param."""
        with pytest.raises(TypeError) as e:
            self.api.delete_vehicle()  # type: ignore
        assert "required positional argument: 'vehicle'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_delete_vehicle__success(self, create_vehicle: fixture) -> None:
        """Check that a Vehicle may be deleted.

        :param create_vehicle: A Vehicle object for testing.
        """
        try:
            self.api.delete_vehicle(create_vehicle)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)
