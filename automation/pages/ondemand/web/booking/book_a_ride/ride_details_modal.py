from pages.ondemand.web.booking.book_a_ride.address_input import AddressInput
from pages.ondemand.web.booking.book_a_ride.passenger_details_modal import PassengerDetailsModal
from pages.ondemand.web.booking.book_a_ride.ride_overview_modal import RideOverviewModal
from pages.ondemand.web.booking.pickup_time_modal.pickup_time_modal import PickupTimeModal
from utilities import Component, Selector, Selectors, WebElement


class RideDetailsModal(Component):
    """Objects and methods for the Ride Details Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-details-container')
    _capacity_details: Selector = Selectors.data_id('capacity-details')
    _confirm_button: Selector = Selectors.data_id('confirm-ride-button')
    _drop_off_details: Selector = Selectors.data_id('dropoff-details')
    _edit_capacity: Selector = Selectors.data_id('edit-capacity')
    _edit_pu_do_button: Selector = Selectors.data_id('edit-pudo')
    _edit_time_button: Selector = Selectors.data_id('edit-datetime')
    _pick_up_details: Selector = Selectors.data_id('pickup-details')
    _pick_up_time_details: Selector = Selectors.data_id('pickup-time-details')

    @property
    def capacity(self) -> str:
        return self.container.find_element(*self._capacity_details).text

    @property
    def confirm_ride_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def drop_off_details(self) -> str:
        return self.container.find_element(*self._drop_off_details).text

    @property
    def edit_capacity_button(self) -> WebElement:
        return self.container.find_element(*self._edit_capacity)

    @property
    def edit_pick_up_time_button(self) -> WebElement:
        return self.container.find_element(*self._edit_time_button)

    @property
    def edit_pu_do_button(self) -> WebElement:
        return self.container.find_element(*self._edit_pu_do_button)

    @property
    def pick_up_details(self) -> str:
        return self.container.find_element(*self._pick_up_details).text

    @property
    def pick_up_time_details(self) -> str:
        return self.container.find_element(*self._pick_up_time_details).text

    def edit_capacity(self) -> object:
        """Edit a ride's capacity by selecting the edit capacity button."""
        self.edit_capacity_button.click()

        return PassengerDetailsModal(self).wait_for_component_to_be_present()

    def edit_pick_up_time(self) -> object:
        """Edit a ride's pick up time by selecting the edit pick up time button."""
        self.edit_pick_up_time_button.click()

        return PickupTimeModal(self).wait_for_component_to_be_present()

    def edit_pu_do(self) -> object:
        """Edit a ride's pick up or drop off by selecting the edit PU/DO button."""
        self.edit_pu_do_button.click()

        return AddressInput(self).wait_for_component_to_be_present()

    def submit_ride(self) -> object:
        """Submit a ride by selecting the confirmation button."""
        self.confirm_ride_button.click()

        return RideOverviewModal(self).wait_for_component_to_be_present()
