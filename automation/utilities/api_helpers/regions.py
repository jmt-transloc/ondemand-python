from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class RegionsAPI(API):
    """API methods for regions."""

    API: API = API()
    URL = API.build_api_url(path=f'/ondemand/{AGENCY}/regions')

    def create_region(self, region_data: dict) -> dict:
        """Add a region using the API, then surface the region ID for teardown.

        :param region_data: A dictionary of region data for API consumption.
        """
        return self.API.create_request(data=region_data, expected_response=[200], url=self.URL)

    def delete_region(self, region: dict) -> None:
        """Delete a region which has been successfully created.

        :param region: The unique region ID generated when a region is created.
        """
        region_id: int = region['region_id']
        delete_url: str = f'{self.URL}/{region_id}'

        self.API.delete_request(expected_response=[200], url=delete_url)
