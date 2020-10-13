from time import process_time
from typing import Any, Callable

from factory import Factory, LazyAttribute
from utilities.api_helpers.regions import RegionsAPI
from utilities.factories.fake import fake
from utilities.models.data_models import Region


class RegionFactory(Factory):
    """Create a new region for OnDemand testing.

    This is a factory which can be configured by passing in optional parameters for region
    customization via the nested class method. Multiple rides may be created using the
    factory by calling a batch method.

    Optional parameters must match fields defined in the Region data class.

    :example usage:
        API: RegionFactory.create(name='Rochester Area')
        Non-API: RegionFactory.build(name='Triangle Area')
    """

    class Meta:
        model = Region

    _api: RegionsAPI = RegionsAPI()

    name: str = LazyAttribute(lambda _: f'{fake.company()}-{process_time()}-Region')
    geometry: dict = {
        'type': 'MultiPolygon',
        'coordinates': [
            [
                [
                    [-78.85182348156738, 35.87850360073744],
                    [-78.85439840222168, 35.87259202888435],
                    [-78.842210444458, 35.87113145494405],
                    [-78.84143796826172, 35.87815587342781],
                ],
            ],
        ],
    }

    @classmethod
    def _build(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _build method to build a new Region.

        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        return model_class(**kwargs).__dict__

    @classmethod
    def _create(cls, model_class: Callable, **kwargs: Any) -> dict:
        """Override the default _create method to post against the Regions API.

        :param app: The application under test.
        :param model_class: The factory model used for generation.
        :param kwargs: Additional arguments being passed for generation.
        """
        _region_dict: dict = model_class(**kwargs).__dict__

        return cls._api.create_region(region_data=_region_dict)
