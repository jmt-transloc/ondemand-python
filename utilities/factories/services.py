from datetime import date, timedelta
from time import process_time
from typing import Any, Callable

from factory import Factory, LazyAttribute, Trait
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.fake import fake
from utilities.models.data_models import Service


class ServiceFactory(Factory):
    """Create a new service for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for
    service customization via the nested class method. Multiple services may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Service data class.

    :example usage:
        Fare Service: ServiceFactory.create(fare_service=True, in_advance_enabled=True)
        Non-Fare Service: ServiceFactory.create(in_advance_enabled=True)
    """

    class Meta:
        model = Service

    class Params:
        """Optional boolean params which change factory output when True.

        :param exception_service_added: Create a service with an add service exception.
        :param exception_service_removed: Create a service with a remove service exception.
        :param expired_service: Create a service that has expired.
        :param fare_service: Create a service with a fare payment.
        :param future_ride_service: Create a service with future rides enabled.
        :param hub_address: Create a service with a hub.
        :param recurring_ride_service: Create a service with recurring rides enabled.

        :example usage: ServiceFactory.create(expired_service=True)
        """

        exception_service_added: bool = Trait(
            exceptions=[
                {
                    'end_time': f'{date.today() + timedelta(days=22)}T18:00:00.000Z',
                    'message': 'Testing Service Addition.',
                    'start_time': f'{date.today() + timedelta(days=15)}T09:30:00.000Z',
                    'type': 'service_added',
                },
            ],
        )

        exception_service_removed: bool = Trait(
            exceptions=[
                {
                    'end_time': f'{date.today() + timedelta(days=7)}T18:00:00.000Z',
                    'message': 'Testing Service Removal.',
                    'start_time': f'{date.today() + timedelta(days=3)}T09:30:00.000Z',
                    'type': 'service_removed',
                },
            ],
        )

        expired_service: bool = Trait(
            end_date=date.isoformat(date.today() - timedelta(days=5)),
            start_date=date.isoformat(date.today() - timedelta(days=10)),
        )

        fare_service: bool = Trait(
            fare_required=True, fare_price=2.0,
        )

        future_ride_service: bool = Trait(in_advance_enabled=True)

        hub_address: bool = Trait(
            addresses=[{'hub': True, 'pickup': True, 'dropoff': True, 'address_id': '7539'}],
        )

        recurring_ride_service: bool = Trait(
            in_advance_enabled=True, recurring_rides_enabled=True,
        )

    _api: ServicesAPI = ServicesAPI()

    name: str = LazyAttribute(lambda _: f'{fake.company()}-{process_time()}-Service')

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Services API.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        _service_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_service(service_data=_service_dict)
