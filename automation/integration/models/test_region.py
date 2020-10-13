import pytest
from pytest import fixture
from utilities.models.data_models import Region


@pytest.mark.model
@pytest.mark.unit
class TestRegion:
    """Battery of tests for Region data model functionality."""

    @pytest.fixture
    def valid_region(self) -> Region:
        """Create a valid Region."""
        region: Region = Region(
            name='Testing Region',
            geometry={
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
            },
        )

        yield region

    @pytest.mark.low
    def test_build__override_default_values(self, valid_region: fixture) -> None:
        """Check that default values may be overridden post-build.

        :param valid_region: A valid Region object for testing.
        """
        valid_region.name = 'New Region'

        assert valid_region.name == 'New Region'

    @pytest.mark.low
    def test_build__requires_geometry_param(self) -> None:
        """Check that the Region data model requires a geometry param."""
        with pytest.raises(TypeError) as e:
            Region(name='Testing Region')  # type: ignore
        assert "required positional argument: 'geometry'" in str(e.value)

    @pytest.mark.low
    def test_build__requires_name_param(self) -> None:
        """Check that the Region data model requires a name param."""
        with pytest.raises(TypeError) as e:
            Region(geometry={})  # type: ignore
        assert "required positional argument: 'name'" in str(e.value)

    @pytest.mark.low
    def test_build__set_none_values(self, valid_region: fixture) -> None:
        """Check that the Region data model sets None values.

        :param valid_region: A valid Region object for testing.
        """
        assert valid_region.region_id is None

    @pytest.mark.low
    def test_build__valid_input(self, valid_region: fixture) -> None:
        """Build a Region with valid input.

        :param valid_region: A valid Region object for testing.
        """
        assert valid_region.name == 'Testing Region' and valid_region.geometry is not None

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        region: Region = Region(name='Testing', geometry={}, region_id=1)

        assert region.region_id == 1
