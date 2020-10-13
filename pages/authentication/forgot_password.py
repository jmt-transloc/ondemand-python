from typing import List

from pages.authentication.conftest import build_login_url
from utilities import Component, Page, Selector, Selectors, WebElement, WebElements
from utilities.models.data_models import User


class Errors(Component):
    """Objects and methods for the Errors component."""

    ROOT_LOCATOR: Selector = Selectors.class_name('errors')
    _errors: Selector = Selectors.tag('li')

    @property
    def errors(self) -> WebElements:
        return self.container.find_elements(*self._errors)

    @property
    def error_messages(self) -> List[str]:
        return [error.text for error in self.errors]


class ForgotPassword(Page):
    """Objects and methods for the Forgot Password page."""

    URL_PATH: str = build_login_url(path='/forgot-password')
    ROOT_LOCATOR: Selector = Selectors.data_id('forgot-password-container')

    _cancel_button: Selector = Selectors.data_id('cancel-button')
    _email_field: Selector = Selectors.name('email')
    _submit_button: Selector = Selectors.data_id('submit-forgot-password-button')

    @property
    def cancel_button(self) -> WebElement:
        return self.driver.find_element(*self._cancel_button)

    @property
    def email_field(self) -> WebElement:
        return self.driver.find_element(*self._email_field)

    @property
    def errors(self) -> Errors:
        return Errors(self)

    @property
    def submit_button(self) -> WebElement:
        return self.driver.find_element(*self._submit_button)

    def fill_forgot_password_form(self, user: User) -> None:
        """Fill out a forgot password form.

        :param user: A user generated from a User Factory.
        """
        self.email_field.fill(user.email)
