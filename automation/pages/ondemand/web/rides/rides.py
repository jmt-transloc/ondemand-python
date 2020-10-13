from pages.ondemand.web.base.base import Base
from pages.ondemand.web.rides.rides_list.rides_list import RidesList
from utilities import Selector, Selectors, WebElement


class Rides(Base):
    """Rides Page objects and methods for the OnDemand Web application."""

    URL_PATH = f'{Base.URL_PATH}/rides'
    ROOT_LOCATOR: Selector = Selectors.data_id('rides-page-container')
    _past_tab: Selector = Selectors.data_id('past')
    _tabs_container: Selector = Selectors.data_id('tabs-container')
    _upcoming_tab: Selector = Selectors.data_id('upcoming')

    @property
    def past_rides_tab(self) -> WebElement:
        return self.tabs_container.find_element(*self._past_tab)

    @property
    def rides_list(self) -> RidesList:
        return RidesList(self)

    @property
    def tabs_container(self) -> WebElement:
        return self.driver.find_element(*self._tabs_container)

    @property
    def upcoming_rides_tab(self) -> WebElement:
        return self.tabs_container.find_element(*self._upcoming_tab)
