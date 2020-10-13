from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from utilities import Component, Selector, Selectors, WebElement


class ScheduledRideRow(Component):
    """Objects and methods for a Scheduled Ride row."""

    ROOT_LOCATOR: Selector = Selectors.data_id('scheduled-ride')
    _cancel_button: Selector = Selectors.data_id('cancel-scheduled-ride')
    _confirm_delete_button: Selector = Selectors.data_id('confirm-delete-scheduled-ride')
    _date: Selector = Selectors.data_id('scheduled-ride-date')
    _day: Selector = Selectors.data_id('scheduled-ride-day')
    _delete_button: Selector = Selectors.data_id('delete-scheduled-ride')
    _details_link: Selector = Selectors.data_id('scheduled-ride-details-link')
    _no_service_tooltip: Selector = Selectors.data_id('scheduled-ride-no-service-tooltip')
    _ride_id: Selector = Selectors.data_id('scheduled-ride-id')
    _status: Selector = Selectors.data_id('scheduled-ride-status')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def confirm_delete_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_delete_button)

    @property
    def date(self) -> str:
        return self.container.find_element(*self._date).text

    @property
    def day(self) -> str:
        return self.container.find_element(*self._day).text

    @property
    def delete_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def details_link(self) -> WebElement:
        return self.container.find_element(*self._details_link)

    @property
    def no_service_tooltip(self) -> WebElement:
        return self.container.find_element(*self._no_service_tooltip)

    @property
    def ride_id(self) -> str:
        """Return the unique ride ID for a scheduled ride row.

        The get_attribute method is used instead of .text as the service_id is a hidden
        attribute.
        """
        return self.container.find_element(*self._ride_id).get_attribute('innerText')

    @property
    def status(self) -> str:
        return self.container.find_element(*self._status).text

    def cancel_ride(self, reason: str) -> None:
        """Cancel a ride by selecting cancel, then confirm the ride cancellation.

        :param reason: The reason for cancelling a ride.
        """
        self.cancel_button.click()

        self.cancellation_modal.wait_for_component_to_be_present()
        self.cancellation_modal.cancel_ride(reason)
        self.cancellation_modal.wait_for_component_to_not_be_visible()

    def delete_ride(self) -> None:
        """Delete a ride by selecting delete, then confirm the ride deletion."""
        self.delete_button.click()

        confirm_button: WebElement = self.container.wait_until_present(*self._confirm_delete_button)
        confirm_button.click()

        self.container.wait_until_not_present(*self._confirm_delete_button)
