from utilities.driver_helpers.selectors import Selector, Selectors
from utilities.driver_helpers.types import WebElement
from utilities.page_object_models.component import Component


class DeletionModal(Component):
    """Objects and methods for the Deletion Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('deletion-modal-container')
    _cancel_button: Selector = Selectors.data_id('deletion-modal-cancel-button')
    _confirm_button: Selector = Selectors.data_id('deletion-modal-confirm-button')
    _message: Selector = Selectors.data_id('deletion-modal-message')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def message(self) -> WebElement:
        return self.container.find_element(*self._message)
