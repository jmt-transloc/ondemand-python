import pytest
from pytest import fixture


@pytest.mark.fixtures
@pytest.mark.integration
class TestServiceFixtures:
    """Battery of tests for testing service fixture functionality."""

    @pytest.mark.low
    def test__service(self, service: fixture) -> None:
        """Check that a service fixture returns a service with an ID.

        :param service: A service fixture.
        """
        new_service: dict = service

        assert new_service['service_id'] is not None

    @pytest.mark.low
    def test__service_with_add_exception(self, service_with_add_exception: fixture) -> None:
        """Check that a service fixture returns a service with an add exception.

        :param service_with_add_exception: An add service exception fixture.
        """
        service: dict = service_with_add_exception
        exceptions: dict = service['exceptions'][0]

        assert (
            'service_added' in exceptions['type']
            and 'Testing Service Addition.' in exceptions['message']
        )

    @pytest.mark.low
    def test__service_with_fare(self, service_with_fare: fixture) -> None:
        """Check that a service fixture returns a service with fare enabled.

        :param service_with_fare: A fare service fixture.
        """
        service: dict = service_with_fare

        assert service['fare_price'] == 2.0 and service['fare_required'] is True

    @pytest.mark.low
    def test__service_with_hub_address(self, service_with_hub_address: fixture) -> None:
        """Check that a service fixture returns a service with a hub address.

        :param service_with_hub_address: A hub address service fixture.
        """
        service: dict = service_with_hub_address
        addresses: dict = service['addresses'][0]

        assert addresses['hub'] is True

    @pytest.mark.low
    def test__service_with_in_advance(self, service_with_in_advance: fixture) -> None:
        """Check that a service fixture returns a service with in advance enabled.

        :param service_with_in_advance: An in advance enabled service fixture.
        """
        service: dict = service_with_in_advance

        assert service['in_advance_enabled'] is True

    @pytest.mark.low
    def test__service_with_limited_in_advance(
        self, service_with_limited_in_advance: fixture,
    ) -> None:
        """Check that a service fixture returns a limited in advance enabled service.

        :param service_with_limited_in_advance: A limited in advance enabled service fixture.
        """
        service: dict = service_with_limited_in_advance

        assert service['in_advance_enabled'] is True and service['max_schedule_time'] == 7

    @pytest.mark.low
    def test__service_with_managed_mode(self, service_with_managed_mode: fixture) -> None:
        """Check that a service fixture returns a managed mode service.

        :param service_with_managed_mode: A managed mode service fixture.
        """
        service: dict = service_with_managed_mode

        assert service['managed_mode'] is True

    @pytest.mark.low
    def test__service_with_recurring_rides(self, service_with_recurring_rides: fixture) -> None:
        """Check that a service fixture returns a service with recurring rides enabled.

        :param service_with_recurring_rides: A recurring rides enabled service fixture.
        """
        service: dict = service_with_recurring_rides

        assert service['in_advance_enabled'] is True and service['recurring_rides_enabled'] is True

    @pytest.mark.low
    def test__service_with_limited_recurring_rides(
        self, service_with_limited_recurring_rides: fixture,
    ) -> None:
        """Check that a service fixture returns a service with limited recurring rides enabled.

        :param service_with_limited_recurring_rides: A limited recurring rides service fixture.
        """
        service: dict = service_with_limited_recurring_rides

        assert (
            service['in_advance_enabled'] is True
            and service['recurring_rides_enabled'] is True
            and service['max_schedule_time'] == 7
        )

    @pytest.mark.low
    def test__service_with_remove_exception(self, service_with_remove_exception: fixture) -> None:
        """Check that a service fixture returns a service with a remove exception.

        :param service_with_remove_exception: A remove service exception fixture.
        """
        service: dict = service_with_remove_exception
        exceptions: dict = service['exceptions'][0]

        assert (
            'service_removed' in exceptions['type']
            and 'Testing Service Removal.' in exceptions['message']
        )
