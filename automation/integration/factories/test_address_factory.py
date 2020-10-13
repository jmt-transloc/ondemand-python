import pytest
from utilities.api_helpers.addresses import AddressesAPI
from utilities.factories.addresses import AddressFactory


@pytest.mark.factory
class TestAddressFactory:
    """Battery of tests for AddressFactory functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs for AddressFactory testing."""
        self.api: AddressesAPI = AddressesAPI()

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__override_default_values(self) -> None:
        """Check that AddressFactory values may be overridden post-build."""
        address: dict = AddressFactory.build()
        default_address_name: str = address['name']

        address['name'] = 'Test Address'

        assert address['name'] != default_address_name

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__requires_no_params(self) -> None:
        """Check that the AddressFactory build method does not require params."""
        address: dict = AddressFactory.build()

        assert address is not None

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__params__rider_address(self) -> None:
        """Check that a rider address (OnDemand Web) can be built from the AddressFactory."""
        address: dict = AddressFactory.build(rider_address=True)

        assert '/me/rider/addresses' in address['url']

    @pytest.mark.low
    @pytest.mark.unit
    def test_build__returns_type_dict(self) -> None:
        """Check that a dictionary is returned from the AddressFactory build method."""
        address = AddressFactory.build()

        assert type(address) == dict

    @pytest.mark.medium
    @pytest.mark.unit
    def test_build__subsequent_calls_return_new_address(self) -> None:
        """Check that a new Address is returned from the AddressFactory build method."""
        address_one: dict = AddressFactory.build()
        address_two: dict = AddressFactory.build()

        assert address_one != address_two

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__params__rider_address(self) -> None:
        """Check that a rider address (OnDemand Web) can be built from the AddressFactory."""
        address: dict = AddressFactory.create(rider_address=True)

        self.api.delete_address(address=address, rider_address=True)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__returns_type_dict(self) -> None:
        """Check that a dictionary is returned from the AddressFactory create method."""
        address = AddressFactory.create()

        assert type(address) == dict

        self.api.delete_address(address=address, rider_address=False)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create__requires_no_params(self) -> None:
        """Check that the AddressFactory create method requires no params."""
        address = AddressFactory.create()

        assert address is not None

        self.api.delete_address(address=address, rider_address=False)
