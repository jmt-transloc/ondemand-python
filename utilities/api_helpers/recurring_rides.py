from random import random
from time import sleep

import requests
from environs import Env
from requests import HTTPError, Response
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class RecurringRidesAPI(API):
    """API methods for recurring rides."""

    API: API = API()
    URL: str = API.build_api_url(path=f'/ondemand/{AGENCY}/rides/subscriptions')

    def cancel_booked_ride(self, ride: dict) -> None:
        """Cancel a booked portion of a recurring ride using the API.

        :param ride: A recurring ride yielded by the API.
        """
        self.change_ride_status(ride, 'Canceled')

    def cancel_recurring_ride(self, recurring_ride: dict) -> None:
        """Cancel a recurring ride using the API.

        Use this method for cancelling an entire subscription rather than a single booked ride.

        :param recurring_ride: A recurring ride yielded by the API.
        """
        tries: int = 10
        url: str = f'{self.URL}/{recurring_ride["ride_subscription_id"]}/cancel'

        while True:
            tries -= 1

            sleep(random())
            response: Response = requests.put(
                url=url, headers=self.API.build_auth_headers(),
            )
            if response.status_code == 200:
                break
            elif tries == 0:
                raise HTTPError(f'Requests failed with response: {response.json()}')

    def change_ride_status(self, ride: dict, status: str) -> None:
        """Manipulate a recurring ride's status using the API.

        :param ride: A recurring ride yielded by the API.
        :param status: A specified status.
        """
        groomed_status: str = status.lower().replace(' ', '_')
        ride_id: int = ride['ride']['ride_id']
        status_data: dict = {'status': f'{groomed_status}'}
        url: str = API.build_api_url(path=f'/ondemand/{AGENCY}/rides/{ride_id}')

        self.API.change_ride_status_request(data=status_data, expected_response=[200], url=url)

    def complete_ride(self, ride: dict) -> None:
        """Complete a ride using the API.

        :param ride: A recurring ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='In Progress')
        self.change_ride_status(ride=ride, status='Complete')

    def create_recurring_ride(self, ride_data: dict) -> dict:
        """Add a recurring ride using the API, then surface the ride ID for teardown.

        :param ride_data: A dictionary of recurring ride data for API consumption.
        """
        return self.API.create_request(data=ride_data, expected_response=[200], url=self.URL)

    def set_no_show(self, ride: dict) -> None:
        """Set a ride to 'No Show' status.

        :param ride: A recurring ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='No Show')

    def start_ride(self, ride: dict) -> None:
        """Start a ride using the API.

        :param ride: A recurring ride yielded by the API.
        """
        self.change_ride_status(ride=ride, status='In Progress')
