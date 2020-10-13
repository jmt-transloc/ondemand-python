import pytest
from factory import Factory
from pages import Login
from pages.authentication.forgot_password import ForgotPassword
from pytest import fixture
from utilities.constants.common import MESSAGES
from utilities.factories.fake import fake
from utilities.models.data_models import User


@pytest.mark.no_auth
@pytest.mark.ui
class TestForgotPassword:
    """Battery of tests for the forgot password workflow."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in forgot password testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.forgot_password: ForgotPassword = ForgotPassword(selenium)
        self.login: Login = Login(selenium)

    @pytest.mark.low
    @pytest.mark.smoke
    def test_forgot_password__visit_page(self) -> None:
        """Visit the forgot password page, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        self.login.visit()
        self.login.wait_for_page_to_load()
        self.login.forgot_password_link.click()

        self.forgot_password.wait_for_page_to_load()

        assert self.forgot_password.loaded

    @pytest.mark.high
    @pytest.mark.smoke
    def test_forgot_password__success(self, user_factory: Factory) -> None:
        """Input a valid account, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(account_user=True)

        self.forgot_password.visit()

        self.forgot_password.wait_for_page_to_load()
        self.forgot_password.fill_forgot_password_form(user)
        self.forgot_password.submit_button.click()

        self.login.wait_for_page_to_load()
        assert self.login.success_message.visible

    @pytest.mark.low
    def test_forgot_password__failure__invalid_email(self, user_factory: fixture) -> None:
        """Input an incomplete email address, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(email='stuff@stuff')

        self.forgot_password.visit()

        self.forgot_password.wait_for_page_to_load()
        self.forgot_password.fill_forgot_password_form(user)
        self.forgot_password.submit_button.click()

        assert MESSAGES.AUTH.INCOMPLETE_EMAIL in self.forgot_password.errors.error_messages

    @pytest.mark.low
    def test_forgot_password__failure__min_email_entered(self, user_factory: fixture) -> None:
        """Input an invalid email address, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(email='')

        self.forgot_password.visit()

        self.forgot_password.wait_for_page_to_load()
        self.forgot_password.fill_forgot_password_form(user)
        self.forgot_password.submit_button.click()

        assert MESSAGES.AUTH.NO_EMAIL in self.forgot_password.errors.error_messages

    @pytest.mark.low
    def test_forgot_password__failure__no_account_found(self, user_factory: fixture) -> None:
        """Input an invalid email address, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(email=fake.email())

        self.forgot_password.visit()

        self.forgot_password.wait_for_page_to_load()
        self.forgot_password.fill_forgot_password_form(user)
        self.forgot_password.submit_button.click()

        assert MESSAGES.AUTH.USER_NOT_FOUND in self.forgot_password.errors.error_messages
