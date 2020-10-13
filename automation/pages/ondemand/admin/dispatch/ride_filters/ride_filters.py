from typing import List

from utilities import Component, Selector, Selectors
from utilities.constants.ondemand import Admin
from utilities.exceptions import FilterException


class RideFilters(Component):
    """Objects and methods for the Ride Filters container."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-filters-container')
    TABS: List[str] = Admin.RIDE_FILTERS

    def select_filter(self, filter_type: str) -> None:
        """Filter all ride cards based on a selected type.

        :param filter_type: The specified ride filter.
        """
        _groomed_tab: str = filter_type.lower().replace(' ', '-')

        if filter_type not in self.TABS:
            raise FilterException
        self.container.find_element(*Selectors.data_id(f'ride-filter-{_groomed_tab}')).click()
