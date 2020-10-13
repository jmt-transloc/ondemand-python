from datetime import date, timedelta

import pytest
from pytest import fixture
from utilities.models.data_models import (
    Service,
    set_empty_list,
    set_service_regions,
    set_service_vehicle,
)


@pytest.mark.model
@pytest.mark.unit
class TestService:
    """Battery of tests for Service data model functionality."""

    @pytest.fixture
    def valid_service(self) -> Service:
        """Create a valid Service."""
        service: Service = Service(name='Testing Service')

        yield service

    @pytest.mark.low
    def test_build__override_default_values(self, valid_service: fixture) -> None:
        """Check that default values may be overridden post-build."""
        service: Service = valid_service
        service.recurring_rides_enabled = True

        assert service.recurring_rides_enabled is True

    @pytest.mark.low
    def test_build__requires_name_param(self) -> None:
        """Attempt to build a new service without entering params."""
        with pytest.raises(TypeError) as e:
            Service()  # type: ignore
        assert "required positional argument: 'name'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_service: fixture) -> None:
        """Check that building a service sets default values."""
        service: Service = valid_service

        assert (
            service.friday is True
            and service.monday is True
            and service.saturday is True
            and service.sunday is True
            and service.thursday is True
            and service.tuesday is True
            and service.wednesday is True
            and service.color == '1e88e5'
            and service.end_time == 86340
            and service.fare_required is False
            and service.in_advance_enabled is False
            and service.managed_mode is False
            and service.max_capacity == 10
            and service.on_demand_enabled is True
            and service.recurring_rides_enabled is False
            and service.rider_restricted is False
            and service.shibboleth_restricted is False
            and service.start_time == 0
            and service.stop_restriction == 'unrestricted'
            and service.wheelchair_accessible is True
        )

    @pytest.mark.low
    def test_build__set_empty_fields(self, valid_service: fixture) -> None:
        """Check that building a service sets empty lists."""
        service: Service = valid_service

        assert service.addresses == set_empty_list() and service.exceptions == set_empty_list()

    @pytest.mark.low
    def test_build__set_end_date(self, valid_service: fixture) -> None:
        """Check that building a service sets an end date 10 days in the future."""
        service: Service = valid_service

        assert date.isoformat(date.today() + timedelta(days=10)) in service.end_date

    @pytest.mark.low
    def test_build__set_none_values(self, valid_service: fixture) -> None:
        """Check that building a service sets None values."""
        service: Service = valid_service

        assert (
            service.service_id is None
            and service.fare_price is None
            and service.max_schedule_time is None
            and service.shibboleth_affiliation is None
            and service.token_transit_fare_id is None
        )

    @pytest.mark.low
    def test_build__set_regions(self, valid_service: fixture) -> None:
        """Check that building a service sets a region."""
        service: Service = valid_service

        assert service.regions == set_service_regions()

    @pytest.mark.low
    def test_build__set_start_date(self, valid_service: fixture) -> None:
        """Check that building a service sets a start date 1 day in the past."""
        service: Service = valid_service

        assert date.isoformat(date.today() - timedelta(days=1)) in service.start_date

    @pytest.mark.low
    def test_build__set_vehicles(self, valid_service: fixture) -> None:
        """Check that building a service sets a vehicle."""
        service: Service = valid_service

        assert service.vehicles == set_service_vehicle()

    @pytest.mark.low
    def test_build__valid_input(self, valid_service: fixture) -> None:
        """Build a service with valid input."""
        service: Service = valid_service

        assert service.name == 'Testing Service'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        service: Service = Service(name='Testing Service', recurring_rides_enabled=True)

        assert service.recurring_rides_enabled is True
