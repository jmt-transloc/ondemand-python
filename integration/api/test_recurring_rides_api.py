from typing import Generator

import pytest
from pytest import fixture
from requests import HTTPError
from utilities.api_helpers.recurring_rides import RecurringRidesAPI
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.recurring_rides import RecurringRideFactory
from utilities.factories.rides import RideFactory
from utilities.factories.services import ServiceFactory


@pytest.mark.api
class TestRecurringRidesAPI:
    """Battery of tests for RecurringRidesAPI helper functionality."""

    @pytest.fixture
    def ride(self) -> Generator[dict, None, None]:
        """Instantiate a recurring ride for RecurringRidesAPI method testing."""
        service: dict = ServiceFactory.create(recurring_ride_service=True)
        ride: dict = RecurringRideFactory.create(service=service)

        yield ride

        self.services_api.delete_service(service)

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in RecurringRidesAPI testing."""
        self.recurring_rides_api: RecurringRidesAPI = RecurringRidesAPI()
        self.services_api: ServicesAPI = ServicesAPI()

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_booked_ride__failure__invalid_input(self) -> None:
        """Check that the cancel_booked_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.recurring_rides_api.cancel_booked_ride(1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_booked_ride__failure__ride_required(self) -> None:
        """Check that the cancel_booked_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.cancel_booked_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_cancel_booked_ride__success(self, ride: fixture) -> None:
        """Check that a booked recurring ride status may be changed to 'Canceled'.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.cancel_booked_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_recurring_ride__failure__invalid_input(self) -> None:
        """Check that the cancel_recurring_ride method fails with invalid input."""
        with pytest.raises(KeyError) as e:
            self.recurring_rides_api.cancel_recurring_ride(recurring_ride={})  # type: ignore
        assert 'ride_subscription_id' in str(e.value)

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_recurring_ride__failure__invalid_id(self) -> None:
        """Check that the cancel_recurring_ride method fails with invalid ID input."""
        with pytest.raises(HTTPError):
            self.recurring_rides_api.cancel_recurring_ride({'ride_subscription_id': 1})

    @pytest.mark.low
    @pytest.mark.unit
    def test_cancel_recurring_ride__failure__ride_required(self) -> None:
        """Check that the cancel_recurring_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.cancel_recurring_ride()  # type: ignore
        assert "required positional argument: 'recurring_ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_cancel_recurring_ride__success(self, ride: fixture) -> None:
        """Check that a recurring ride subscription may be cancelled.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.cancel_recurring_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__invalid_input(self) -> None:
        """Check that the change_ride_status method fails with invalid input."""
        with pytest.raises(TypeError):
            self.recurring_rides_api.change_ride_status(ride=11111, status='testing')  # type: ignore  # noqa: E501

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__ride_required(self) -> None:
        """Check that the change_ride_status method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.change_ride_status(status='testing')  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.low
    @pytest.mark.unit
    def test_change_ride_status__failure__status_required(self) -> None:
        """Check that the change_ride_status method fails without a status param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.change_ride_status(ride={})  # type: ignore
        assert "required positional argument: 'status'" in str(e.value)

    @pytest.mark.medium
    @pytest.mark.integration
    def test_change_ride_status__failure__invalid_status(self, ride: fixture) -> None:
        """Check that the change_ride_status method fails with an invalid status param.

        :param ride: A recurring ride for testing.
        """
        with pytest.raises(HTTPError):
            self.recurring_rides_api.change_ride_status(ride=ride, status='testing')

    @pytest.mark.high
    @pytest.mark.integration
    def test_change_ride_status__success(self, ride: fixture) -> None:
        """Check that a recurring ride status may be changed.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.change_ride_status(ride=ride, status='Canceled')
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_complete_ride__failure__invalid_input(self) -> None:
        """Check that the complete_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.recurring_rides_api.complete_ride(1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_complete_ride__failure__ride_required(self) -> None:
        """Check that the complete_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.complete_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_complete_ride__success(self, ride: fixture) -> None:
        """Check that a booked recurring ride status may be changed to 'Complete'.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.complete_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_recurring_ride__failure__invalid_input(self) -> None:
        """Check that the create_recurring_ride method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.recurring_rides_api.create_recurring_ride(1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_recurring_ride__failure__requires_ride_data(self) -> None:
        """Check that the create_recurring_ride method requires a ride_data param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.create_recurring_ride()  # type: ignore
        assert "required positional argument: 'ride_data'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_create_recurring_ride__success(self) -> None:
        """Check that a recurring ride may be created."""
        service: dict = ServiceFactory.create(recurring_ride_service=True)
        ride_data: dict = RecurringRideFactory.build(
            ride=RideFactory.build(service_id=service['service_id']),
        )

        try:
            self.recurring_rides_api.create_recurring_ride(ride_data)
            self.services_api.delete_service(service)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_set_no_show_ride__failure__invalid_input(self) -> None:
        """Check that the set_no_show_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.recurring_rides_api.set_no_show(1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_set_no_show_ride__failure__ride_required(self) -> None:
        """Check that the set_no_show_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.set_no_show()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_set_no_show_ride__success(self, ride: fixture) -> None:
        """Check that a booked recurring ride status may be changed to 'No Show'.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.set_no_show(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.unit
    def test_start_ride__failure__invalid_input(self) -> None:
        """Check that the start_ride method fails with invalid input."""
        with pytest.raises(TypeError):
            self.recurring_rides_api.start_ride(1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_start_ride__failure__ride_required(self) -> None:
        """Check that the start_ride method fails without a ride param."""
        with pytest.raises(TypeError) as e:
            self.recurring_rides_api.start_ride()  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_start_ride__success(self, ride: fixture) -> None:
        """Check that a booked recurring ride status may be changed to 'In Progress'.

        :param ride: A recurring ride for testing.
        """
        try:
            self.recurring_rides_api.start_ride(ride)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)
