import pytest
from pytest import fixture
from utilities.models.data_models import User


@pytest.mark.model
@pytest.mark.unit
class TestUser:
    """Battery of tests for the User dataclass."""

    @pytest.fixture
    def default_value_user(self) -> User:
        """Create a user with empty values to check default values."""
        user: User = User(username='', first_name='', last_name='', email='')

        yield user

    @pytest.fixture
    def valid_user(self) -> User:
        """Create a user with non-empty values."""
        user: User = User(
            username='testing123',
            first_name='Tester',
            last_name='Testerton',
            email='testing@testing.com',
        )

        yield user

    @pytest.mark.low
    def test_user__params_required(self) -> None:
        """Attempt to build a new user without entering params."""
        with pytest.raises(TypeError):
            assert User()  # type: ignore

    @pytest.mark.low
    def test_user__default_values(self, default_value_user: fixture) -> None:
        """Check for default user values."""
        user: User = default_value_user

        assert (
            user.phone == '(555) 222-3333'
            and user.password == 'testing123'
            and user.repeat_password == 'testing123'
            and user.privacy_policy_accepted == 'y'
        )

    @pytest.mark.low
    def test_user__valid_input(self, valid_user: fixture) -> None:
        """Build a user with valid input."""
        user: User = valid_user

        assert (
            user.username == 'testing123'
            and user.first_name == 'Tester'
            and user.last_name == 'Testerton'
            and user.email == 'testing@testing.com'
        )
