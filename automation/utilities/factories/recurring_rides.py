from typing import Any, Callable, List

from factory import Factory, LazyAttribute, Trait
from utilities.api_helpers.recurring_rides import RecurringRidesAPI
from utilities.factories import date_objects
from utilities.factories.rides import RideFactory
from utilities.models.data_models import RecurringRide


class RecurringRideFactory(Factory):
    """Create a new recurring ride for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for recurring ride
    customization via the nested class method. Multiple recurring rides may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the RecurringRide data class.

    :example usage:
        API: RecurringRideFactory.create()
        Non-API: RecurringRideFactory.build()

    RideFactory is a SubFactory of the RecurringRideFactory. Each time RecurringRideFactory is
    called, the RideFactory will also be called in order to build out a Ride object for the
    recurring ride. The ride object may be configured in the same manner as the base RideFactory.

    :example usage:
        API: RecurringRideFactory.create(ride=RideFactory.build(account_ride=True))
        Non-API: RecurringRideFactory.build(ride=RideFactory.build(note='This is a test'))
    """

    class Meta:
        model = RecurringRide

    class Params:
        """Optional params which change factory output when True.

        :param future_recurring_ride: Create a recurring ride for a future date.
        :param ride_with_note: Create a recurring ride with a driver note.
        :param same_day_future_recurring_ride: Create a same-day recurring ride for a future time.

        :example usage: RecurringRideFactory.create(future_recurring_ride=True)
        """

        future_recurring_ride: bool = Trait(ride=RideFactory.build(future_ride=True))

        ride_with_note: bool = Trait(
            ride=LazyAttribute(lambda _: RideFactory.build(ride_with_note=True)),
        )

        same_day_future_recurring_ride: bool = Trait(
            ride=RideFactory.build(same_day_future_ride=True),
        )

    _api: RecurringRidesAPI = RecurringRidesAPI()

    ride: dict = LazyAttribute(lambda _: RideFactory.build())
    rides: List[dict] = [
        {'timestamp': date_objects.build_date_string(days=1)},
        {'timestamp': date_objects.build_date_string(days=3)},
        {'timestamp': date_objects.build_date_string(days=5)},
        {'timestamp': date_objects.build_date_string(days=7)},
        {'timestamp': date_objects.build_date_string(days=9)},
        {'timestamp': date_objects.build_date_string(days=11)},
    ]

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to generate Recurring Ride data.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, service: dict, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Rides API.

        :param model_class: The factory model used for generation.
        :param service: The intended service for RecurringRide creation.
        :param kwargs: Additional arguments being passed for generation.
        """
        kwargs['ride']['service_id'] = service['service_id']
        _recurring_ride_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_recurring_ride(ride_data=_recurring_ride_dict)
