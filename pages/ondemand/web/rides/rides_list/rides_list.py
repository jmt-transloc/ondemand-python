from typing import Tuple

from pages.ondemand.web.rides.rides_list.ride_row import RideRow
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors, WebElements


class RidesList(Component):
    """Objects and methods for the Rides List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-list-container')

    @property
    def ride_rows(self) -> Tuple[RideRow, ...]:
        rows: WebElements = self.container.find_elements(*RideRow.ROOT_LOCATOR)

        return tuple(RideRow(self, element) for element in rows)

    def filter_rows(self, ride_id: str) -> RideRow:
        """Filter all ride rows for a match with a ride id.

        :param ride_id: The unique ride ID for a ride.
        """
        row_list: Tuple[RideRow, ...] = tuple(
            row for row in self.ride_rows if row.ride_id == ride_id
        )

        if not row_list:
            raise NoSuchElementException
        return row_list[0]

    def surface_ride_row(self, ride_id: str) -> RideRow:
        """Raise a ride row that matches a ride id.

        :param ride_id: The unique ride ID for a ride.
        """
        return self.filter_rows(ride_id)
