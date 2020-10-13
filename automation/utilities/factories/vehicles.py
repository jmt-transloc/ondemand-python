from time import process_time
from typing import Any, Callable

from factory import Factory, LazyAttribute, Trait
from utilities.api_helpers.vehicles import VehiclesAPI
from utilities.factories.fake import fake
from utilities.models.data_models import Vehicle


class VehicleFactory(Factory):
    """Create a new vehicle for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for
    vehicle customization via the nested class method. Multiple vehicles may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Vehicle data class.

    :example usage:
        API Disabled Vehicle: VehicleFactory.create(enabled=False)
        API Wheelchair Vehicle: VehicleFactory.create(wheelchair_vehicle=True)
        Non-API: VehicleFactory.build(call_name='Striker 1')
    """

    class Meta:
        model = Vehicle

    class Params:
        """Optional params which change factory output when True.

        :param wheelchair_vehicle: Generate a vehicle with wheelchair accessibility.

        :example usage: VehicleFactory.create(wheelchair_vehicle=True)
        """

        wheelchair_vehicle: bool = Trait(wheelchair_capacity=2, wheelchair_impact=2)

    _api: VehiclesAPI = VehiclesAPI()
    call_name: str = LazyAttribute(lambda _: f'{fake.company()}-{process_time()}-Vehicle')

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to build a new Vehicle.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Vehicles API.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        _vehicle_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_vehicle(vehicle_data=_vehicle_dict)
