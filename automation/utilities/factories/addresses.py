from time import process_time
from typing import Any, Callable

from environs import Env
from factory import Factory, LazyAttribute, Trait
from utilities.api_helpers.addresses import AddressesAPI
from utilities.api_helpers.api import API
from utilities.factories.fake import fake
from utilities.models.data_models import Address


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class AddressFactory(Factory):
    """Create a new address for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for
    address customization via the nested class method. Multiple addresses may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Address data class.

    :example usage:
        API: AddressFactory.create(name='Lake Park Plaza')
        API Web Address: AddressFactory.create(name='Lake Park Plaza', rider_address=True)
        Non-API: AddressFactory.build(name='Lake Park Plaza')
    """

    class Meta:
        model = Address

    class Params:
        """Optional params which change factory output when True.

        :param rider_address: Generate an address for the OnDemand Web application.

        :example usage: AddressFactory.create(rider_address=True)
        """

        rider_address = Trait(url=API.build_api_url('/me/rider/addresses'))

    _api: AddressesAPI = AddressesAPI()

    url: str = API.build_api_url(f'/ondemand/{AGENCY}/addresses')
    name: str = LazyAttribute(lambda _: f'{fake.sentence(nb_words=3)}-{process_time()}')

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to build a new Address.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Addresses API.

        :param app: The application under test.
        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        _address_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_address(address_data=_address_dict, url=_address_dict['url'])
