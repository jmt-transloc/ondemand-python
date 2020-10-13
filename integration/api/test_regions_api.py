from typing import Generator

import pytest
from pytest import fixture
from requests import HTTPError
from utilities.api_helpers.regions import RegionsAPI
from utilities.factories.regions import RegionFactory


@pytest.mark.api
class TestRegionsAPI:
    """Battery of tests for RegionsAPI functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in RegionsAPI testing."""
        self.regions_api: RegionsAPI = RegionsAPI()

    @pytest.fixture
    def build_region(self) -> Generator[dict, None, None]:
        """Build a Region object for RegionsAPI method testing.

        This region should be used in testing API creation methods.
        """
        region: dict = RegionFactory.build()

        yield region

    @pytest.fixture
    def create_region(self) -> Generator[dict, None, None]:
        """Create a Region via API for RegionsAPI method testing.

        This region should be used in testing API deletion methods.
        """
        region: dict = RegionFactory.create()

        yield region

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_region__failure__invalid_input(self) -> None:
        """Check that the create_region method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.regions_api.create_region(region_data=1111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_region__failure__region_data_required(self) -> None:
        """Check that the create_region method fails without a region_data param."""
        with pytest.raises(TypeError) as e:
            self.regions_api.create_region()  # type: ignore
        assert "required positional argument: 'region_data'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_create_region__success(self, build_region: fixture) -> None:
        """Check that a Region may be created.

        :param build_region: A Region object for testing.
        """
        try:
            self.regions_api.create_region(build_region)
            self.regions_api.delete_region(build_region)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create_region__success__returns_type_dict(self, build_region: fixture) -> None:
        """Check that the create_region method returns a dictionary.

        :param build_region: A Region object for testing.
        """
        region = self.regions_api.create_region(build_region)

        assert type(region) == dict

        self.regions_api.delete_region(region)

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_region__failure__invalid_input(self) -> None:
        """Check that the delete_region method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.regions_api.delete_region(region={'region_id': 1})

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_region__failure__region_required(self) -> None:
        """Check that the delete_region method fails without a region param."""
        with pytest.raises(TypeError) as e:
            self.regions_api.delete_region()  # type: ignore
        assert "required positional argument: 'region'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_delete_region__success(self, create_region: fixture) -> None:
        """Check that a Region may be deleted.

        :param create_region: A Region object for testing.
        """
        try:
            self.regions_api.delete_region(create_region)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)
