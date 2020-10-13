from typing import Tuple

from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors

from .scheduled_ride_row import ScheduledRideRow


class ScheduledRidesList(Component):
    """Objects and methods for the Scheduled Ride list."""

    ROOT_LOCATOR: Selector = Selectors.data_id('scheduled-rides-container')

    @property
    def scheduled_rides(self) -> Tuple[ScheduledRideRow, ...]:
        return tuple(
            ScheduledRideRow(self, ele)
            for ele in self.container.find_elements(*ScheduledRideRow.ROOT_LOCATOR)
        )

    def cancel_scheduled_ride(self) -> None:
        """Cancel the first ride in the scheduled rides container.

        This method will always cancel the first ride as it is the only ride that can be cancelled
        in the entire series. All other rides will feature a 'Delete' button as they will be
        of status 'Scheduled' instead of 'Booked'.
        """
        self.scheduled_rides[0].cancel_button.click()

    def delete_scheduled_ride(self, date: str) -> None:
        """Delete a scheduled ride.

        :param date: A specified date in MM-DD-YYYY format.
        """
        ride_row: ScheduledRideRow = self.filter_scheduled_rides(date)
        ride_row.delete_ride()

    def filter_scheduled_rides(self, date: str) -> ScheduledRideRow:
        """Filter all scheduled rides for a match with a specific date.

        :param date: A specified date in MM-DD-YYYY format.
        """
        ride_list: Tuple[ScheduledRideRow, ...] = tuple(
            ride for ride in self.scheduled_rides if ride.date == date
        )

        if not ride_list:
            raise NoSuchElementException(f'A ride could not be found for the date: {date}.')
        return ride_list[0]
