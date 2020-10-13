from time import process_time
from typing import Any, Callable

from factory import Factory, LazyAttribute, Trait
from utilities.factories.fake import fake
from utilities.models.data_models import User


class UserFactory(Factory):
    """Create new user data for OnDemand testing.

    NOTE: This factory DOES NOT involve an API. Data will be created as a User object using both
    _create and _build class methods.

    This is a factory which can be configured by passing in optional parameters for user
    customization via the nested class method. Multiple users may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the User data class.

    :example usage: UserFactory.create(account_user=True)
    """

    class Meta:
        model = User

    class Params:
        """Optional params which change factory output when True.

        :param account_user: Generate a user using an existing account.

        :example usage: UserFactory.create(account_user=True)
        """

        account_user: bool = Trait(
            first_name='QA',
            last_name='Rider',
            email='automation+qa_user_001@transloc.com',
            username='qa_user_001',
        )

    email: str = LazyAttribute(lambda _: f'{process_time()}-{fake.email()}')
    first_name: str = LazyAttribute(lambda _: f'{fake.first_name()}-{process_time()}')
    last_name: str = LazyAttribute(lambda _: f'{fake.last_name()}-{process_time()}')
    username: str = LazyAttribute(lambda _: f'{fake.user_name()}-{fake.numerify()}')

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> User:
        """Override the default _build method to build a new User.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs)

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> User:
        """Override the default _create method to build a new User.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs)
