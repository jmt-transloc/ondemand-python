from pages.ondemand.admin.dispatch.book_a_ride.recurring_rides.subscription_errors import (
    SubscriptionErrors,
)
from pages.ondemand.common.recurring_rides.ride_placard import RidePlacard
from utilities import Component, Selector, Selectors, WebElement


class RideSubscriptionModal(Component):
    """Objects and methods for the recurring rides subscription modal."""

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-modal-container')
    _confirm_button: Selector = Selectors.data_id('subscription-modal-confirm-button')
    _message: Selector = Selectors.data_id('subscription-modal-message')
    _rides_error_message: Selector = Selectors.data_id('rides-scheduled-with-errors-message')
    _rides_link: Selector = Selectors.data_id('subscription-modal-rides-link')
    _rides_success_message: Selector = Selectors.data_id('rides-scheduled-message')

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def message(self) -> str:
        return self.container.find_element(*self._message).text

    @property
    def rides_page_link(self) -> WebElement:
        return self.container.find_element(*self._rides_link)

    @property
    def ride_placard(self) -> RidePlacard:
        return RidePlacard(self)

    @property
    def subscription_errors(self) -> SubscriptionErrors:
        return SubscriptionErrors(self)
