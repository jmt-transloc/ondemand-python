import pytest
from pages import Login
from pages.authentication.conftest import build_login_url
from pytest import fixture
from utilities.constants.common import USERS


@pytest.mark.no_auth
@pytest.mark.ui
class TestLogin:
    """Battery of tests for TransLoc application login functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in login testing."""
        self.login: Login = Login(selenium)

    @pytest.mark.low
    def test_login__failure(self) -> None:
        """Input invalid user data, then check for an error state."""
        self.login.visit()

        self.login.login(
            'testing', 'testing123',
        )
        self.login.check_login_fail()

        assert self.login.error_message.visible

    @pytest.mark.high
    @pytest.mark.smoke
    def test_login__success(self) -> None:
        """Input valid user data, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        self.login.visit()

        self.login.login(
            USERS.Superuser.USERNAME, USERS.Superuser.PASSWORD,
        )

        assert self.login.driver.current_url == build_login_url(path='/')
