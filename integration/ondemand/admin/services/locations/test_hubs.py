import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pages.ondemand.admin.services.locations.locations import Locations
from pages.ondemand.admin.services.services import Services
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestHubs:
    """Battery of tests for service location hub functionality."""

    @pytest.fixture
    def navigate_to_service(self, service: fixture) -> None:
        """Navigate to the locations page for a yielded service."""
        self.service.navigate_to_locations_by_service(service)

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in service location testing."""
        self.dispatch = Dispatch(selenium)
        self.locations = Locations(selenium)
        self.service = Services(selenium)

    @pytest.mark.low
    def test_address_can_be_hubs(self, address: fixture, navigate_to_service: fixture) -> None:
        """Open the address list and ensure that addresses can be marked as hubs."""
        self.locations.open_addresses_list()
        card = self.locations.addresses_list.surface_location_card(address['name'])

        assert card.hub_field.visible is True

    @pytest.mark.high
    def test_regions_cannot_be_hubs(self, region: fixture, navigate_to_service: fixture) -> None:
        """Open the region list and ensure that regions cannot be marked as hubs."""
        self.locations.open_regions_list()
        card = self.locations.regions_list.surface_location_card(region['name'])

        assert card.hub_card() is None

    @pytest.mark.high
    def test_add_address_as_hub(self, address: fixture, navigate_to_service: fixture) -> None:
        """Mark an address location as a hub, then check for a success state."""
        self.locations.open_addresses_list()
        card = self.locations.addresses_list.surface_location_card(address['name'])
        card.container.mouse_over()
        card.hub_checkbox.click()

        self.locations.save_button.click()

        assert card.hub_checkbox.checked is True

    @pytest.mark.medium
    def test_hub_disables_pu_do(self, service_with_hub_address: fixture) -> None:
        """Locate a hub address and ensure that pick up and drop off are disabled."""
        self.service.navigate_to_locations_by_service(service_with_hub_address)
        self.locations.open_addresses_list()

        card = self.locations.addresses_list.surface_location_card(
            address_label='Stop #300 - TransLoc Office',
        )
        card.container.mouse_over()

        assert (card.pick_up_checkbox.is_enabled() and card.drop_off_checkbox.is_enabled()) is False

    @pytest.mark.high
    def test_remove_address_as_hub(self, service_with_hub_address: fixture) -> None:
        """Locate a hub address, remove the hub mark, then check for a success state.

        When hubs are removed, the PU/DO inputs should remain in a checked state. However, both
        fields should no longer be disabled. This test should utilize the .is_enabled() method
        once hub has been removed to ensure it equals True.
        """
        self.service.navigate_to_locations_by_service(service_with_hub_address)
        self.locations.open_addresses_list()

        card = self.locations.addresses_list.surface_location_card(
            address_label='Stop #300 - TransLoc Office',
        )
        card.container.mouse_over()
        card.hub_checkbox.click()

        self.locations.save_button.click()

        assert card.hub_checkbox.checked is False

    @pytest.mark.high
    def test_hubs_must_be_used__success(
        self, ride_factory: Factory, service_with_hub_address: fixture,
    ) -> None:
        """Build a ride using a hub address as PU/DO, then check for a success state."""
        ride = ride_factory.build(hub_ride=True)
        rider: dict = ride['rider']
        rider_name: str = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()
        self.dispatch.fill_ride_form(service_with_hub_address, ride=ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        card = self.dispatch.ride_card_panel.surface_ride_card(ride)
        assert card.rider_name == rider_name

    @pytest.mark.high
    def test_hubs_must_be_used__failure(
        self, ride_factory: Factory, service_with_hub_address: fixture,
    ) -> None:
        """Build a ride using a non-hub address as PU/DO, then check for a failure state."""
        ride = ride_factory.build(hub_ride=False)

        self.dispatch.visit()
        self.dispatch.fill_ride_form(service_with_hub_address, ride=ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert self.dispatch.ride_booking_panel.ride_form.service_error_check() is True
