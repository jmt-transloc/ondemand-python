from utilities import Component, Selector, Selectors, WebElement


class DeletionModal(Component):
    """Objects and methods for the Deletion Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('delete-address-modal-container')
    _cancel_button: Selector = Selectors.data_id('cancel-delete-address-button')
    _confirm_button: Selector = Selectors.data_id('confirm-delete-address-button')
    _message: Selector = Selectors.data_id('delete-address-message')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def delete_message(self) -> WebElement:
        return self.container.find_element(*self._message)

    def confirm_address_deletion(self) -> None:
        """Confirm an address deletion.

        Returns True if the container is no longer displayed. This should be used with an assert
        statement to verify it is True.
        """
        self.confirm_button.click()
        self.page.driver.wait_until_not_visible(*self.ROOT_LOCATOR)
