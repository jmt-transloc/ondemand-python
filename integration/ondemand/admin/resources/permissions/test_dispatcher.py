import pytest
from pages.ondemand.admin.resources.devices.devices import Devices
from pages.ondemand.admin.resources.regions.regions import Regions
from pages.ondemand.admin.resources.resources import Resources
from pages.ondemand.admin.resources.settings.settings import Settings
from pages.ondemand.admin.resources.users.users import Users
from pages.ondemand.admin.resources.vehicles.vehicles import Vehicles
from pytest import fixture
from utilities.api_helpers.vehicles import VehiclesAPI


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.role_dispatcher
@pytest.mark.ui
class TestDispatcherPermissions:
    """Battery of tests for Dispatcher role permissions on the Resources page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Dispatcher role Resource page testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.API: VehiclesAPI = VehiclesAPI()
        self.devices: Devices = Devices(selenium)
        self.resources: Resources = Resources(selenium)
        self.regions: Regions = Regions(selenium)
        self.settings: Settings = Settings(selenium)
        self.users: Users = Users(selenium)
        self.vehicles: Vehicles = Vehicles(selenium)

    @pytest.mark.medium
    @pytest.mark.parametrize('tab_name', ['Devices', 'Regions', 'Settings', 'Users', 'Vehicles'])
    @pytest.mark.xfail(
        reason='Dispatchers can only view Vehicles and Devices on Dev.',
    )  # TODO(J. Thompson) Remove once fixed
    def test_view__access(self, tab_name: fixture) -> None:
        """Ensure that specific tabs are shown to role Dispatchers.

        :param tab_name: A list of tabs a Dispatcher should have access to.
        """
        self.resources.visit()

        assert tab_name in self.resources.sidebar.container.html

    @pytest.mark.medium
    @pytest.mark.parametrize('tab_name', ['Addresses'])
    @pytest.mark.xfail(
        reason='Dispatchers currently have access to Addresses.',
    )  # TODO(J. Thompson) Remove once fixed
    def test_view__no_access(self, tab_name: fixture) -> None:
        """Ensure that specific tabs are not shown to role Dispatchers.

        :param tab_name: A list of tabs a Dispatcher should not have access to.
        """
        self.resources.visit()

        assert tab_name not in self.resources.sidebar.container.html

    @pytest.mark.medium
    @pytest.mark.xfail(
        reason='Dispatchers currently do not have access to Regions on Dev.',
    )  # TODO(J. Thompson) Remove once fixed
    def test_update_regions__no_access(self) -> None:
        """Ensure that role Dispatcher does not have update permissions for Regions."""
        self.regions.visit()

        assert bool(self.regions.fab_button) is False

    @pytest.mark.medium
    @pytest.mark.xfail(
        reason='Dispatchers currently have access to update users.',
    )  # TODO(J. Thompson) Remove once fixed
    def test_update_users__no_access(self) -> None:
        """Ensure that role Dispatcher does not have update permissions for Users."""
        self.users.visit()

        assert bool(self.users.fab_button) is False

    @pytest.mark.medium
    def test_update_vehicles__access(self) -> None:
        """Ensure that role Dispatcher does have update permissions for Vehicles."""
        self.vehicles.visit()

        assert bool(self.vehicles.fab_button) is True
