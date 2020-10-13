import pytest
from pages.ondemand.admin.services.locations.locations import Locations
from pages.ondemand.admin.services.services import Services
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestServiceLocations:
    """Battery of tests for service location functionality."""

    @pytest.fixture
    def navigate_to_service(self, service: fixture) -> None:
        """Navigate to the locations page for a yielded service."""
        self.service.navigate_to_locations_by_service(service)

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in service location testing."""
        self.service = Services(selenium)
        self.locations = Locations(selenium)

    @pytest.mark.medium
    @pytest.mark.parametrize('mark', ['pickup', 'dropoff'])
    def test_mark_address_location(
        self, address: fixture, mark: fixture, navigate_to_service: fixture,
    ) -> None:
        """Mark an address as a pick up or drop off, then check for a success state."""
        self.locations.open_addresses_list()
        card = self.locations.addresses_list.surface_location_card(address['name'])

        if mark == 'pickup':
            card.pick_up_checkbox.click()
        else:
            card.drop_off_checkbox.click()

        self.locations.save_button.click()

        if mark == 'pickup':
            assert card.pick_up_checkbox.is_selected()
        else:
            assert card.drop_off_checkbox.is_selected()

    @pytest.mark.parametrize('mark', ['pickup', 'dropoff'])
    def test_mark_region_location(
        self, region: fixture, mark: fixture, navigate_to_service: fixture,
    ) -> None:
        """Mark a region as a pick up or drop off, then check for a success state."""
        self.locations.open_regions_list()
        card = self.locations.regions_list.surface_location_card(region['name'])

        if mark == 'pickup':
            card.pick_up_checkbox.click()
        else:
            card.drop_off_checkbox.click()

        self.locations.save_button.click()

        if mark == 'pickup':
            assert card.pick_up_checkbox.is_selected()
        else:
            assert card.drop_off_checkbox.is_selected()
