import pytest
from factory import Factory
from pages import Login
from pages.authentication.registration import Registration
from pytest import fixture
from utilities.constants.common import MESSAGES, USERS
from utilities.factories.fake import fake
from utilities.models.data_models import User


@pytest.mark.no_auth
@pytest.mark.ui
class TestRegister:
    """Battery of tests for the user registration workflow."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in register testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.login: Login = Login(selenium)
        self.registration: Registration = Registration(selenium)

    @pytest.mark.low
    @pytest.mark.smoke
    def test_registration__visit_page(self) -> None:
        """Visit the registration page, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        self.login.visit()
        self.login.wait_for_page_to_load()
        self.login.sign_up_button.click()

        self.registration.wait_for_page_to_load()

        assert self.registration.loaded

    @pytest.mark.high
    @pytest.mark.smoke
    def test_registration__success(self, user_factory: Factory) -> None:
        """Input a valid registration, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create()

        self.registration.visit()
        self.registration.wait_for_page_to_load()
        self.registration.fill_registration_form(user)
        self.registration.submit_button.click()

        self.login.wait_for_page_to_load()
        assert self.login.success_message.visible

    @pytest.mark.low
    def test_registration__failure__email_in_use(self, user_factory: Factory) -> None:
        """Input account data for an existing email, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(email=USERS.EMAIL)

        self.registration.visit()
        self.registration.wait_for_page_to_load()
        self.registration.fill_registration_form(user)
        self.registration.submit_button.click()

        assert self.registration.user_exists_error.visible

    @pytest.mark.low
    def test_registration__failure__username_in_use(self, user_factory: Factory) -> None:
        """Input account data for an existing user, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(username=USERS.USERNAME)

        self.registration.visit()
        self.registration.wait_for_page_to_load()
        self.registration.fill_registration_form(user)
        self.registration.submit_button.click()

        assert self.registration.user_exists_error.visible

    @pytest.mark.low
    def test_registration__failure__passwords_must_match(self, user_factory: Factory) -> None:
        """Input account data with a mismatched password, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(password=fake.password())

        self.registration.visit()
        self.registration.wait_for_page_to_load()
        self.registration.fill_registration_form(user)
        self.registration.submit_button.click()

        assert MESSAGES.AUTH.PASSWORD_MISMATCH in self.registration.inline_error_messages

    @pytest.mark.low
    @pytest.mark.parametrize(
        'username, phone, password, repeat_password',
        [
            ('1', '1', '1', '1'),
            (
                fake.password(length=33),
                fake.password(length=33),
                fake.password(length=129),
                fake.password(length=129),
            ),
        ],
    )
    def test_registration__failure__min_max_length_inputs(
        self,
        user_factory: Factory,
        username: fixture,
        phone: fixture,
        password: fixture,
        repeat_password: fixture,
    ) -> None:
        """Input account data with min and max length inputs, then check for a failure state.

        :param user_factory: A factory for generating user data.
        """
        user: User = user_factory.create(
            username=username, phone=phone, password=password, repeat_password=repeat_password,
        )

        self.registration.visit()
        self.registration.wait_for_page_to_load()
        self.registration.fill_registration_form(user)
        self.registration.submit_button.click()

        assert (
            MESSAGES.AUTH.USERNAME_MIN_LENGTH
            and f'{MESSAGES.AUTH.PHONE_VALIDATION}\n{MESSAGES.AUTH.PHONE_MIN_LENGTH}'
            and MESSAGES.AUTH.PASSWORD_MIN_LENGTH in self.registration.inline_error_messages
        )
