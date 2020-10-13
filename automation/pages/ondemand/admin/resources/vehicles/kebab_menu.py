from pages.ondemand.admin.resources.vehicles.deletion_modal import DeletionModal
from pages.ondemand.admin.resources.vehicles.vehicle_form.vehicle_form import VehicleForm
from utilities import Component, Selector, Selectors, WebElement


class KebabMenu(Component):
    """Objects and methods for the Kebab Menu component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('kebab-menu-container')
    _delete_button: Selector = Selectors.data_id('delete-vehicle')
    _edit_button: Selector = Selectors.data_id('edit-vehicle')

    @property
    def delete_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def edit_button(self) -> WebElement:
        return self.container.find_element(*self._edit_button)

    def delete_vehicle(self) -> object:
        """Open the deletion modal for a vehicle row."""
        self.delete_button.click()

        return DeletionModal(self).wait_for_component_to_be_present()

    def edit_vehicle(self) -> object:
        """Open the edit view for a vehicle row."""
        self.edit_button.click()

        return VehicleForm(self).wait_for_component_to_be_present()
