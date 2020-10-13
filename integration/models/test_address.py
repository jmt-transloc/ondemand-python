import pytest
from pytest import fixture
from utilities.api_helpers.api import API
from utilities.models.data_models import Address, set_address_position


@pytest.mark.model
@pytest.mark.unit
class TestAddress:
    """Battery of tests for Address data model functionality."""

    @pytest.fixture
    def valid_address(self) -> Address:
        """Create a valid Address."""
        url: str = API.build_api_url(f'/ondemand/test_agency/addresses')
        address: Address = Address(name='Test Address', url=url)

        yield address

    @pytest.mark.low
    def test_build__override_default_values(self, valid_address: fixture) -> None:
        """Check that default values may be overridden post-build.

        :param valid_address: A valid Address object for testing.
        """
        valid_address.name = 'New Address'

        assert valid_address.name == 'New Address'

    @pytest.mark.low
    def test_build__requires_name_param(self) -> None:
        """Check that the Address data model requires a name param."""
        with pytest.raises(TypeError) as e:
            Address(url='testing_url')  # type: ignore
        assert "required positional argument: 'name'" in str(e.value)

    @pytest.mark.low
    def test_build__requires_url_param(self) -> None:
        """Check that the Address data model requires a url param."""
        with pytest.raises(TypeError) as e:
            Address(name='Test Address')  # type: ignore
        assert "required positional argument: 'url'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_address: fixture) -> None:
        """Check that building an Address sets default values.

        :param valid_address: A valid Address object for testing.
        """
        assert valid_address.address == '3930 North Pine Grove Avenue Chicago, IL, USA'

    @pytest.mark.low
    def test_build__set_address_position(self, valid_address) -> None:
        """Check that building an Address sets an address position.

        :param valid_address: A valid Address object for testing.
        """
        assert valid_address.position == set_address_position()

    @pytest.mark.low
    def test_build__set_none_values(self, valid_address: fixture) -> None:
        """Check that building an Address sets None values.

        :param valid_address: A valid Address object for testing.
        """
        assert valid_address.address_id is None

    @pytest.mark.low
    def test_build__valid_input(self, valid_address: fixture) -> None:
        """Build an Address with valid input.

        :param valid_address: A valid Address object for testing.
        """
        assert valid_address.name == 'Test Address'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        address: Address = Address(
            name='Test Address', url='testing_url', address='24 Girard Street, Rochester, NY, USA',
        )

        assert address.address == '24 Girard Street, Rochester, NY, USA'
