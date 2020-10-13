from typing import Tuple, Union

from pages.ondemand.admin.rides.ride_tables.ride_row import RideRow
from utilities import Component, Selector, Selectors, WebElement


class SingleRidesTable(Component):
    """Single Rides table component objects and methods for the Rides page.

    The Single Rides table component contains ride data for all single rides within an agency.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('rides-table-container')
    _no_rides_message: Selector = Selectors.data_id('no-rides-message')

    @property
    def no_rides_message(self) -> WebElement:
        return self.container.find_element(*self._no_rides_message)

    @property
    def ride_rows(self) -> Union[Tuple[RideRow, ...], None]:
        try:
            return tuple(
                RideRow(self, element)
                for element in self.container.find_elements(*RideRow.ROOT_LOCATOR)
            )
        except TypeError:
            return None

    def filter_rows(self, ride: dict) -> Union[RideRow, None]:
        """Filter all ride rows for a match with a rider name.

        :param ride: The ride yielded from a ride fixture.
        """
        rider: dict = ride['rider']
        rider_name: str = f'{rider["first_name"]} {rider["last_name"]}'

        ride_list: Tuple[RideRow, ...] = tuple(
            row for row in self.ride_rows if row.ride_name == rider_name
        )

        if not ride_list:
            return None
        return ride_list[0]

    def surface_ride_row(self, ride: dict) -> RideRow:
        """Raise a ride row that matches a rider name.

        :param ride: The ride yielded from a ride fixture.
        """
        return self.filter_rows(ride)
