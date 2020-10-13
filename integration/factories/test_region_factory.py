import pytest
from utilities.api_helpers.regions import RegionsAPI
from utilities.factories.regions import RegionFactory


@pytest.mark.factory
class TestRegionFactory:
    """Battery of tests for RegionFactory functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs for RegionFactory testing."""
        self.api: RegionsAPI = RegionsAPI()

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that RegionFactory values may be overridden post-build."""
        region: dict = RegionFactory.build()
        default_region_name: str = region['name']
        region['name'] = 'Test Region'

        assert region['name'] != default_region_name

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__requires_no_params(self) -> None:
        """Check that the RegionFactory build method does not require params."""
        region: dict = RegionFactory.build()

        assert region is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__returns_type_dict(self) -> None:
        """Check that the RegionFactory build method returns a dictionary."""
        region = RegionFactory.build()

        assert type(region) == dict

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_region(self) -> None:
        """Check that a new Region is returned from the RegionFactory build method."""
        region_one: dict = RegionFactory.build()
        region_two: dict = RegionFactory.build()

        assert region_one != region_two

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__returns_type_dict(self) -> None:
        """Check that the RegionFactory create method returns a dictionary."""
        region = RegionFactory.create()

        assert type(region) == dict

        self.api.delete_region(region)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__requires_no_params(self) -> None:
        """Check that the RegionFactory create method does not require params."""
        region: dict = RegionFactory.create()

        assert region is not None

        self.api.delete_region(region)
