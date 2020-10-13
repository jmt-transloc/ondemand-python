from utilities import Component, Selector, Selectors, WebElement
from utilities.exceptions import RideTypeException


class ScheduleForm(Component):
    """Objects and methods for the Schedule form.

    The Schedule Form component contains toggles and pickers for editing a ride's pickup time from
    within the Details page.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-edit-future-container')

    _asap_ride_button: Selector = Selectors.data_id('ride-edit-asap-button')
    _future_ride_button: Selector = Selectors.data_id('ride-edit-future-button')
    _date_field: Selector = Selectors.name('pickupDate')
    _time_field: Selector = Selectors.name('time')

    @property
    def asap_ride_button(self) -> WebElement:
        return self.container.find_element(*self._asap_ride_button)

    @property
    def date_field(self) -> WebElement:
        return self.container.find_element(*self._date_field)

    @property
    def future_ride_button(self) -> WebElement:
        return self.container.find_element(*self._future_ride_button)

    @property
    def time_field(self) -> WebElement:
        return self.container.find_element(*self._time_field)

    def select_ride_type(self, ride_type: str) -> None:
        """Select a ride type.

        Ride type defaults to ASAP within the OnDemand Admin application.

        :param ride_type: The type of ride to be submitted.
        """
        if ride_type == 'future':
            self.future_ride_button.click()
        elif ride_type != 'asap':
            raise RideTypeException(
                f'The ride type: {ride_type} is not supported.\n'
                f'Expected "asap" or "future"." or "recurring".',
            )


class EditForm(Component):
    """Edit Form component objects and methods for the Rides Info component.

    The Edit Form component contains tools for editing the pick up and drop off locations for a
    ride featured within the Details page. The Edit Form may be accessed from the Ride Info
    component.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('details-edit-ride-container')

    _pick_up_address: Selector = Selectors.name('pickup')
    _drop_off_address: Selector = Selectors.name('dropoff')
    _swap_button: Selector = Selectors.data_id('edit-swap-button')
    _update_button: Selector = Selectors.data_id('edit-update-button')
    _cancel_button: Selector = Selectors.data_id('edit-cancel-button')
    _total_passenger_field: Selector = Selectors.name('capacity')
    _wheelchair_check_box: Selector = Selectors.name('wheelchair')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def drop_off_address(self) -> WebElement:
        return self.container.find_element(*self._drop_off_address)

    @property
    def pick_up_address(self) -> WebElement:
        return self.container.find_element(*self._pick_up_address)

    @property
    def schedule_form(self) -> ScheduleForm:
        return ScheduleForm(self)

    @property
    def swap_button(self) -> WebElement:
        return self.container.find_element(*self._swap_button)

    @property
    def total_passenger_field(self) -> WebElement:
        return self.container.find_element(*self._total_passenger_field)

    @property
    def update_button(self) -> WebElement:
        return self.container.find_element(*self._update_button)

    @property
    def wheelchair_check_box(self) -> WebElement:
        return self.container.find_element(*self._wheelchair_check_box)

    def swap_addresses(self) -> None:
        """Select the swap button, then save the edit."""
        self.swap_button.click()

        self.update_button.click()
