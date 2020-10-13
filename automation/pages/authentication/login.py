import json
import os
from typing import Optional

from pages.authentication.conftest import build_login_url
from utilities import Page, Selector, Selectors, WebElement


class Login(Page):
    """Login methods and objects for all TransLoc applications."""

    URL_PATH: str = build_login_url(path='/login')
    ROOT_LOCATOR: Selector = Selectors.class_name('login-container')

    _error_message: Selector = Selectors.data_id('error-message')
    _forgot_password_link: Selector = Selectors.data_id('forgot-password-link')
    _password_field: Selector = Selectors.name('password')
    _sign_up_button: Selector = Selectors.data_id('sign-up-button')
    _submit_button: Selector = Selectors.data_id('submit-login-button')
    _success_message: Selector = Selectors.data_id('success-message')
    _university_login_button: Selector = Selectors.data_id('university-login-button')
    _username_field: Selector = Selectors.name('username')

    @property
    def error_message(self) -> WebElement:
        return self.driver.find_element(*self._error_message)

    @property
    def forgot_password_link(self) -> WebElement:
        return self.driver.find_element(*self._forgot_password_link)

    @property
    def password_field(self) -> WebElement:
        return self.driver.find_element(*self._password_field)

    @property
    def sign_up_button(self) -> WebElement:
        return self.driver.find_element(*self._sign_up_button)

    @property
    def submit_button(self) -> WebElement:
        return self.driver.find_element(*self._submit_button)

    @property
    def success_message(self) -> WebElement:
        return self.driver.find_element(*self._success_message)

    @property
    def university_login_button(self) -> WebElement:
        return self.driver.find_element(*self._university_login_button)

    @property
    def username_field(self) -> WebElement:
        return self.driver.find_element(*self._username_field)

    def add_auth_token(self):
        """Add a captured authorization token as an environment variable."""
        auth_token = json.loads(os.getenv('AUTH_TOKEN'))
        self.driver.add_cookie(auth_token)

    def capture_token(self) -> None:
        """Capture an authorization token."""
        auth_cookie = self.driver.get_cookies()[1]
        if 'expiry' in auth_cookie:
            del auth_cookie['expiry']

        json_cookie = json.dumps(auth_cookie)

        os.environ['AUTH_TOKEN'] = json_cookie

    def check_login_fail(self) -> None:
        """Check whether an error message is shown."""
        self.driver.wait_until_visible(*self._error_message)

    def login(self, username: Optional[str], password: Optional[str]) -> None:
        """Login in to a TransLoc application.

        :param password: The password for login.
        :param username: The username for login.
        """
        self.username_field.fill(username)
        self.password_field.fill(password)

        self.submit_button.click()
