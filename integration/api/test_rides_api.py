from typing import Generator

import pytest
from pytest import fixture
from requests import HTTPError
from utilities.api_helpers.rides import RidesAPI
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.rides import RideFactory
from utilities.factories.services import ServiceFactory


@pytest.mark.api
class TestRidesAPI:
    """Batter of tests for RidesAPI functionality."""

    @pytest.fixture
    def ride(self) -> Generator[dict, None, None]:
        """Instantiate a ride for RidesAPI method testing."""
        service: dict = ServiceFactory()
        ride: dict = RideFactory(service=service)

        yield ride

        self.services_api.delete_service(service)

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in RidesAPI testing."""
        self.rides_api: RidesAPI = RidesAPI()
        self.services_api: ServicesAPI = ServicesAPI()

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_ride__failure__invalid_input(self) -> None:
        """Check that the cancel_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.rides_api.cancel_ride(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_ride__failure__ride_required(self) -> None:
        """Check that the cancel_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.cancel_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_cancel_ride__success(self, ride: fixture) -> None:
        """Check that a ride status may be changed to 'Canceled'."""
        try:
            self.rides_api.cancel_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__invalid_input(self) -> None:
        """Check that the change_ride_status method fails with invalid input."""
        with pytest.raises(TypeError):
            self.rides_api.change_ride_status(ride=1111111, status='testing')  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__ride_required(self) -> None:
        """Check that the change_ride_status method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.change_ride_status(status='Canceled')  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__status_required(self) -> None:
        """Check that the change_ride_status method fails without a status param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.change_ride_status(ride={})  # type: ignore
        assert "required positional argument: 'status'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_change_ride_status__success(self, ride: fixture) -> None:
        """Check that a ride status may be changed successfully."""
        try:
            self.rides_api.change_ride_status(ride=ride, status='Canceled')
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_complete_ride__failure__invalid_input(self) -> None:
        """Check that the complete_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.rides_api.complete_ride(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_complete_ride__failure__ride_required(self) -> None:
        """Check that the complete_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.complete_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_complete_ride__success(self, ride: fixture) -> None:
        """Check that a ride status may be changed to 'Completed'."""
        try:
            self.rides_api.complete_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_ride__failure__invalid_input(self) -> None:
        """Check that the create_ride method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.rides_api.create_ride(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_ride__failure__ride_data_required(self) -> None:
        """Check that the create_ride method fails without a ride_data param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.create_ride()  # type: ignore
        assert "required positional argument: 'ride_data'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_create_ride__success(self) -> None:
        """Check that a ride may be created."""
        service: dict = ServiceFactory()
        ride_data: dict = RideFactory.build(service_id=service['service_id'])

        try:
            self.rides_api.create_ride(ride_data)
            self.services_api.delete_service(service)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_start_ride__failure__invalid_input(self) -> None:
        """Check that the start_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.rides_api.start_ride(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_start_ride__failure__ride_required(self) -> None:
        """Check that the start_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.rides_api.start_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_start_ride__success(self, ride: fixture) -> None:
        """Check that a ride status may be changed to 'In Progress'."""
        try:
            self.rides_api.start_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')
