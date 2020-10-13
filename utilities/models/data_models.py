from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Union

from faker import Faker
from utilities.factories import date_objects


Fake = Faker('en_US')


def set_address_position() -> dict:
    return {'latitude': 41.9542371, 'longitude': -87.64845700000001}


def set_empty_list() -> list:
    return []


def set_ride_drop_off() -> dict:
    return {
        'address': '4507 South Miami Boulevard Durham, NC, USA',
        'position': {'latitude': 35.9015672, 'longitude': -78.851133},
        'priority': 0,
    }


def set_ride_pick_up() -> dict:
    return {
        'address': '4506 Emperor Boulevard Durham, NC, USA',
        'position': {'latitude': 35.8724046, 'longitude': -78.8426551},
        'priority': 0,
        'timestamp': date_objects.build_date_string(),
    }


def set_service_regions() -> list:
    return [{'dropoff': True, 'pickup': True, 'region_id': '241'}]


def set_service_vehicle() -> list:
    return ['1267']


def set_vehicle_color() -> str:
    return '1e88e5'


@dataclass
class Address:
    """An address for an Atlas application.

    This schema generates address data for the address API.
    """

    name: str
    url: str
    address: str = field(default='3930 North Pine Grove Avenue Chicago, IL, USA')
    address_id: Union[int, None] = field(default=None)
    position: dict = field(default_factory=set_address_position)


@dataclass
class Region:
    """A region for a TransLoc application.

    This schema generates region data for the regions API.
    """

    name: str
    geometry: dict
    region_id: Union[int, None] = field(default=None)


@dataclass
class Rider:
    """A rider for an API generated ride.

    This schema generates rider data for the rides API.
    """

    first_name: str
    last_name: str
    email: str
    phone: str = field(default='(555) 222-3333')
    username: str = field(default='')


@dataclass
class Ride:
    """A ride for an Atlas application.

    This schema generates ride data for the rides API.
    """

    rider: dict
    ride_id: Union[int, None] = field(default=None)
    dropoff: dict = field(default_factory=set_ride_drop_off)
    fare: Union[dict, None] = field(default=None)
    messages: list = field(default_factory=set_empty_list)
    note: Union[str, None] = field(default=None)
    pickup: dict = field(default_factory=set_ride_pick_up)
    capacity: int = field(default=1)
    service_id: Union[int, None] = field(default=None)
    service_type: str = field(default='ondemand')
    source: str = field(default='dispatcher')
    status: str = field(default='pending')
    terminal_reason: Union[str, None] = field(default=None)
    wheelchair: bool = field(default=False)

    @property
    def full_name(self) -> str:
        """Generate the rider full name."""
        return f'{self.rider["first_name"]} {self.rider["last_name"]}'


@dataclass
class RecurringRide:
    """A rides list for an API generated recurring ride.

    This schema generates ride data for the recurring rides API.
    """

    ride: dict
    rides: list
    description: str = field(default='')


@dataclass
class Service:
    """A Service for an Atlas application.

    This schema generates service data for the services API.
    """

    name: str
    service_id: Union[int, None] = field(default=None)
    addresses: list = field(default_factory=set_empty_list)
    exceptions: list = field(default_factory=set_empty_list)
    friday: bool = field(default=True)
    monday: bool = field(default=True)
    regions: list = field(default_factory=set_service_regions)
    saturday: bool = field(default=True)
    service_type: str = field(default='on_demand')
    sunday: bool = field(default=True)
    thursday: bool = field(default=True)
    tuesday: bool = field(default=True)
    vehicles: list = field(default_factory=set_service_vehicle)
    wednesday: bool = field(default=True)
    color: str = field(default='1e88e5')
    end_date: str = field(default=date.isoformat(date.today() + timedelta(days=10)))
    end_time: int = field(default=86340)
    fare_price: Union[float, None] = field(default=None)
    fare_required: bool = field(default=False)
    in_advance_enabled: bool = field(default=False)
    in_service: bool = field(default=True)
    managed_mode: bool = field(default=False)
    max_capacity: int = field(default=10)
    max_schedule_time: Union[int, None] = field(default=None)
    on_demand_enabled: bool = field(default=True)
    recurring_rides_enabled: bool = field(default=False)
    rider_restricted: bool = field(default=False)
    shibboleth_affiliation: Union[str, None] = field(default=None)
    shibboleth_restricted: bool = field(default=False)
    start_date: str = field(default=date.isoformat(date.today() - timedelta(days=1)))
    start_time: int = field(default=0)
    stop_restriction: str = field(default='unrestricted')
    token_transit_fare_id: Union[str, None] = field(default=None)
    wheelchair_accessible: bool = field(default=True)


@dataclass
class User:
    """A User for an Atlas application.

    This schema generates user data for the Users API.
    """

    username: str
    email: str
    first_name: str
    last_name: str
    phone: str = field(default='(555) 222-3333')
    password: str = field(default='testing123')
    repeat_password: str = field(default='testing123')
    privacy_policy_accepted: str = field(default='y')


@dataclass
class Vehicle:
    """A Vehicle for an Atlas application.

    This schema generates vehicle data for the vehicles API.
    """

    call_name: str
    capacity: int = field(default=1)
    color: str = field(default_factory=set_vehicle_color)
    eligible: bool = field(default=True)
    enabled: bool = field(default=True)
    vehicle_id: Union[int, None] = field(default=None)
    wheelchair_capacity: int = field(default=0)
    wheelchair_impact: int = field(default=1)


@dataclass
class Group:
    """A group for an Atlas application.

    This schema generates group data for the group API.
    """

    name: str
