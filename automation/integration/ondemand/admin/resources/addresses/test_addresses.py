import factory
import pytest
from pages.ondemand.admin.resources.addresses.addresses import Addresses
from pages.ondemand.common.addresses.addresses_list import AddressRow
from pytest import fixture
from utilities.api_helpers.addresses import AddressesAPI
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestAddresses:
    """Battery of tests for Addresses page address creation functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.addresses: Addresses = Addresses(selenium)
        self.API: AddressesAPI = AddressesAPI()

    @pytest.mark.high
    @pytest.mark.smoke
    def test_add_address(self, address_factory: factory) -> None:
        """Input a valid address, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        address: dict = address_factory.build(rider_address=False)

        self.addresses.visit()
        self.addresses.add_new_address(address=address)

        row: AddressRow = self.addresses.addresses_list.surface_address_row(address)

        assert address['name'] in row.data

        address['address_id'] = row.address_id
        self.API.delete_address(address, rider_address=False)

    @pytest.mark.medium
    def test_edit_address(self, address: fixture) -> None:
        """Yield an address from the API, edit a field, then check for a success state."""
        self.addresses.visit()

        before_data: str = self.addresses.addresses_list.surface_address_row(address).data
        self.addresses.open_edit_address(address=address)

        new_label = fake.sentence(nb_words=2)
        self.addresses.edit_address(new_label=new_label)

        after_data: str = self.addresses.addresses_list.surface_address_row(
            address, address_label=new_label,
        ).data

        assert before_data != after_data

    @pytest.mark.low
    def test_delete_address(self, address_factory: factory) -> None:
        """Yield an address from the API, delete the address, then check for a success state."""
        address: dict = address_factory.create(rider_address=False)

        self.addresses.visit()

        self.addresses.delete_address(address=address)
        row: AddressRow = self.addresses.addresses_list.surface_address_row(address)

        assert row is None
