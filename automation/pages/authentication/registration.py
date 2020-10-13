from typing import List

from pages.authentication.conftest import build_login_url
from utilities import Page, Selector, Selectors, WebElement, WebElements
from utilities.models.data_models import User


class Registration(Page):
    """Objects and methods for the Register page."""

    URL_PATH: str = build_login_url(path='/register')
    ROOT_LOCATOR: Selector = Selectors.class_name('register-container')

    _email_field: Selector = Selectors.name('email')
    _first_name_field: Selector = Selectors.name('first_name')
    _inline_errors: Selector = Selectors.class_name('errors')
    _last_name_field: Selector = Selectors.name('last_name')
    _password_field: Selector = Selectors.name('password')
    _phone_field: Selector = Selectors.name('phone')
    _privacy_policy_field: Selector = Selectors.name('privacy_policy_accepted')
    _repeat_password_field: Selector = Selectors.name('repeat_password')
    _submit_button: Selector = Selectors.data_id('submit-button')
    _username_field: Selector = Selectors.name('username')
    _user_exists_error: Selector = Selectors.data_id('error-message')

    @property
    def email_field(self) -> WebElement:
        return self.driver.find_element(*self._email_field)

    @property
    def first_name_field(self) -> WebElement:
        return self.driver.find_element(*self._first_name_field)

    @property
    def inline_errors(self) -> WebElements:
        return self.driver.find_elements(*self._inline_errors)

    @property
    def inline_error_messages(self) -> List[str]:
        return [error.text for error in self.inline_errors]

    @property
    def last_name_field(self) -> WebElement:
        return self.driver.find_element(*self._last_name_field)

    @property
    def password_field(self) -> WebElement:
        return self.driver.find_element(*self._password_field)

    @property
    def phone_field(self) -> WebElement:
        return self.driver.find_element(*self._phone_field)

    @property
    def privacy_policy_checkbox(self) -> WebElement:
        return self.driver.find_element(*self._privacy_policy_field)

    @property
    def repeat_password_field(self) -> WebElement:
        return self.driver.find_element(*self._repeat_password_field)

    @property
    def submit_button(self) -> WebElement:
        return self.driver.find_element(*self._submit_button)

    @property
    def username_field(self) -> WebElement:
        return self.driver.find_element(*self._username_field)

    @property
    def user_exists_error(self) -> WebElement:
        return self.driver.find_element(*self._user_exists_error)

    def fill_registration_form(self, user: User) -> None:
        """Fill out a user registration form.

        :param user: A user generated from a User Factory.
        """
        self.username_field.fill(user.username)
        self.email_field.fill(user.email)
        self.first_name_field.fill(user.first_name)
        self.last_name_field.fill(user.last_name)
        self.phone_field.fill(user.phone)
        self.password_field.fill(user.password)
        self.repeat_password_field.fill(user.repeat_password)
        self.privacy_policy_checkbox.click()
