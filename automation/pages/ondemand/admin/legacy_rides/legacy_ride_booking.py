from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.details.details import Details
from pages.ondemand.common.autocomplete_suggestions.autocomplete_suggestions import (
    AutocompleteSuggestions,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from utilities import Selector, Selectors, WebElement
from utilities.exceptions import PaymentMethodException


class LegacyRideBooking(Base):
    """Objects and methods for the Legacy Ride Booking page.

    The legacy ride booking page is a work flow which must be supported due to the volume of
    dispatchers who continue to utilize the page over the Admin Dispatch page.
    """

    URL_PATH: str = f'{Base.URL_PATH}/rides/new'

    _asap_ride_radio: Selector = Selectors.data_id('use-now')
    _driver_note: Selector = Selectors.name('note')
    _drop_off_field: Selector = Selectors.name('dropoff')
    _first_name_field: Selector = Selectors.name('first_name')
    _future_ride_radio: Selector = Selectors.data_id('use-later')
    _last_name_field: Selector = Selectors.name('last_name')
    _pay_on_vehicle_radio: Selector = Selectors.radio('cash')
    _phone_field: Selector = Selectors.name('phone')
    _pick_up_field: Selector = Selectors.name('pickup')
    _places_autocomplete_suggestion: Selector = Selectors.data_id('places-autocomplete-suggestion')
    _service_dropdown: Selector = Selectors.name('serviceId')
    _submit_ride_button: Selector = Selectors.data_id('book_ride')
    _total_passenger_field: Selector = Selectors.name('capacity')
    _waive_fee_radio: Selector = Selectors.radio('waive')
    _wheelchair_switch: Selector = Selectors.name('wheelchair')

    @property
    def asap_ride_button(self) -> WebElement:
        return self.driver.find_element(*self._asap_ride_radio)

    @property
    def driver_note_field(self) -> WebElement:
        return self.driver.find_element(*self._driver_note)

    @property
    def drop_off_field(self) -> WebElement:
        return self.driver.find_element(*self._drop_off_field)

    @property
    def first_name_field(self) -> WebElement:
        return self.driver.find_element(*self._first_name_field)

    @property
    def future_ride_button(self) -> WebElement:
        return self.driver.find_element(*self._future_ride_radio)

    @property
    def last_name_field(self) -> WebElement:
        return self.driver.find_element(*self._last_name_field)

    @property
    def pay_on_vehicle_button(self) -> WebElement:
        return self.driver.find_element(*self._pay_on_vehicle_radio)

    @property
    def phone_field(self) -> WebElement:
        return self.driver.find_element(*self._phone_field)

    @property
    def pick_up_field(self) -> WebElement:
        return self.driver.find_element(*self._pick_up_field)

    @property
    def service_dropdown(self) -> Select:
        return self.driver.find_dropdown(*self._service_dropdown)

    @property
    def submit_ride_button(self) -> WebElement:
        return self.driver.find_element(*self._submit_ride_button)

    @property
    def suggestions(self) -> AutocompleteSuggestions:
        return AutocompleteSuggestions(self)

    @property
    def total_passenger_field(self) -> WebElement:
        return self.driver.find_element(*self._total_passenger_field)

    @property
    def waive_fee_button(self) -> WebElement:
        return self.driver.find_element(*self._waive_fee_radio)

    @property
    def wheelchair_switch(self) -> WebElement:
        return self.driver.find_element(*self._wheelchair_switch)

    def fill_ride_form(self, service: dict, ride: dict) -> None:
        """Fill out the legacy ride form.

        Use send_keys for phone_field as clearing the field within the fill method causes input
        to occur at the end of the field. This results in an input failure.

        :param service: The service yielded from a service API fixture.
        :param ride: The ride intended for booking.
        """
        self.first_name_field.fill(ride['rider']['first_name'])
        self.last_name_field.fill(ride['rider']['last_name'])
        self.last_name_field.fill(Keys.TAB)
        self.phone_field.send_keys(ride['rider']['phone'])

        self.select_pick_up_location(ride['pickup']['address'])
        self.select_drop_off_location(ride['dropoff']['address'])

        #
        # Occurs further down the stack than its form location as it intermittently failed when it
        # was called first.
        #
        self.select_a_service(service['service_id'])

        if ride['note'] is not None:
            self.driver_note_field.send_keys(ride['note'])

    def pay_ride_fee(self, method: str) -> None:
        """Select a payment method based on a method string.

        :param method: A payment method for the ride.
        """
        if method == 'cash':
            self.pay_on_vehicle_button.scroll_to().click()
        elif method == 'waive':
            self.waive_fee_button.scroll_to().click()
        else:
            raise PaymentMethodException(
                f'The payment method: "{method}" is not allowed for this ride.',
            )

    def select_a_service(self, service_id: int) -> None:
        """Select a service within the service drop down.

        :param service_id: The service ID yielded from a service API fixture.
        """
        try:
            self.driver.wait_until_visible(*self._service_dropdown, wait_time=4)
            self.service_dropdown.select_by_value(service_id)
        except NoSuchElementException:
            raise NoSuchElementException(
                f'The service ID: {service_id} cannot be found within the selected agency.\n'
                f'Please select a valid service within the selected agency.',
            )

    def select_drop_off_location(self, drop_off: str) -> None:
        """Fill out a drop off location, then select an autocomplete suggestion.

        :param drop_off: The drop off location for a ride.
        """
        self.drop_off_field.fill(drop_off)
        self.suggestions.select_suggestion(drop_off)

    def select_pick_up_location(self, pick_up: str) -> None:
        """Fill out a pick up location, then select an autocomplete suggestion.

        :param pick_up: The pick up location for a ride.
        """
        self.pick_up_field.fill(pick_up)
        self.suggestions.select_suggestion(pick_up)

    def submit_ride_form(self) -> object:
        """Submit a legacy ride form."""
        self.submit_ride_button.scroll_to().click()

        return Details(self.driver).wait_for_page_to_load()
