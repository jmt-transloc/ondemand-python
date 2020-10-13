from typing import Generator

import pytest
from factory import Factory
from pytest_factoryboy import register
from utilities.api_helpers.addresses import AddressesAPI
from utilities.api_helpers.groups import GroupsAPI
from utilities.api_helpers.regions import RegionsAPI
from utilities.api_helpers.services import ServicesAPI
from utilities.api_helpers.vehicles import VehiclesAPI
from utilities.factories.addresses import AddressFactory
from utilities.factories.groups import GroupFactory
from utilities.factories.recurring_rides import RecurringRideFactory
from utilities.factories.regions import RegionFactory
from utilities.factories.rides import RideFactory
from utilities.factories.services import ServiceFactory
from utilities.factories.users import UserFactory
from utilities.factories.vehicles import VehicleFactory


register(AddressFactory)
register(GroupFactory)
register(RecurringRideFactory)
register(RegionFactory)
register(RideFactory)
register(ServiceFactory)
register(UserFactory)
register(VehicleFactory)

_addresses_api: AddressesAPI = AddressesAPI()
_groups_api: GroupsAPI = GroupsAPI()
_regions_api: RegionsAPI = RegionsAPI()
_service_api: ServicesAPI = ServicesAPI()
_vehicles_api: VehiclesAPI = VehiclesAPI()


@pytest.fixture
def address(address_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down an address for testing the OnDemand Admin application.

    :param address_factory: A factory for building addresses via the API or UI.
    """
    address: dict = address_factory.create(rider_address=False)

    yield address

    _addresses_api.delete_address(address, rider_address=False)


@pytest.fixture
def group(group_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a group for testing OnDemand applications.

    :param group_factory: A factory for building a group via the API.
    """
    group: dict = group_factory.create()

    yield group

    _groups_api.delete_group(group)


@pytest.fixture
def region(region_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a region for testing OnDemand applications.

    :param region_factory: A factory for building regions via the API.
    """
    region: dict = region_factory.create()

    yield region

    _regions_api.delete_region(region)


@pytest.fixture
def rider_address(address_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down an address for testing the OnDemand Web application.

    :param address_factory: A factory for building addresses via the API.
    """
    rider_address: dict = address_factory.create(rider_address=True)

    yield rider_address

    _addresses_api.delete_address(rider_address, rider_address=True)


@pytest.fixture
def service(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service for testing OnDemand applications.

    :param service_factory: A factory for building services via the API.
    """
    service: dict = service_factory.create()

    yield service

    _service_api.delete_service(service)


@pytest.fixture
def service_with_add_exception(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down an add exception service.

    :param service_factory: A factory for building services via the API.
    """
    add_exception_service: dict = service_factory.create(exception_service_added=True)

    yield add_exception_service

    _service_api.delete_service(add_exception_service)


@pytest.fixture
def service_with_fare(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a fare service.

    :param service_factory: A factory for building services via the API.
    """
    fare_service: dict = service_factory.create(fare_service=True)

    yield fare_service

    _service_api.delete_service(fare_service)


@pytest.fixture
def service_with_hub_address(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with a hub address.

    :param service_factory: A factory for building services via the API.
    """
    hub_service: dict = service_factory.create(hub_address=True)

    yield hub_service

    _service_api.delete_service(hub_service)


@pytest.fixture
def service_with_in_advance(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with advanced rides enabled.

    :param service_factory: A factory for building services via the API.
    """
    future_ride_service: dict = service_factory.create(future_ride_service=True)

    yield future_ride_service

    _service_api.delete_service(future_ride_service)


@pytest.fixture
def service_with_limited_in_advance(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with limited advanced rides enabled.

    This service will allow advanced rides up to 7 days in the future.

    :param service_factory: A factory for building services via the API.
    """
    limited_future_ride_service: dict = service_factory.create(
        future_ride_service=True, max_schedule_time=7,
    )

    yield limited_future_ride_service

    _service_api.delete_service(limited_future_ride_service)


@pytest.fixture
def service_with_managed_mode(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with managed mode enabled.

    :param service_factory: A factory for building services via the API.
    """
    managed_mode_service: dict = service_factory.create(managed_mode=True)

    yield managed_mode_service

    _service_api.delete_service(managed_mode_service)


@pytest.fixture
def service_with_recurring_rides(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with recurring rides enabled.

    :param service_factory: A factory for building services via the API.
    """
    recurring_ride_service: dict = service_factory.create(recurring_ride_service=True)

    yield recurring_ride_service

    _service_api.delete_service(recurring_ride_service)


@pytest.fixture
def service_with_limited_recurring_rides(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a service with limited recurring rides enabled.

    This service will allow advanced rides up to 7 days in the future.

    :param service_factory: A factory for building services via the API.
    """
    limited_recurring_ride_service: dict = service_factory.create(
        recurring_ride_service=True, max_schedule_time=7,
    )

    yield limited_recurring_ride_service

    _service_api.delete_service(limited_recurring_ride_service)


@pytest.fixture
def service_with_remove_exception(service_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a remove exception service for testing OnDemand applications.

    :param service_factory: A factory for building services via the API.
    """
    remove_exception_service: dict = service_factory.create(exception_service_removed=True)

    yield remove_exception_service

    _service_api.delete_service(remove_exception_service)


@pytest.fixture
def vehicle(vehicle_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a vehicle for testing OnDemand applications.

    :param vehicle_factory: A factory for building vehicles via the API or UI.
    """
    vehicle: dict = vehicle_factory.create()

    yield vehicle

    _vehicles_api.delete_vehicle(vehicle)


@pytest.fixture
def wheelchair_vehicle(vehicle_factory: Factory) -> Generator[dict, None, None]:
    """Instantiate and tear down a wheelchair enabled vehicle for testing OnDemand applications.

    :param vehicle_factory: A factory for building vehicles via the API or UI.
    """
    wheelchair_vehicle: dict = vehicle_factory.create(wheelchair_vehicle=True)

    yield wheelchair_vehicle

    _vehicles_api.delete_vehicle(wheelchair_vehicle)
