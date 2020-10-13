from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from utilities import Component, Selector, Selectors, WebElement


class RideOverviewModal(Component):
    """Objects and methods for the Ride Overview Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-overview-container')
    _cancel_ride_button: Selector = Selectors.data_id('cancel-ride-button')
    _capacity_details: Selector = Selectors.data_id('capacity-details')
    _drop_off_details: Selector = Selectors.data_id('dropoff-details')
    _pick_up_details: Selector = Selectors.data_id('pickup-details')
    _pick_up_time_details: Selector = Selectors.data_id('pickup-time-details')

    @property
    def cancel_ride_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_ride_button)

    @property
    def capacity(self) -> str:
        return self.container.find_element(*self._capacity_details).text

    @property
    def drop_off(self) -> str:
        return self.container.find_element(*self._drop_off_details).text

    @property
    def pick_up(self) -> str:
        return self.container.find_element(*self._pick_up_details).text

    @property
    def wait_time(self) -> str:
        return self.container.find_element(*self._pick_up_time_details).text

    def cancel_ride(self) -> object:
        """Cancel a ride by selecting the cancel button."""
        self.cancel_ride_button.click()

        return CancellationModal(self).wait_for_component_to_be_present()
