from typing import Generator

import pytest
from environs import Env
from pytest import fixture
from requests import HTTPError
from utilities.api_helpers.addresses import AddressesAPI
from utilities.api_helpers.api import API
from utilities.factories.addresses import AddressFactory


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


@pytest.mark.api
class TestAddressesAPI:
    """Battery of tests for AddressesAPI functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in AddressesAPI testing."""
        self.addresses_api: AddressesAPI = AddressesAPI()

    @pytest.fixture
    def address(self) -> Generator[dict, None, None]:
        """Instantiate an Address for AddressesAPI method testing."""
        address: dict = AddressFactory.create()

        yield address

    @pytest.fixture
    def rider_address(self) -> Generator[dict, None, None]:
        """Instantiate an OnDemand Web Address for AddressesAPI method testing."""
        address: dict = AddressFactory.create(rider_address=True)

        yield address

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_address__failure__invalid_input(self) -> None:
        """Check that the create_address method fails with invalid input."""
        with pytest.raises(TypeError):
            self.addresses_api.create_address(
                address_data=1111111, url=API.build_api_url('/testing'),  # type: ignore
            )

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_address__failure__address_data_required(self) -> None:
        """Check that the create_address method fails without an address_data param."""
        with pytest.raises(TypeError) as e:
            self.addresses_api.create_address(url='testing_url')  # type: ignore
        assert "required positional argument: 'address_data'" in str(e.value)

    @pytest.mark.low
    @pytest.mark.unit
    def test_create_address__failure__url_required(self) -> None:
        """Check that the create_address method fails without an url param."""
        with pytest.raises(TypeError) as e:
            self.addresses_api.create_address(address_data={})  # type: ignore
        assert "required positional argument: 'url'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_create_address__success(self) -> None:
        """Check that an Address may be created."""
        address_data: dict = AddressFactory.build()
        url: str = API.build_api_url(path=f'/ondemand/{AGENCY}/addresses')

        try:
            address: dict = self.addresses_api.create_address(address_data=address_data, url=url)
            self.addresses_api.delete_address(address=address, rider_address=False)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.', pytrace=True)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create_address__remove_url_key(self) -> None:
        """Check that the create_address method removes the 'url' key."""
        address_data: dict = AddressFactory.build()
        url: str = API.build_api_url(path=f'/ondemand/{AGENCY}/addresses')

        address: dict = self.addresses_api.create_address(address_data=address_data, url=url)

        assert 'url' not in address

        self.addresses_api.delete_address(address=address, rider_address=False)

    @pytest.mark.low
    @pytest.mark.integration
    def test_create_address__returns_type_dict(self) -> None:
        """Check that the create_address method returns a dictionary."""
        address_data: dict = AddressFactory.build()
        address: dict = self.addresses_api.create_address(
            address_data=address_data, url=address_data['url'],
        )

        assert type(address) is dict

        self.addresses_api.delete_address(address=address, rider_address=False)

    @pytest.mark.low
    @pytest.mark.integration
    def test_delete_address__failure__invalid_input(self) -> None:
        """Check that the delete_address method fails with invalid input."""
        with pytest.raises(HTTPError):
            self.addresses_api.delete_address(address={'address_id': 1}, rider_address=False)

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_address__failure__requires_address_param(self) -> None:
        """Check that the delete_address method fails without an address param."""
        with pytest.raises(TypeError) as e:
            self.addresses_api.delete_address(rider_address=False)  # type: ignore
        assert "required positional argument: 'address'" in str(e.value)

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete_address__failure__requires_rider_address_param(self) -> None:
        """Check that the delete_address method fails without a rider address param."""
        with pytest.raises(TypeError) as e:
            self.addresses_api.delete_address(address={'address_id': 1})  # type: ignore
        assert "required positional argument: 'rider_address'" in str(e.value)

    @pytest.mark.high
    @pytest.mark.integration
    def test_delete_address__success(self, address: fixture) -> None:
        """Check that an Address may be deleted.

        :param address: An Address object for testing.
        """
        self.addresses_api.delete_address(address=address, rider_address=False)

    @pytest.mark.high
    @pytest.mark.integration
    def test_delete_address__success__rider_address(self, rider_address: fixture) -> None:
        """Check that an OnDemand Web Address may be deleted.

        :param rider_address: An OnDemand Web Address object for testing.
        """
        self.addresses_api.delete_address(address=rider_address, rider_address=True)
