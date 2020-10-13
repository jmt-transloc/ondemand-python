from utilities import Component, Selector, Selectors, WebElement


class RideShareModal(Component):
    """Objects and methods for the Ride Share Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('rideshare-modal-container')
    _confirm_button: Selector = Selectors.data_id('rideshare-confirm-button')
    _message: Selector = Selectors.data_id('rideshare-message')

    @property
    def ride_share_message(self) -> WebElement:
        return self.container.find_element(*self._message)

    @property
    def ride_share_confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    def check_for_modal(self) -> None:
        """Check for the ride share modal, then click if it is visible."""
        if self.ride_share_message.visible:
            self.ride_share_confirm_button.click()
