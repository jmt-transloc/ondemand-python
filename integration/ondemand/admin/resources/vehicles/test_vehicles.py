import pytest
from factory import Factory
from pages.ondemand.admin.resources.vehicles.vehicle_row import VehicleRow
from pages.ondemand.admin.resources.vehicles.vehicles import Vehicles
from pytest import fixture
from utilities.api_helpers.services import ServicesAPI
from utilities.api_helpers.vehicles import VehiclesAPI


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestVehicles:
    """Battery of tests for Vehicles page functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.vehicles: Vehicles = Vehicles(selenium)
        self.API: VehiclesAPI = VehiclesAPI()
        self.services_API: ServicesAPI = ServicesAPI()

    @pytest.mark.high
    @pytest.mark.parametrize('vehicle_type', ['accessible', 'non-accessible'])
    @pytest.mark.smoke
    def test_add_vehicle(self, vehicle_factory: Factory, vehicle_type: fixture) -> None:
        """Input valid vehicle data, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        vehicle: dict

        if vehicle_type == 'accessible':
            vehicle = vehicle_factory.build(wheelchair_vehicle=True)
        else:
            vehicle = vehicle_factory.build()

        self.vehicles.visit()

        self.vehicles.add_new_vehicle(vehicle)
        row = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)

        assert vehicle['call_name'] in row.vehicle_call_name

        vehicle['vehicle_id'] = row.vehicle_id
        self.API.delete_vehicle(vehicle)

    @pytest.mark.medium
    def test_edit_existing_vehicle(self, vehicle: fixture) -> None:
        """Yield a vehicle from the API, edit a field, then check for a success state."""
        self.vehicles.visit()
        row = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)

        before_capacity: str = row.vehicle_capacity
        row.container.click()

        self.vehicles.vehicle_form.wait_for_component_to_be_present()
        self.vehicles.vehicle_form.capacity_field.fill('10')
        self.vehicles.vehicle_form.save_button.click()
        self.vehicles.vehicle_form.wait_for_component_to_not_be_visible()

        after_capacity: str = row.vehicle_capacity

        assert before_capacity != after_capacity

    @pytest.mark.low
    def test_delete_existing_vehicle(self, vehicle_factory: Factory) -> None:
        """Yield a vehicle from the API, delete the vehicle, then check for a success state."""
        vehicle: dict = vehicle_factory.create()
        self.vehicles.visit()

        before_row: VehicleRow = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)
        before_row.container.click()

        self.vehicles.vehicle_form.wait_for_component_to_be_visible()
        self.vehicles.delete_vehicle()
        self.vehicles.deletion_modal.confirm_button.click()

        after_row: VehicleRow = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)

        assert after_row is None

    @pytest.mark.medium
    def test_disable_existing_vehicle(self, vehicle: fixture) -> None:
        """Yield a vehicle from the API, disable the vehicle, then check for a success state."""
        self.vehicles.visit()
        row: VehicleRow = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)

        before_enabled: str = row.enabled
        row.container.click()

        self.vehicles.vehicle_form.wait_for_component_to_be_visible()
        self.vehicles.toggle_vehicle_operation()
        self.vehicles.vehicle_form.save_button.click()

        after_enabled: str = row.enabled

        assert before_enabled != after_enabled

    @pytest.mark.low
    def test_vehicles_display_assigned_services(
        self, service_factory: Factory, vehicle: fixture,
    ) -> None:
        """Yield a vehicle from the API, assign a service, then check for a success state."""
        vehicle_id = vehicle['vehicle_id']
        service: dict = service_factory.create(vehicles=[vehicle_id])

        self.vehicles.visit()
        row: VehicleRow = self.vehicles.vehicles_list.surface_vehicle_row(vehicle)
        row.container.click()

        assigned = self.vehicles.vehicle_form.assigned_services_list.surface_assigned_service(
            service['service_id'],
        )

        assert assigned is not False

        self.services_API.delete_service(service)
