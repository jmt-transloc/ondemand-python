from utilities import Component, Selector, Selectors, WebElement


class PassengerForm(Component):
    """Objects and methods for the Passenger form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('user-details-container')
    _first_name_field: Selector = Selectors.name('first_name')
    _last_name_field: Selector = Selectors.name('last_name')
    _phone_field: Selector = Selectors.name('phone')

    @property
    def first_name_field(self) -> WebElement:
        return self.container.find_element(*self._first_name_field)

    @property
    def last_name_field(self) -> WebElement:
        return self.container.find_element(*self._last_name_field)

    @property
    def phone_field(self) -> WebElement:
        return self.container.find_element(*self._phone_field)

    def fill_passenger_info_form(self, ride: dict) -> None:
        """Fill out the passenger information form.

        The ride param may be of type RecurringRide or Ride depending on the test which is being
        ran. The default type will be Ride as it is the most common data type for testing.

        :param ride: A ride yielded from a ride fixture.
        """
        try:
            rider = ride['ride']['rider']
        except KeyError:
            rider = ride['rider']

        self.first_name_field.fill(rider['first_name'])
        self.last_name_field.fill(rider['last_name'])
        self.phone_field.fill(rider['phone'])
