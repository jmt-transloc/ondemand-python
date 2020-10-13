import pytest
from pytest import fixture
from utilities.models.data_models import RecurringRide


@pytest.mark.model
@pytest.mark.unit
class TestRecurringRide:
    """Battery of tests for RecurringRide data model functionality."""

    @pytest.fixture
    def valid_ride(self) -> RecurringRide:
        """Create a valid RecurringRide."""
        ride: RecurringRide = RecurringRide(
            ride={
                'rider': {
                    'first_name': 'Test',
                    'last_name': 'Rider',
                    'email': 'testing@testing.com',
                    'phone': '(555) 222-3333',
                    'username': '',
                },
                'ride_id': None,
                'dropoff': {
                    'address': '4507 South Miami Boulevard Durham, NC, USA',
                    'position': {'latitude': 35.9015672, 'longitude': -78.851133},
                    'priority': 0,
                },
                'fare': None,
                'messages': [],
                'note': None,
                'pickup': {
                    'address': '4506 Emperor Boulevard Durham, NC, USA',
                    'position': {'latitude': 35.8724046, 'longitude': -78.8426551},
                    'priority': 0,
                    'timestamp': '2020-07-01T13:11:47.000Z',
                },
                'capacity': 1,
                'service_id': None,
                'service_type': 'ondemand',
                'source': 'dispatcher',
                'status': 'pending',
                'terminal_reason': None,
                'wheelchair': False,
            },
            rides=[
                {'timestamp': '2020-07-02T13:11:41.000Z'},
                {'timestamp': '2020-07-04T13:11:41.000Z'},
                {'timestamp': '2020-07-06T13:11:41.000Z'},
                {'timestamp': '2020-07-08T13:11:41.000Z'},
                {'timestamp': '2020-07-10T13:11:41.000Z'},
                {'timestamp': '2020-07-12T13:11:41.000Z'},
            ],
        )

        yield ride

    @pytest.mark.low
    def test_build__override_default_values(self, valid_ride: fixture) -> None:
        """Check that default values may be overridden post-build.

        :param valid_ride: A valid RecurringRide object.
        """
        valid_ride.ride['wheelchair'] = True

        assert valid_ride.ride['wheelchair'] is True

    @pytest.mark.low
    def test_build__requires_ride_param(self) -> None:
        """Check that the RecurringRide data model requires a ride param."""
        with pytest.raises(TypeError) as e:
            RecurringRide(rides=[])  # type: ignore
        assert "required positional argument: 'ride'" in str(e.value)

    @pytest.mark.low
    def test_build__requires_rides_param(self) -> None:
        """Check that the RecurringRide data model requires a rides param."""
        with pytest.raises(TypeError) as e:
            RecurringRide(ride={})  # type: ignore
        assert "required positional argument: 'rides'" in str(e.value)

    @pytest.mark.low
    def test_build__set_default_values(self, valid_ride: fixture) -> None:
        """Check that building a RecurringRide sets default values.

        :param valid_ride: A valid RecurringRide object.
        """
        assert valid_ride.description == ''

    @pytest.mark.low
    def test_build__valid_input(self, valid_ride: fixture) -> None:
        """Build a RecurringRide with valid input.

        :param valid_ride: A valid RecurringRide object.
        """
        rider: dict = valid_ride.ride['rider']

        assert rider['first_name'] == 'Test' and rider['last_name'] == 'Rider'

    @pytest.mark.low
    def test_model__override_default_values(self) -> None:
        """Check that the default values may be overridden prior to build."""
        ride: RecurringRide = RecurringRide(ride={}, rides=[], description='This is a test.')

        assert ride.description == 'This is a test.'
