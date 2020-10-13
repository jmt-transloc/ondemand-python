from utilities import Component, Selector, Selectors, WebElement


class CancellationModal(Component):
    """Cancellation Modal component objects and methods for OnDemand applications.

    The cancellation modal may be accessed by selected 'Cancel' for a ride The modal may be found
    in the Ride Card or Ride Row kebab menus.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('cancellation-modal-container')
    _cancel_button: Selector = Selectors.data_id('cancellation-modal-cancel-button')
    _confirm_button: Selector = Selectors.data_id('cancellation-modal-confirm-button')
    _cancel_reason: Selector = Selectors.name('terminal-reason')

    @property
    def ride_cancel_input(self) -> WebElement:
        return self.container.find_element(*self._cancel_reason)

    @property
    def ride_cancel_confirm(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    def cancel_ride(self, reason: str) -> None:
        """Cancel a ride, then wait for the cancellation modal to no longer be visible.

        :param reason: The cancellation reason for the ride.
        """
        self.ride_cancel_input.fill(reason)
        self.ride_cancel_confirm.click()

        self.wait_for_component_to_not_be_visible()
