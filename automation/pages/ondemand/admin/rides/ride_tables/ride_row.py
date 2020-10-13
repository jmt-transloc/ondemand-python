from utilities import Component, Selector, Selectors, WebElement


class RideRow(Component):
    """Objects and methods for an individual Ride table row.

    Ride rows contain information for the ride, a cancellation button, and a details button.
    Selecting the cancellation button raises a modal while selecting the details button redirects
    to the Details page for the specific ride.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('rides-table-row')
    _ride_name: Selector = Selectors.data_id('ride-name')
    _ride_pickup_address: Selector = Selectors.data_id('ride-pickup-address')
    _ride_dropoff_address: Selector = Selectors.data_id('ride-dropoff-address')
    _ride_id: Selector = Selectors.data_id('ride-id')
    _ride_status: Selector = Selectors.data_id('ride-status')
    _ride_time: Selector = Selectors.data_id('ride-time')
    _ride_cancel_button: Selector = Selectors.data_id('ride-cancel-button')
    _ride_details_button: Selector = Selectors.data_id('ride-details-button')

    @property
    def ride_name(self) -> str:
        return self.container.find_element(*self._ride_name).text

    @property
    def ride_pickup_address(self) -> str:
        return self.container.find_element(*self._ride_pickup_address).text

    @property
    def ride_dropoff_address(self) -> str:
        return self.container.find_element(*self._ride_dropoff_address).text

    @property
    def ride_id(self) -> str:
        """Return the unique ride ID for a ride row.

        The get_attribute method is used instead of .text as the ride_id is a hidden attribute.
        """
        return self.container.find_element(*self._ride_id).get_attribute('innerText')

    @property
    def ride_status(self) -> str:
        return self.container.find_element(*self._ride_status).text

    @property
    def ride_time(self) -> str:
        return self.container.find_element(*self._ride_time).text

    @property
    def ride_cancel_button(self) -> WebElement:
        return self.container.find_element(*self._ride_cancel_button)

    @property
    def ride_details_button(self) -> WebElement:
        return self.container.find_element(*self._ride_details_button)
