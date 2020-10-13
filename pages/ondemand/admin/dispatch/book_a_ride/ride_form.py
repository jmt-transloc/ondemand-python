from pages.ondemand.common.autocomplete_suggestions.autocomplete_suggestions import (
    AutocompleteSuggestions,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from utilities import Component, Selector, Selectors, WebElement


class RideForm(Component):
    """Objects and methods for the Ride form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-details-container')
    _driver_note_field: Selector = Selectors.name('note')
    _drop_off_field: Selector = Selectors.name('dropoff')
    _pick_up_field: Selector = Selectors.name('pickup')
    _service_drop_down: Selector = Selectors.name('serviceId')
    _service_drop_down_error: Selector = Selectors.data_id('service-dropdown-with-errors')
    _total_passenger_field: Selector = Selectors.name('capacity')
    _wheelchair_check_box: Selector = Selectors.name('wheelchair')

    @property
    def driver_note_field(self) -> WebElement:
        return self.container.find_element(*self._driver_note_field)

    @property
    def drop_off_field(self) -> WebElement:
        return self.container.find_element(*self._drop_off_field)

    @property
    def pick_up_field(self) -> WebElement:
        return self.container.find_element(*self._pick_up_field)

    @property
    def service_drop_down(self) -> Select:
        return self.container.find_dropdown(*self._service_drop_down)

    @property
    def suggestions(self) -> AutocompleteSuggestions:
        return AutocompleteSuggestions(self)

    @property
    def total_passenger_field(self) -> WebElement:
        return self.container.find_element(*self._total_passenger_field)

    @property
    def wheelchair_check_box(self) -> WebElement:
        return self.container.find_element(*self._wheelchair_check_box)

    def fill_ride_info_form(self, service: dict, ride: dict) -> None:
        """Fill out the ride information form.

        The ride param may be of type RecurringRide or Ride depending on the test which is being
        ran. The default type will be Ride as it is the most common data type for testing.

        :param service: The service yielded from a service API fixture.
        :param ride: A ride yielded from a ride fixture.
        """
        try:
            ride_data = ride['ride']
        except KeyError:
            ride_data = ride

        dropoff: dict = ride_data['dropoff']
        note: str = ride_data['note']
        pickup: dict = ride_data['pickup']

        self.select_a_service(service['service_id'])
        self.select_pick_up_location(pickup['address'])
        self.select_drop_off_location(dropoff['address'])

        if note is not None:
            self.driver_note_field.send_keys(note)

    def select_a_service(self, service_id: str) -> None:
        """Select a service within the service drop down.

        :param service_id: The service ID yielded from a service API fixture.
        """
        try:
            self.service_drop_down.select_by_value(service_id)
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

    def service_error_check(self) -> bool:
        return self.container.find_element(*self._service_drop_down_error).is_displayed()
