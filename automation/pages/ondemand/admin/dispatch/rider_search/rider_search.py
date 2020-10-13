from utilities import Component, Selector, Selectors, WebElement
from utilities.exceptions import SearchException


class RiderSearch(Component):
    """Objects and methods for the Rider Search form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('search-container')
    _clear_button: Selector = Selectors.data_id('search-clear')
    _input_field: Selector = Selectors.data_id('search-input')
    _search_button: Selector = Selectors.data_id('search-icon')

    @property
    def clear_button(self) -> WebElement:
        return self.container.find_element(*self._clear_button)

    @property
    def input_field(self) -> WebElement:
        return self.container.find_element(*self._input_field)

    @property
    def search_button(self) -> WebElement:
        return self.container.find_element(*self._search_button)

    def fill_search_field(self, input_type: str, ride: dict) -> None:
        """Fill out the rider search form.

        :param input_type: The type of search.
        :param ride: The ride yielded from a ride fixture.
        """
        rider = ride['rider']
        ride_email = rider['email']
        ride_name = f'{rider["first_name"]} {rider["last_name"]}'
        ride_phone = rider['phone']

        accepted_types: dict = {'email': ride_email, 'name': ride_name, 'phone': ride_phone}

        self.search_button.click()

        if input_type not in accepted_types:
            raise SearchException
        self.input_field.fill(accepted_types[input_type])
