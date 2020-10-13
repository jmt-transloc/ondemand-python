from selenium.common.exceptions import UnexpectedAlertPresentException
from utilities import Component, Selector, Selectors, WebElement


class ArchiveModal(Component):
    """Objects and methods for the Service Archive Modal."""

    ROOT_LOCATOR: Selector = Selectors.data_id('archive-service-modal-container')
    _cancel_button: Selector = Selectors.data_id('cancel-archive-service-button')
    _confirm_button: Selector = Selectors.data_id('confirm-archive-service-button')
    _message: Selector = Selectors.data_id('archive-service-message')

    @property
    def archive_message(self) -> WebElement:
        return self.container.find_element(*self._message)

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    def confirm_service_archive(self) -> bool:
        """Confirm a service archive.

        Returns True if the container is no longer displayed and False if an Alert is raised. This
        method should be used with an assert statement to verify its boolean return.
        """
        self.confirm_button.click()

        try:
            self.page.driver.wait_until_not_visible(*self.ROOT_LOCATOR)
            return True
        except UnexpectedAlertPresentException:
            return False
