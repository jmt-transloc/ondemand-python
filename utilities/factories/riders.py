from time import process_time
from typing import Any, Callable

from factory import Factory, LazyAttribute, Trait
from utilities.factories.fake import fake
from utilities.models.data_models import Rider


class RiderFactory(Factory):
    """Create new rider data for OnDemand testing.

    NOTE: This factory DOES NOT involve an API. Data will be created as a Rider object using both
    _create and _build class methods.

    This is a factory which can be configured by passing in optional parameters for rider
    customization via the nested class method. Multiple riders may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Rider data class.

    :example usage: RiderFactory.create(account_rider=True)
    """

    class Meta:
        model = Rider

    class Params:
        """Optional params which change factory output when True.

        :param account_rider: Generate a rider using an existing account.

        :example usage: RiderFactory.create(account_rider=True)
        """

        account_rider: bool = Trait(
            first_name='QA',
            last_name='Rider',
            email='automation+qa_rider_001@transloc.com',
            username='qa_rider_001',
        )

        superuser_account_rider: bool = Trait(
            first_name='QA',
            last_name='User',
            email='automation+qa_user_001@transloc.com',
            username='qa_user_001',
        )

    first_name: str = LazyAttribute(lambda _: f'{fake.first_name()}-{process_time()}')
    last_name: str = LazyAttribute(lambda _: f'{fake.last_name()}-{process_time()}')
    email: str = LazyAttribute(lambda _: f'{process_time()}-{fake.email()}')

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to build a new Rider.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to build a new Rider.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__
