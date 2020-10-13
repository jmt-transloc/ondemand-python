from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class ServicesAPI(API):
    """API methods for services."""

    API: API = API()
    URL = API.build_api_url(path=f'/ondemand/{AGENCY}/services')

    def archive_service(self, service: dict) -> None:
        """Archive an expired service which has been successfully created.

        This endpoint calls True when both a 200 or 503 have been received. The reasoning for this
        is to ensure that services have been archived correctly (503 response) and if not, to
        archive them (200 response).

        :param service: The service intended for archive.
        """
        service_id: str = service['service_id']
        archive_url: str = f'{self.URL}/{service_id}'

        self.API.delete_request(expected_response=[200, 503], url=archive_url)

    def create_service(self, service_data: dict) -> dict:
        """Create a service using the API, then surface the service ID for teardown.

        :param service_data: A dictionary of service data for API consumption.
        """
        return self.API.create_request(data=service_data, expected_response=[200], url=self.URL)

    def delete_service(self, service: dict) -> None:
        """Delete a service which has been successfully created.

        :param service: The service intended for deletion.
        """
        service_id: int = service['service_id']
        destroy_url: str = f'{self.URL}/{service_id}/destroy'

        self.API.delete_request(expected_response=[200], url=destroy_url)
