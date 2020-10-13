from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.edit_service.edit_service import EditService
from pages.ondemand.admin.services.locations.locations import Locations
from pages.ondemand.admin.services.service_cards.service_card_list import ServiceCardList
from utilities import Selector, Selectors


class Services(Base):
    """Services Page objects and methods for the OnDemand Admin application."""

    URL_PATH: str = f'{Base.URL_PATH}/services'
    ROOT_LOCATOR: Selector = Selectors.data_id('services-page-container')

    @property
    def service_card_list(self) -> ServiceCardList:
        return ServiceCardList(self)

    def navigate_to_edit_by_service_id(self, service: dict) -> object:
        """Navigate to the Details Page for a specific service using a direct URL.

        This is a useful method for bypassing the application work flows following creation of a
        service using the API.

        :param service: The service yielded from a service fixture.
        """
        service_id: int = service['service_id']
        service_details_url: str = f'{self.URL_PATH}/{service_id}/details'
        self.driver.get(service_details_url)

        return EditService(self.driver, service_details_url).wait_for_page_to_load()

    def navigate_to_locations_by_service(self, service: dict) -> object:
        """Navigate to the Locations page for a specific service using a direct URL.

        This is a useful method for bypassing the application work flows following creation of a
        service using the API.

        :param service: The service intended for navigation.
        """
        service_id: int = service['service_id']
        locations_url = f'{self.URL_PATH}/{service_id}/locations'
        self.driver.get(locations_url)

        return Locations(self)
