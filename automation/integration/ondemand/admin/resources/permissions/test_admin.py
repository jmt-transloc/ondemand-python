import pytest
from pages.ondemand.admin.resources.addresses.addresses import Addresses
from pages.ondemand.admin.resources.devices.devices import Devices
from pages.ondemand.admin.resources.regions.regions import Regions
from pages.ondemand.admin.resources.resources import Resources
from pages.ondemand.admin.resources.settings.settings import Settings
from pages.ondemand.admin.resources.users.users import Users
from pages.ondemand.admin.resources.vehicles.vehicles import Vehicles
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.role_admin
@pytest.mark.ui
class TestAdminPermissions:
    """Battery of tests for Admin role permissions on the Resources page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Admin role Resource page testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.addresses: Addresses = Addresses(selenium)
        self.devices: Devices = Devices(selenium)
        self.resources: Resources = Resources(selenium)
        self.regions: Regions = Regions(selenium)
        self.settings: Settings = Settings(selenium)
        self.users: Users = Users(selenium)
        self.vehicles: Vehicles = Vehicles(selenium)

    @pytest.mark.medium
    @pytest.mark.parametrize(
        'tab_name', ['Addresses', 'Devices', 'Regions', 'Settings', 'Users', 'Vehicles'],
    )
    def test_view__access(self, tab_name: fixture) -> None:
        """Ensure that specific tabs are shown to role Admins.

        :param tab_name: A list of tabs an Admin should have access to.
        """
        self.resources.visit()

        assert tab_name in self.resources.sidebar.container.html

    @pytest.mark.medium
    def test_update_addresses__access(self) -> None:
        """Ensure that role Admin does have update permissions for Addresses."""
        self.addresses.visit()

        assert bool(self.addresses.fab_button) is True

    @pytest.mark.medium
    def test_update_regions__access(self) -> None:
        """Ensure that role Admin does have update permissions for Regions."""
        self.regions.visit()

        assert bool(self.regions.fab_button) is True

    @pytest.mark.medium
    def test_update_users__access(self) -> None:
        """Ensure that role Admin does have update permissions for Users."""
        self.users.visit()

        assert bool(self.users.fab_button) is True

    @pytest.mark.medium
    def test_update_vehicles__access(self) -> None:
        """Ensure that role Admin does have update permissions for Vehicles."""
        self.vehicles.visit()

        assert bool(self.vehicles.fab_button) is True
