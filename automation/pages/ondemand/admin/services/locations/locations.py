from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.services.locations.addresses_list import AddressesList
from pages.ondemand.admin.services.locations.regions_list import RegionsList
from utilities import Selector, Selectors, WebElement


class Locations(Base):
    """Locations Page objects and methods for the OnDemand Admin application.

    The Locations page may be accessed by navigating to the Services page, selecting a service, then
    selecting the map.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('locations-page-container')
    _addresses_list_button: Selector = Selectors.data_id('addresses-list-button')
    _back_button: Selector = Selectors.data_id('back-button')
    _regions_list_button: Selector = Selectors.data_id('regions-list-button')
    _save_button: Selector = Selectors.data_id('save-button')

    @property
    def addresses_button(self) -> WebElement:
        return self.driver.find_element(*self._addresses_list_button)

    @property
    def addresses_list(self) -> AddressesList:
        return AddressesList(self)

    @property
    def back_button(self) -> WebElement:
        return self.driver.find_element(*self._back_button)

    @property
    def regions_button(self) -> WebElement:
        return self.driver.find_element(*self._regions_list_button)

    @property
    def regions_list(self) -> RegionsList:
        return RegionsList(self)

    @property
    def save_button(self) -> WebElement:
        return self.driver.find_element(*self._save_button)

    def open_addresses_list(self) -> object:
        """Open the address list component."""
        self.addresses_button.click()

        return AddressesList(self).wait_for_component_to_be_present()

    def open_regions_list(self) -> object:
        """Open the region list component."""
        self.regions_button.click()

        return RegionsList(self).wait_for_component_to_be_present()
