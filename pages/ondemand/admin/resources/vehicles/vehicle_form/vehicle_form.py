from pages.ondemand.admin.resources.vehicles.vehicle_form.assigned_services import (
    AssignedServicesList,
)
from utilities.driver_helpers.selectors import Selector, Selectors
from utilities.driver_helpers.types import WebElement
from utilities.page_object_models.component import Component


class VehicleForm(Component):
    """Objects and methods for the Deletion Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('vehicle-container')

    _call_name_field: Selector = Selectors.data_id('vehicle-call-name')
    _cancel_button: Selector = Selectors.data_id('cancel-button')
    _capacity_field: Selector = Selectors.data_id('ambulatory-capacity')
    _color_picker: Selector = Selectors.data_id('color')
    _delete_vehicle_button: Selector = Selectors.data_id('delete-vehicle-button')
    _operational_toggle: Selector = Selectors.name('enabled')
    _save_button: Selector = Selectors.data_id('save-vehicle-button')
    _wheelchair_capacity: Selector = Selectors.data_id('accessible-capacity')
    _wheelchair_impact: Selector = Selectors.data_id('capacity-impact')

    @property
    def assigned_services_list(self) -> AssignedServicesList:
        return AssignedServicesList(self)

    @property
    def call_name_field(self) -> WebElement:
        return self.container.find_element(*self._call_name_field)

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def capacity_field(self) -> WebElement:
        return self.container.find_element(*self._capacity_field)

    @property
    def color_picker(self) -> WebElement:
        return self.container.find_element(*self._color_picker)

    @property
    def delete_vehicle_button(self) -> WebElement:
        return self.container.find_element(*self._delete_vehicle_button)

    @property
    def operational_toggle(self) -> WebElement:
        return self.container.find_element(*self._operational_toggle)

    @property
    def save_button(self) -> WebElement:
        return self.container.find_element(*self._save_button)

    @property
    def wheelchair_capacity_field(self) -> WebElement:
        return self.container.find_element(*self._wheelchair_capacity)

    @property
    def wheelchair_impact_field(self) -> WebElement:
        return self.container.find_element(*self._wheelchair_impact)

    def fill_form(self, vehicle: dict) -> None:
        """Fill out a vehicle form, then submit the form.

        :param vehicle: The vehicle yielded from a vehicle fixture.
        """
        self.call_name_field.fill(vehicle['call_name'])
        self.capacity_field.fill(vehicle['capacity'])
        self.wheelchair_capacity_field.fill(vehicle['wheelchair_capacity'])

        if vehicle['wheelchair_capacity'] >= 1:
            self.wheelchair_impact_field.fill(vehicle['wheelchair_impact'])
        self.operational_toggle.click()
