from pages.ondemand.admin.resources.resources import Resources
from pages.ondemand.admin.resources.vehicles.deletion_modal import DeletionModal
from pages.ondemand.admin.resources.vehicles.vehicle_form.vehicle_form import VehicleForm
from pages.ondemand.admin.resources.vehicles.vehicles_list import VehiclesList
from utilities.driver_helpers.selectors import Selector, Selectors
from utilities.driver_helpers.types import WebElement


class Vehicles(Resources):
    """Objects and methods for the Vehicles page.

    The vehicles page may be accessed by selecting the 'Vehicles' tab from the side navigation
    panel on the 'Resources' page.
    """

    URL_PATH: str = f'{Resources.URL_PATH}/vehicles'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
    _fab_button: Selector = Selectors.data_id('new-button')

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def fab_button(self) -> WebElement:
        return self.driver.find_element(*self._fab_button)

    @property
    def vehicle_form(self) -> VehicleForm:
        return VehicleForm(self)

    @property
    def vehicles_list(self) -> VehiclesList:
        return VehiclesList(self)

    def add_new_vehicle(self, vehicle: dict) -> None:
        """Add a new vehicle using the Vehicle Form component.

        :param vehicle: The vehicle yielded from a vehicle fixture.
        """
        self.fab_button.click()

        self.vehicle_form.wait_for_component_to_be_present()
        self.vehicle_form.fill_form(vehicle)
        self.vehicle_form.save_button.click()

        self.driver.wait_until_not_present(*VehicleForm.ROOT_LOCATOR, wait_time=4)

    def delete_vehicle(self) -> object:
        """Delete an existing vehicle."""
        self.vehicle_form.wait_for_component_to_be_visible()

        self.vehicle_form.delete_vehicle_button.click()

        return self.deletion_modal.wait_for_component_to_be_visible()

    def toggle_vehicle_operation(self) -> None:
        """Toggle an existing vehicle's operational slider."""
        self.vehicle_form.operational_toggle.click()

        self.vehicle_form.operational_toggle.is_selected()
