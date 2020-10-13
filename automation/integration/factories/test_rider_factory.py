import pytest
from utilities.factories.riders import RiderFactory


@pytest.mark.factory
@pytest.mark.unit
class TestRiderFactory:
    """Battery of tests for RiderFactory functionality."""

    @pytest.mark.low
    def test_build__override_default_values(self) -> None:
        """Check that RiderFactory values may be overridden post-build."""
        rider: dict = RiderFactory.build()
        default_first_name: str = rider['first_name']
        rider['first_name'] = 'Testing'

        assert rider['first_name'] != default_first_name

    @pytest.mark.medium
    def test_build__params__account_rider(self) -> None:
        """Check that the RiderFactory build method generates an account rider."""
        rider: dict = RiderFactory.build(account_rider=True)

        assert (
            rider['first_name'] == 'QA'
            and rider['last_name'] == 'Rider'
            and rider['email'] == 'automation+qa_rider_001@transloc.com'
            and rider['username'] == 'qa_rider_001'
        )

    @pytest.mark.low
    def test_build__requires_no_params(self) -> None:
        """Check that the RiderFactory build method does not require params."""
        rider: dict = RiderFactory.build()

        assert rider is not None

    @pytest.mark.low
    def test_build__returns_type_dict(self) -> None:
        """Check that the RiderFactory build method returns a dictionary."""
        rider = RiderFactory.build()

        assert type(rider) == dict

    @pytest.mark.medium
    def test_build__subsequent_calls_return_new_rider(self) -> None:
        """Check that a new Rider is returned from the RiderFactory build method."""
        rider_one: dict = RiderFactory.build()
        rider_two: dict = RiderFactory.build()

        assert rider_one != rider_two

    @pytest.mark.medium
    def test_create__params__account_rider(self) -> None:
        """Check that the RiderFactory create method generates an account rider."""
        rider: dict = RiderFactory.create(account_rider=True)

        assert (
            rider['first_name'] == 'QA'
            and rider['last_name'] == 'Rider'
            and rider['email'] == 'automation+qa_rider_001@transloc.com'
            and rider['username'] == 'qa_rider_001'
        )

    @pytest.mark.low
    def test_create__requires_no_params(self) -> None:
        """Check that the RiderFactory create method does not require params."""
        rider: dict = RiderFactory.create()

        assert rider is not None

    @pytest.mark.low
    def test_create__returns_type_dict(self) -> None:
        """Check that the RiderFactory create method returns a dictionary."""
        rider = RiderFactory.create()

        assert type(rider) == dict
