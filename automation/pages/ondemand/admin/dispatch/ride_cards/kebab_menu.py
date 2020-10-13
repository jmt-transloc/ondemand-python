from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.dispatch.ride_prioritization.ride_prioritization_modal import (
    RidePrioritizationModal,
)
from utilities import Component, Selector, Selectors, WebElement


class KebabMenu(Component):
    """Objects and methods for a Ride Card Kebab Menu.

    The Kebab Menu allows administrators to cancel, prioritize, or edit rides.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-card-kebab-menu')
    _cancel_ride_button: Selector = Selectors.data_id('kebab-cancel-ride')
    _disabled_prioritize_ride_button: Selector = Selectors.data_id('kebab-disable-prioritize')
    _prioritize_ride_button: Selector = Selectors.data_id('kebab-prioritize-ride')
    _ride_details_button: Selector = Selectors.data_id('kebab-ride-details')

    @property
    def cancel_ride_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_ride_button)

    @property
    def prioritize_ride_button(self) -> WebElement:
        return self.container.find_element(*self._prioritize_ride_button)

    @property
    def ride_details_button(self) -> WebElement:
        return self.container.find_element(*self._ride_details_button)

    @property
    def ride_details_link(self) -> str:
        return self.ride_details_button.get_attribute('href')

    def prioritize_disabled(self) -> WebElement:
        return self.container.wait_until_present(*self._disabled_prioritize_ride_button)

    def navigate_to_ride_details(self) -> object:
        """Navigate to the Details Page link.

        Selecting the ride_details_link element opens a new tab. To get around this, we save the
        link URL, then input the str to the Web Driver.

        :returns Details: An instance of the Ride Details page.
        """
        ride_details_url = self.ride_details_link
        self.driver.get(ride_details_url)

        return Details(self.driver, ride_details_url).wait_for_page_to_load()

    def open_ride_prioritization_modal(self) -> object:
        """Find and open a ride card ride prioritization modal.

        :returns RidePrioritizationModal: An instance of the ride's Ride Prioritization Modal.
        """
        self.prioritize_ride_button.click()

        return RidePrioritizationModal(self).wait_for_component_to_be_visible()
