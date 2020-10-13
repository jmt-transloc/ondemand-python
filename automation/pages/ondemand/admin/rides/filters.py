from selenium.webdriver.common.keys import Keys
from utilities import Component, Selector, Selectors, WebElement


class Filters(Component):
    """Filters component objects and methods for the Rides page.

    The Filters component allows administrators to filter current, completed, or cancelled rides
    by service, rider name, or date.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('filters-container')
    _date_filter: Selector = Selectors.data_id('date')
    _service_filter: Selector = Selectors.data_id('service-filter')
    _service_filter_list: Selector = Selectors.role('listbox')
    _text_filter: Selector = Selectors.data_id('filter')

    @property
    def date_filter(self) -> WebElement:
        return self.container.find_element(*self._date_filter)

    @property
    def service_filter(self) -> WebElement:
        return self.container.find_element(*self._service_filter)

    @property
    def text_filter(self) -> WebElement:
        return self.container.find_element(*self._text_filter)

    def filter_by_date(self, date: str) -> None:
        """Filter ride rows by date input.

        :param date: The specified date.
        """
        self.container.wait_until_visible(*self._date_filter)
        self.date_filter.fill_picker_input(date)

    def filter_by_ride_info(self, ride_info: str):
        """Filter ride rows by either rider name or PU/DO destination.

        :param ride_info: PU/DO destination or Rider name.
        """
        self.text_filter.fill(ride_info)

    def filter_service_by_id(self, service_id: int) -> None:
        """Open the service filter, select a service by ID, then close the filter.

        :param service_id: A service ID yielded from a service fixture.
        """
        service_list = self.open_service_filter()
        service = self.page.driver.mouse_over_element(*Selectors.data_id(str(service_id)))
        service.click()

        service_list.send_keys(Keys.ESCAPE)

    def open_service_filter(self) -> WebElement:
        """Open the service filter, then verify it opened successfully."""
        self.service_filter.click()

        return self.page.driver.wait_until_visible(*self._service_filter_list)
