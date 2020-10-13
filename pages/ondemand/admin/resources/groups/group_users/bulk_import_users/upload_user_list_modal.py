from utilities import Component, Selector, Selectors, WebElement


class UploadUserListModal(Component):
    """Objects and methods for the Upload User List Modal."""

    ROOT_LOCATOR: Selector = Selectors.data_id('upload-user-list-modal-container')
    _confirm_button: Selector = Selectors.data_id('upload-user-list-confirm-button')
    _message: Selector = Selectors.data_id('upload-user-list-message')

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def message(self) -> str:
        return self.container.find_element(*self._message).text
