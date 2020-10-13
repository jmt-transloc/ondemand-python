from typing import Tuple

from selenium.common.exceptions import NoSuchElementException
from utilities import Selector, Selectors, WebElement, WebElements


class AutocompleteSuggestions(object):
    """Objects and methods for autocomplete suggestions.

    :example usage:
        suggestions = AutocompleteSuggestions(self)
        suggestions.select_suggestion(location='4506 Emperor Boulevard Durham, NC, USA')
    """

    def __init__(self, page):
        self.driver = page.driver

    _places_autocomplete_suggestion: Selector = Selectors.data_id('places-autocomplete-suggestion')

    @property
    def suggestion_list(self) -> WebElements:
        return self.driver.find_elements(*self._places_autocomplete_suggestion)

    def filter_suggestions(self, location: str) -> WebElement:
        """Filter location suggestions for a match with a location.

        :param location: The location for a ride.
        """
        locations: Tuple[WebElement, ...] = tuple(
            loc for loc in self.suggestion_list if location in loc.text.replace('\n', ' ')
        )

        if not location:
            raise NoSuchElementException(f'A suggestion for: {location} could not be located.')
        return locations[0]

    def select_suggestion(self, location: str) -> None:
        """Select a location suggestion.

        :param location: The location for a ride.
        """
        self.filter_suggestions(location).click()
        self.driver.wait_until_not_present(*self._places_autocomplete_suggestion, wait_time=1)
