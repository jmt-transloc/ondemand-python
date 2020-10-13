from pages.ondemand.web.booking.book_a_ride.ride_overview_modal import RideOverviewModal
from utilities import Component, Selector, Selectors, WebElement


class RideRow(Component):
    """Objects and methods for the Ride Row component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-list-row')
    _ride_drop_off: Selector = Selectors.data_id('ride-row-drooff-address')
    _ride_fare: Selector = Selectors.data_id('ride-row-fare')
    _ride_id: Selector = Selectors.data_id('ride-row-id')
    _ride_overview_button: Selector = Selectors.data_id('ride-overview-button')
    _ride_pick_up: Selector = Selectors.data_id('ride-row-pickup-address')
    _ride_status: Selector = Selectors.data_id('ride-row-status')

    @property
    def drop_off_address(self) -> str:
        return self.container.find_element(*self._ride_drop_off).text

    @property
    def fare(self) -> str:
        return self.container.find_element(*self._ride_fare).text

    @property
    def pick_up_address(self) -> str:
        return self.container.find_element(*self._ride_pick_up).text

    @property
    def ride_details_button(self) -> WebElement:
        return self.container.find_element(*self._ride_overview_button)

    @property
    def ride_id(self) -> str:
        """Return the unique ride ID for a ride row.

        The get_attribute method is used instead of .text as the ride_id is a hidden attribute.
        """
        return self.container.find_element(*self._ride_id).get_attribute('innerText')

    @property
    def status(self) -> str:
        return self.container.find_element(*self._ride_status).text

    def open_ride_overview(self) -> object:
        """Navigate to the ride overview modal for a ride."""
        self.ride_details_button.click()

        return RideOverviewModal(self).wait_for_component_to_be_present()
