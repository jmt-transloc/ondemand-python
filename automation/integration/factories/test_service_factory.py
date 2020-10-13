from datetime import date, timedelta

import pytest
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.services import ServiceFactory
from utilities.models.data_models import Service


@pytest.mark.factory
class TestServiceFactory:
    """Battery of tests for ServiceFactory functionality."""

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that ServiceFactory values may be overridden post-build."""
        service = ServiceFactory.build()
        default_service_name: str = service.name

        service.name = 'Testing123'

        assert service.name != default_service_name

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__exception_service_added(self) -> None:
        """Check that an exception service added is built from the ServiceFactory."""
        exception_service: Service = ServiceFactory.build(exception_service_added=True)

        assert (
            'service_added' in exception_service.exceptions[0]['type']
            and 'Testing Service Addition.' in exception_service.exceptions[0]['message']
        )

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__exception_service_removed(self) -> None:
        """Check that an exception service removed is built from the ServiceFactory."""
        exception_service: Service = ServiceFactory.build(exception_service_removed=True)

        assert (
            'service_removed' in exception_service.exceptions[0]['type']
            and 'Testing Service Removal.' in exception_service.exceptions[0]['message']
        )

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__expired_service(self) -> None:
        """Check that an expired service is built from the ServiceFactory."""
        expired_service: Service = ServiceFactory.build(expired_service=True)

        assert expired_service.end_date == date.isoformat(
            date.today() - timedelta(days=5),
        ) and expired_service.start_date == date.isoformat(date.today() - timedelta(days=10))

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__fare_service(self) -> None:
        """Check that a fare service is built from the ServiceFactory."""
        fare_service: Service = ServiceFactory.build(fare_service=True)

        assert fare_service.fare_price == 2.0 and fare_service.fare_required is True

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__future_ride_service(self) -> None:
        """Check that a future ride service is built from the ServiceFactory."""
        future_ride_service: Service = ServiceFactory.build(future_ride_service=True)

        assert future_ride_service.in_advance_enabled is True

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__hub_address(self) -> None:
        """Check that a hub address service is built from the ServiceFactory."""
        hub_service: Service = ServiceFactory.build(hub_address=True)

        assert hub_service.addresses[0]['hub'] is True

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__recurring_ride_service(self) -> None:
        """Check that a recurring ride service is built from the ServiceFactory."""
        recurring_ride_service: Service = ServiceFactory.build(recurring_ride_service=True)

        assert (
            recurring_ride_service.in_advance_enabled is True
            and recurring_ride_service.recurring_rides_enabled is True
        )

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__returns_type_service(self) -> None:
        """Check that a Service is built from the ServiceFactory build method."""
        service = ServiceFactory.build()

        assert type(service) == Service

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_service(self) -> None:
        """Check that a new Service is returned from the ServiceFactory build method."""
        service_one: Service = ServiceFactory.build()
        service_two: Service = ServiceFactory.build()

        assert service_one != service_two

    @pytest.mark.medium
    @pytest.mark.integration
    def test_create__returns_type_dict(self) -> None:
        """Check that a dictionary is created from the ServiceFactory create method."""
        api: ServicesAPI = ServicesAPI()
        service = ServiceFactory.create()

        assert type(service) == dict

        api.delete_service(service)
