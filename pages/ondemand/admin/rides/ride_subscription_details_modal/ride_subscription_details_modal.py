from pages.ondemand.admin.rides.deletion_modal import DeletionModal
from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from pages.ondemand.common.recurring_rides.ride_placard import RidePlacard
from utilities import Component, Selector, Selectors, WebElement

from .scheduled_rides_list import ScheduledRidesList


class RideSubscriptionDetailsModal(Component):
    """Objects and methods for the Ride Subscription Details modal."""

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-modal-details-container')
    _back_button: Selector = Selectors.data_id('subscription-modal-back-button')
    _cancel_all_button: Selector = Selectors.data_id('subscription-modal-cancel-all')
    _summary: Selector = Selectors.data_id('subscription-modal-summary')

    @property
    def back_button(self) -> WebElement:
        return self.container.find_element(*self._back_button)

    @property
    def cancel_all_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_all_button)

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def ride_placard(self) -> RidePlacard:
        return RidePlacard(self)

    @property
    def scheduled_rides_list(self) -> ScheduledRidesList:
        return ScheduledRidesList(self)

    @property
    def summary(self) -> str:
        return self.container.find_element(*self._summary).text

    def cancel_all_rides(self, reason: str) -> None:
        """Cancel all scheduled rides for a recurring ride request.

        :param reason: The reason for cancelling a ride.
        """
        self.cancel_all_button.click()

        self.cancellation_modal.cancel_ride(reason)
        self.cancellation_modal.wait_for_component_to_not_be_visible()

    def delete_all_rides(self) -> None:
        """Delete all scheduled rides for a recurring ride request."""
        self.cancel_all_button.click()

        self.deletion_modal.confirm_button.click()
        self.deletion_modal.wait_for_component_to_not_be_visible()
