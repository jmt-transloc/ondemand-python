from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class AddressesAPI(API):
    """API methods for addresses."""

    API: API = API()
    URL: str = API.build_api_url(path=f'/ondemand/{AGENCY}/addresses')

    def create_address(self, address_data: dict, url: str) -> dict:
        """Add an address using the API, then surface the address ID for teardown.

        This method does not utilize the base self.URL attribute as it requires a url to be passed
        from the creation of the address dictionary. This is due to the separation between Web and
        Admin address creation.

        :param address_data: A dictionary of address data for API consumption.
        :param url: An application URL yielded from the Address Factory.
        """
        if 'url' in address_data:
            del address_data['url']

        return self.API.create_request(data=address_data, expected_response=[200], url=url)

    def delete_address(self, address: dict, rider_address: bool) -> None:
        """Add an address using the API, then surface the address ID for teardown.

        :param address: The address intended for deletion.
        :param rider_address: Boolean for whether the address is web or not.
        """
        address_id: int = address['address_id']
        if rider_address:
            self.URL = self.API.build_api_url('/me/rider/addresses')
        delete_url: str = f'{self.URL}/{address_id}'

        self.API.delete_request(expected_response=[200], url=delete_url)
