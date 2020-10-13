import pytest
from pytest import fixture
from utilities.models.data_models import Rider


@pytest.mark.model
@pytest.mark.unit
class TestRider:
    """Battery of tests for Rider data model functionality."""

    @pytest.fixture
    def valid_rider(self) -> Rider:
        """Create a valid Rider."""
        rider: Rider = Rider(first_name='Test', last_name='User', email='test@testing.com')

        yield rider

    @pytest.mark.low
    def test_build__override_default_values(self, valid_rider: fixture) -> None:
        """Check that default values may be overridden post-build.

        :param valid_rider: A valid Rider object for testing.
        """
        valid_rider.first_name = 'Testing'

        assert valid_rider.first_name == 'Testing'

    @pytest.mark.low
    def test_build__requires_first_name_param(self) -> None:
        """Check that the Rider data model requires a first_name param."""
        with pytest.raises(TypeError) as e:
            Rider(last_name='User', email='test@testing.com')  # type: ignore
        assert "required positional argument: 'first_name'" in str(e.value)

    @pytest.mark.low
    def test_build__requires_last_name_param(self) -> None:
        """Check that the Rider data model requires a last_name param."""
        with pytest.raises(TypeError) as e:
            Rider(first_name='Test', email='test@testing.com')  # type: ignore
        assert "required positional argument: 'last_name'" in str(e.value)

    @pytest.mark.low
    def test_build__requires_email_param(self) -> None:
        """Check that the Rider data model requires an email param."""
        with pytest.raises(TypeError) as e:
            Rider(first_name='Test', last_name='User')  # type: ignore
        assert "required positional argument: 'email'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_rider: fixture) -> None:
        """Check that the Rider data model sets default values.

        :param valid_rider: A valid Rider object for testing.
        """
        assert valid_rider.phone == '(555) 222-3333' and valid_rider.username == ''

    @pytest.mark.low
    def test_build__valid_input(self, valid_rider: fixture) -> None:
        """Build a Rider with valid input.

        :param valid_rider: A valid Rider object for testing.
        """
        assert valid_rider.first_name == 'Test' and valid_rider.last_name == 'User'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that default values may be overridden prior to build."""
        rider: Rider = Rider(first_name='Testing', last_name='User', email='testing@test.com')

        assert (
            rider.first_name == 'Testing'
            and rider.last_name == 'User'
            and rider.email == 'testing@test.com'
        )
