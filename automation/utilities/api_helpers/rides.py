from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class RidesAPI(API):
    """API methods for rides."""

    API: API = API()
    URL = API.build_api_url(path=f'/ondemand/{AGENCY}/rides')

    def cancel_ride(self, ride: dict) -> None:
        """Cancel a ride using the API.

        :param ride: A ride yielded by the API.
        """
        self.change_ride_status(ride, 'Canceled')

    def change_ride_status(self, ride: dict, status: str) -> None:
        """Manipulate a ride's status using the API.

        :param ride: A ride yielded from the API.
        :param status: A specified status.
        """
        groomed_status: str = status.lower().replace(' ', '_')
        ride_id: int = ride['ride_id']
        status_data: dict = {'status': f'{groomed_status}'}
        url: str = f'{self.URL}/{ride_id}'

        self.API.change_ride_status_request(data=status_data, expected_response=[200], url=url)

    def complete_ride(self, ride: dict) -> None:
        """Complete a ride using the API.

        :param ride: A ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='In Progress')
        self.change_ride_status(ride=ride, status='Complete')

    def create_ride(self, ride_data: dict) -> dict:
        """Add a ride using the API, then surface the ride ID for teardown.

        :param ride_data: A dictionary of ride data for API consumption.
        """
        return self.API.create_request(data=ride_data, expected_response=[200], url=self.URL)

    def set_no_show(self, ride: dict) -> None:
        """Set a ride to 'No Show' status.

        :param ride: A ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='No Show')

    def start_ride(self, ride: dict) -> None:
        """Start a ride using the API.

        :param ride: A ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='In Progress')
