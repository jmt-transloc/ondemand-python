from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class VehiclesAPI(API):
    """API methods for vehicles."""

    API: API = API()
    URL = API.build_api_url(path=f'/ondemand/{AGENCY}/vehicles')

    def create_vehicle(self, vehicle_data: dict) -> dict:
        """Add a vehicle using the API, then surface the vehicle ID for teardown.

        :param vehicle_data: A dictionary of vehicle data for API consumption.
        """
        return self.API.create_request(data=vehicle_data, expected_response=[200], url=self.URL)

    def delete_vehicle(self, vehicle: dict) -> None:
        """Delete a vehicle which has been successfully created.

        :param vehicle: The unique vehicle generated when a vehicle is created.
        """
        vehicle_id: int = vehicle['vehicle_id']
        delete_url: str = f'{self.URL}/{vehicle_id}'

        self.API.delete_request(expected_response=[200], url=delete_url)
