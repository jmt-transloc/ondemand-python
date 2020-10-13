from utilities import Component, Selector, Selectors, WebElement


class DeletionModal(Component):
    """Objects and methods for the deletion modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('deletion-modal-container')

    _cancel_button: Selector = Selectors.data_id('deletion-modal-cancel-button')
    _confirm_button: Selector = Selectors.data_id('deletion-modal-confirm-button')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)
