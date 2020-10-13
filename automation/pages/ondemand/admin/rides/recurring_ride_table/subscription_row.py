from pages.ondemand.admin.rides.deletion_modal import DeletionModal
from pages.ondemand.admin.rides.recurring_ride_table.kebab_menu import KebabMenu
from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from utilities import Component, Selector, Selectors, WebElement

from ..ride_subscription_details_modal.ride_subscription_details_modal import (
    RideSubscriptionDetailsModal,
)


class SubscriptionRow(Component):
    """Objects and methods for the Subscription Row component.

    Subscription rows may only be found within the RideSubscriptionTable component located on the
    Rides page. This table is generated when selecting 'Active', 'Upcoming', or 'Complete' under
    'Recurring Rides' within the side bar navigation panel.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-row')

    _subscription_drop_off: Selector = Selectors.data_id('subscription-dropoff')
    _subscription_end_date: Selector = Selectors.data_id('subscription-end-date')
    _subscription_id: Selector = Selectors.data_id('subscription-id')
    _subscription_kebab_menu: Selector = Selectors.data_id('subscription-kebab-menu')
    _subscription_pick_up: Selector = Selectors.data_id('subscription-pickup')
    _subscription_rider_name: Selector = Selectors.data_id('subscription-rider-name')
    _subscription_start_date: Selector = Selectors.data_id('subscription-start-date')
    _subscription_start_time: Selector = Selectors.data_id('subscription-start-time')
    _subscription_total_cancel: Selector = Selectors.data_id('subscription-total-cancel')
    _subscription_total_no_shows: Selector = Selectors.data_id('subscription-total-no-shows')

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def deletion_modal(self) -> DeletionModal:
        return DeletionModal(self)

    @property
    def details_modal(self) -> RideSubscriptionDetailsModal:
        return RideSubscriptionDetailsModal(self)

    @property
    def drop_off_address(self) -> str:
        return self.container.find_element(*self._subscription_drop_off).text

    @property
    def end_date(self) -> str:
        return self.container.find_element(*self._subscription_end_date).text

    @property
    def id(self) -> str:
        """Return the unique subscription ID for a subscription row.

        The get_attribute method is used instead of .text as the subscription id is a hidden
        attribute.
        """
        return self.container.find_element(*self._subscription_id).get_attribute('innerText')

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    @property
    def kebab_menu_button(self) -> WebElement:
        return self.container.find_element(*self._subscription_kebab_menu)

    @property
    def pick_up_address(self) -> str:
        return self.container.find_element(*self._subscription_pick_up).text

    @property
    def rider_name(self) -> str:
        return self.container.find_element(*self._subscription_rider_name).text

    @property
    def start_date(self) -> str:
        return self.container.find_element(*self._subscription_start_date).text

    @property
    def start_time(self) -> str:
        return self.container.find_element(*self._subscription_start_time).text

    @property
    def total_no_shows(self) -> str:
        return self.container.find_element(*self._subscription_total_no_shows).text

    @property
    def total_cancels(self) -> str:
        return self.container.find_element(*self._subscription_total_cancel).text

    def cancel_all_scheduled_rides(self) -> None:
        """Open the cancellation modal for a subscription row."""
        self.open_kebab_menu()
        self.kebab_menu.cancel_all_button.click()

    def open_kebab_menu(self) -> object:
        """Open the kebab menu for a subscription row."""
        self.kebab_menu_button.click()

        return KebabMenu(self).wait_for_component_to_be_present()
