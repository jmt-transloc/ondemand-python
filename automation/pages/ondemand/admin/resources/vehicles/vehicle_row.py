from pages.ondemand.admin.resources.vehicles.kebab_menu import KebabMenu
from utilities import Component, Selector, Selectors, WebElement


class VehicleRow(Component):
    """Vehicle Row component objects and methods for the Vehicles Page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('vehicle-row')
    _color: Selector = Selectors.data_id('color')
    _enabled: Selector = Selectors.data_id('operational')
    _kebab_button: Selector = Selectors.data_id('kebab-button')
    _vehicle_call_name: Selector = Selectors.data_id('vehicle-call-name')
    _vehicle_capacity: Selector = Selectors.data_id('ambulatory-capacity')
    _vehicle_id: Selector = Selectors.data_id('row-id')
    _wheelchair_capacity: Selector = Selectors.data_id('accessible-capacity')
    _wheelchair_impact: Selector = Selectors.data_id('capacity-impact')

    @property
    def vehicle_id(self) -> str:
        """Return the unique vehicle ID for a vehicle row.

        The get_attribute method is used instead of .text as the vehicle_id is a hidden attribute.
        """
        return self.container.find_element(*self._vehicle_id).get_attribute('innerText')

    @property
    def color(self) -> WebElement:
        return self.container.find_element(*self._color)

    @property
    def enabled(self) -> str:
        return self.container.find_element(*self._enabled).text

    @property
    def kebab_button(self) -> WebElement:
        return self.container.find_element(*self._kebab_button)

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    @property
    def vehicle_call_name(self) -> str:
        return self.container.find_element(*self._vehicle_call_name).text

    @property
    def vehicle_capacity(self) -> str:
        return self.container.find_element(*self._vehicle_capacity).text

    @property
    def wheelchair_capacity(self) -> str:
        return self.container.find_element(*self._wheelchair_capacity).text

    @property
    def wheelchair_impact(self) -> str:
        return self.container.find_element(*self._wheelchair_impact).text

    def open_kebab_menu(self) -> object:
        """Open the kebab menu for a vehicle row."""
        self.kebab_button.click()

        return KebabMenu(self).wait_for_component_to_be_present()
