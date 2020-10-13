from typing import Any, Callable

from factory import Factory, SubFactory, Trait
from utilities.api_helpers.rides import RidesAPI
from utilities.factories import date_objects
from utilities.factories.fake import fake
from utilities.factories.riders import RiderFactory
from utilities.models.data_models import Ride, Rider


class RideFactory(Factory):
    """Create a new ride for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for ride
    customization via the nested class method. Multiple rides may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Ride data class.

    :example usage:
        API: RideFactory.create(source='dispatcher', service)
        API Web Ride: RideFactory.create(account_ride=True, service)
        Non-API: RideFactory.build(source='rider_web')

    RiderFactory is a SubFactory of the RideFactory. Each time RideFactory is called, the
    RiderFactory will also be called in order to build out a Rider object for the ride. The rider
    object may be configured in the same manner as the base RiderFactory.

    :example usage: RideFactory.create(rider=RiderFactory.build(account_ride=True))
    """

    class Meta:
        model = Ride

    class Params:
        """Optional params which change factory output when True.

        :param account_ride: Generate a ride using a rider with an existing account.
        :param future_ride: Generate a ride for a future date.
        :param same_day_future_ride: Generate a same day ride for a future time.
        :param hub_ride: Generate a ride which uses a hub address as pick up or drop off.

        :example usage: RideFactory.create(hub_ride=True)
        """

        account_ride: bool = Trait(rider=RiderFactory.build(account_rider=True))

        future_ride: bool = Trait(
            pickup={
                'address': '4506 Emperor Boulevard Durham, NC, USA',
                'position': {'latitude': 35.8724046, 'longitude': -78.8426551},
                'priority': 0,
                'timestamp': date_objects.build_date_string(days=1),
            },
        )

        hub_ride: bool = Trait(
            pickup={
                'address': 'Stop #300 - TransLoc Office',
                'position': {'latitude': 35.8750625, 'longitude': -78.8406699},
                'priority': 0,
            },
        )

        ride_with_note: bool = Trait(note=fake.sentence(nb_words=3))

        same_day_future_ride: bool = Trait(
            pickup={
                'address': '4506 Emperor Boulevard Durham, NC, USA',
                'position': {'latitude': 35.8724046, 'longitude': -78.8426551},
                'priority': 0,
                'timestamp': date_objects.build_date_string(hours=1),
            },
        )

        superuser_account_ride: bool = Trait(rider=RiderFactory.build(superuser_account_rider=True))

    _api: RidesAPI = RidesAPI()

    rider: Rider = SubFactory(RiderFactory)

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to generate Ride data.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, service: dict, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Rides API.

        :param model_class: The factory model used for generation.
        :param service: The intended service for Ride creation.
        :param kwargs: Additional arguments being passed for generation.
        """
        kwargs['service_id'] = service['service_id']
        _ride_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_ride(ride_data=_ride_dict)
