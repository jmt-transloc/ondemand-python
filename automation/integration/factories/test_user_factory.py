import pytest
from pytest import fixture
from utilities.constants.common import USERS
from utilities.factories.users import UserFactory
from utilities.models.data_models import User


@pytest.mark.factory
@pytest.mark.unit
class TestUserFactory:
    """Battery of tests for UserFactory functionality."""

    @pytest.mark.low
    def test_build__returns_type_user(self) -> None:
        """Check that a User is created from the UserFactory."""
        user: User = UserFactory.build()

        assert type(user) == User

    @pytest.mark.low
    def test_create__returns_type_user(self) -> None:
        """Check that a User is created from the UserFactory."""
        user: User = UserFactory.create()

        assert type(user) == User

    @pytest.mark.low
    def test_factory__subsequent_calls_return_new_user(self) -> None:
        """Check that a new User is returned from the UserFactory."""
        user_one: User = UserFactory.create()
        user_two: User = UserFactory.create()

        assert user_one != user_two

    @pytest.mark.low
    @pytest.mark.parametrize(
        'username, first_name, last_name, email',
        [('testing123', 'unit', 'testing', 'testing@testing.com')],
    )
    def test_factory__override_values(
        self, username: fixture, first_name: fixture, last_name: fixture, email: fixture,
    ) -> None:
        """Check that factory values may be overridden."""
        user: User = UserFactory.create(
            username=username, first_name=first_name, last_name=last_name, email=email,
        )

        assert (
            user.first_name == first_name
            and user.username == username
            and user.email == email
            and user.last_name == last_name
        )

    @pytest.mark.low
    def test_factory__params__account_user(self) -> None:
        """Check that a User may be manipulated using a factory trait."""
        user: User = UserFactory.create(account_user=True)
        expected_username: str = USERS.USERNAME
        expected_email: str = USERS.EMAIL

        assert expected_email in user.email and expected_username in user.username
