import json
import os
from random import random
from time import sleep
from typing import List, Union

import requests
from environs import Env
from requests import HTTPError, Response
from utilities.constants.common import API_PASSWORD, USERS


sut_env = Env()


class API(object):
    """Base API class for use with API helper methods."""

    URL: str = None

    @staticmethod
    def authenticate(username: str) -> Union[dict, None]:
        """Authenticate using the API for framework login.

        :param username: The username for application login.
        """
        _url: str = API.build_api_url(f'/me/login?username={username}&password={API_PASSWORD}')
        tries: int = 10

        while True:
            tries -= 1

            sleep(random())
            response: Response = requests.post(url=_url)

            if response.status_code == 200:
                return response.json()
            elif tries == 0:
                raise HTTPError(f'Requests failed with response: {response.json()}')

    @staticmethod
    def build_api_url(path: str = '') -> str:
        """Construct an API URL from environment data.

        :param path: Additional path for a site URL.
        """
        env = sut_env.str('ENV')
        port = sut_env.int('PORT')
        team = sut_env.str('TEAM')

        if env == 'localhost':
            return f'http://{env}.transloc.com:{port}/v1{path}'
        elif env == 'stage':
            return f'https://api.stage.transloc.com/v1{path}'
        else:
            return f'https://api.{team}.{env}.transloc.com/v1{path}'

    def build_auth_headers(self) -> dict:
        """Consume the authenticate method to create an auth header for API usage.

        This method saves a superuser token for the creation and deletion of test data. Using other
        permissions would provide unreliable test data so superuser has been chosen as it has the
        highest level of privileges.
        """
        self.capture_token(username=USERS.Superuser.USERNAME, superuser=True)
        _token: str = json.loads(os.getenv('SUPERUSER_AUTH_TOKEN'))['value']

        return {'Authorization': f'Token {_token}', 'Content-Type': 'application/json'}

    def capture_token(self, username: str, superuser: bool = False) -> None:
        """Capture an authentication token as an environment variable for framework usage.

        :param username: The username for application login.
        :param superuser: Boolean for whether the user is a superuser or not.
        """
        _auth_response: dict = self.authenticate(username)
        _token: str = _auth_response['token']
        _cookie: dict = dict(
            domain='.transloc.com',
            httpOnly=False,
            name='transloc_authn_cookie',
            path='/',
            secure=False,
            value=_token,
        )
        json_cookie = json.dumps(_cookie)

        if superuser:
            os.environ['SUPERUSER_AUTH_TOKEN'] = json_cookie
        else:
            os.environ['AUTH_TOKEN'] = json_cookie

    def change_ride_status_request(
        self, data: dict, expected_response: List[int], url: str,
    ) -> None:
        """Change the status of a Ride or Recurring Ride object using a specified API endpoint.

        :param data: The intended data for status change.
        :param expected_response: A list of expected responses.
        :param url: The URL for status change.
        """
        tries: int = 10

        while True:
            tries -= 1

            sleep(random())
            response: Response = requests.patch(
                url=url, headers=self.build_auth_headers(), data=json.dumps(data),
            )
            if response.status_code in expected_response:
                break
            elif tries == 0:
                raise requests.HTTPError(f'Requests failed with response: {response.json()}')

    def create_request(self, data: dict, expected_response: List[int], url: str) -> dict:
        """Create an object using a specified API endpoint.

        :param data: The intended data for creation.
        :param expected_response: A list of expected responses.
        :param url: The URL for creation.
        """
        tries: int = 10

        while True:
            tries -= 1

            sleep(random())
            response: Response = requests.post(
                url=url, headers=self.build_auth_headers(), data=json.dumps(data),
            )

            if response.status_code in expected_response:
                return response.json()
            elif tries == 0:
                raise requests.HTTPError(f'Requests failed with response: {response.json()}')

    def delete_request(self, expected_response: List[int], url: str) -> None:
        """Delete an object using a specified API endpoint.

        :param expected_response: A list of expected responses.
        :param url: The URL for deletion.
        """
        tries: int = 10

        while True:
            tries -= 1

            sleep(random())
            response: Response = requests.delete(
                url=url, headers=self.build_auth_headers(),
            )

            if response.status_code in expected_response:
                break
            elif tries == 0:
                raise requests.HTTPError(f'Requests failed with response: {response.json()}')
