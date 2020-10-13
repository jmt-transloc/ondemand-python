from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.details.edit_form import EditForm
from pages.ondemand.admin.details.events_list import EventsList
from pages.ondemand.admin.details.info_card import InfoCard
from utilities import Selector, Selectors, WebElement


class Details(Base):
    """Details Page objects and methods for the OnDemand Admin application.

    The Details Page contains information on the specified ride, a mapped location of the ride, and
    the tools for editing the pick up and drop off locations for the ride. The Details Page may be
    accessed from either the Rides or Dispatch pages using a 'Details' button found within a table
    or kebab menu.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('details-page-container')
    _back_button: Selector = Selectors.data_id('details-back-button')

    @property
    def back_button(self) -> WebElement:
        return self.driver.find_element(*self._back_button)

    @property
    def events_list(self) -> EventsList:
        return EventsList(self)

    @property
    def edit_form(self) -> EditForm:
        return EditForm(self)

    @property
    def info_card(self) -> InfoCard:
        return InfoCard(self)

    @property
    def ride_id(self) -> str:
        """Return a ride ID parsed from the Details page URL.

        This method conditionally removes URL parameters as the ride URL contains a date parameter
        when accessed directly from the Rides page. The ride URL does not contain a date
        parameter when redirected from ride creation.
        """
        id = self.driver.current_url.replace(f'{Base.URL_PATH}/rides/', '')

        if '?' in self.driver.current_url:
            return id[: id.find('?')]
        return id
