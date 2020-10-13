from pages.ondemand.web.agency.agency_select.agency_select import AgencySelectModal
from pages.ondemand.web.agency.service_list.service_list import ServiceList
from pages.ondemand.web.base.base import Base
from utilities import Selector, Selectors, WebElement


class Agency(Base):
    """Agency Page objects and methods for the OnDemand Web application."""

    ROOT_LOCATOR: Selector = Selectors.data_id('agency-page-container')
    _agency_email: Selector = Selectors.data_id('agency-email')
    _agency_name: Selector = Selectors.data_id('agency-name')
    _agency_phone: Selector = Selectors.data_id('agency-phone')
    _edit_agency_button: Selector = Selectors.data_id('edit-agency-button')

    @property
    def edit_agency_button(self) -> WebElement:
        return self.driver.find_element(*self._edit_agency_button)

    @property
    def email(self) -> str:
        return self.driver.find_element(*self._agency_email).text

    @property
    def name(self) -> str:
        return self.driver.find_element(*self._agency_name).text

    @property
    def phone(self) -> str:
        return self.driver.find_element(*self._agency_phone).text

    @property
    def service_list(self) -> ServiceList:
        return ServiceList(self)

    def edit_agency(self) -> object:
        """Open the agency select modal."""
        self.edit_agency_button.click()

        return AgencySelectModal(self).wait_for_component_to_be_present()
