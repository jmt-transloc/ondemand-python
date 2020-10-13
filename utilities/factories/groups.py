from time import process_time
from typing import Any, Callable

from environs import Env
from factory import Factory, LazyAttribute
from utilities.api_helpers.groups import GroupsAPI
from utilities.factories.fake import fake
from utilities.models.data_models import Group


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class GroupFactory(Factory):
    """Create a new group for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for group
    customization via the nested class method. Multiple groups may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Group data class.

    :example usage:
        API: GroupFactory.create(name='Rider Group')
        Non-API: GroupFactory.build(name='Admin Group')
    """

    class Meta:
        model = Group

    _api: GroupsAPI = GroupsAPI()
    name: str = LazyAttribute(lambda _: f'{fake.sentence(nb_words=3)}-{process_time()}')

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to build a new Group.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Groups API.

        :param app: The application under test.
        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        _group_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_group(group_data=_group_dict)
