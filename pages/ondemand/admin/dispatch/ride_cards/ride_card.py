from pages.ondemand.admin.dispatch.ride_cards.kebab_menu import KebabMenu
from pages.ondemand.admin.dispatch.ride_prioritization.ride_prioritization_modal import (
    RidePrioritizationModal,
)
from utilities import Component, Selector, Selectors, WebElement


class RideCard(Component):
    """Objects and methods for an individual Ride Card."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-card')
    card_locator: Selector = Selectors.data_id('ride-card')
    _drop_off_prioritized: Selector = Selectors.data_id('dropoff-prioritized')
    _entire_ride_prioritized: Selector = Selectors.data_id('entire-ride-prioritized')
    _kebab_menu: Selector = Selectors.data_id('ride-card-kebab-menu-button')
    _pick_up_prioritized: Selector = Selectors.data_id('pickup-prioritized')
    _ride_drop_off: Selector = Selectors.data_id('ride-card-drop-off-address')
    _ride_drop_off_time: Selector = Selectors.data_id('ride-card-drop-off-time')
    _ride_email: Selector = Selectors.data_id('ride-card-email')
    _ride_id: Selector = Selectors.data_id('ride-card-ride-id')
    _ride_note: Selector = Selectors.data_id('ride-card-driver-note')
    _ride_pick_up: Selector = Selectors.data_id('ride-card-pick-up-address')
    _ride_pick_up_time: Selector = Selectors.data_id('ride-card-pick-up-time')
    _ride_status: Selector = Selectors.data_id('ride-card-ride-status')
    _ride_wait: Selector = Selectors.data_id('ride-card-ride-wait')
    _rider_name: Selector = Selectors.data_id('ride-card-rider-name')
    _rider_phone: Selector = Selectors.data_id('ride-card-phone')

    @property
    def kebab_menu(self) -> KebabMenu:
        return KebabMenu(self)

    @property
    def prioritization_modal(self) -> RidePrioritizationModal:
        return RidePrioritizationModal(self)

    @property
    def rider_name(self) -> str:
        return self.container.find_element(*self._rider_name).text

    @property
    def drop_off_address(self) -> str:
        return self.container.find_element(*self._ride_drop_off).text

    @property
    def drop_off_time(self) -> str:
        return self.container.find_element(*self._ride_drop_off_time).text

    @property
    def email(self) -> str:
        """Return the rider email for a ride card.

        The get_attribute method is used instead of .text as the email is a hidden attribute.
        """
        return self.container.find_element(*self._ride_email).get_attribute('innerText')

    @property
    def note(self) -> str:
        return self.container.find_element(*self._ride_note).text

    @property
    def phone(self) -> str:
        return self.container.find_element(*self._rider_phone).text

    @property
    def pick_up_address(self) -> str:
        return self.container.find_element(*self._ride_pick_up).text

    @property
    def pick_up_time(self) -> str:
        return self.container.find_element(*self._ride_pick_up_time).text

    @property
    def ride_status(self) -> str:
        return self.container.find_element(*self._ride_status).text

    @property
    def ride_wait(self) -> str:
        return self.container.find_element(*self._ride_wait).text

    @property
    def ride_card_kebab_button(self) -> WebElement:
        return self.container.find_element(*self._kebab_menu)

    @property
    def ride_id(self) -> str:
        """Return the unique ride ID for a ride card.

        The get_attribute method is used instead of .text as the ride_id is a hidden attribute.
        """
        return self.container.find_element(*self._ride_id).get_attribute('innerText')

    def drop_off_prioritized(self) -> WebElement:
        return self.container.wait_until_present(*self._drop_off_prioritized)

    def entire_ride_prioritized(self) -> WebElement:
        return self.container.wait_until_present(*self._entire_ride_prioritized)

    def pick_up_prioritized(self) -> WebElement:
        return self.container.wait_until_present(*self._pick_up_prioritized)

    def open_kebab_menu(self) -> object:
        """Find and open a ride card kebab menu.

        :returns KebabMenu: An instance of the ride's Kebab Menu.
        """
        self.ride_card_kebab_button.click()

        return KebabMenu(self).wait_for_component_to_be_present()
