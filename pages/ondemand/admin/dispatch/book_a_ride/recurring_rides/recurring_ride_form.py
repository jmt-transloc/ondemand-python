from datetime import datetime
from typing import List, Set

from utilities import Component, Selector, Selectors, WebElement
from utilities.exceptions import SelectionException


class RecurringRideForm(Component):
    """Objects and methods for the recurring ride form."""

    ROOT_LOCATOR: Selector = Selectors.data_id('recurring-ride-container')
    _end_date_field: Selector = Selectors.name('endDate')
    _start_date_field: Selector = Selectors.name('startDate')
    _time_field: Selector = Selectors.name('time')
    _days: List[str] = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
    ]

    @property
    def end_date_field(self) -> WebElement:
        return self.container.find_element(*self._end_date_field)

    @property
    def start_date_field(self) -> WebElement:
        return self.container.find_element(*self._start_date_field)

    @property
    def time_field(self) -> WebElement:
        return self.container.find_element(*self._time_field)

    def fill_recurring_ride_form(self, recurring_ride: dict) -> None:
        """Fill out the recurring ride form.

        Each timestamp must be converted into a datetime object, then converted to specific strings
        for input. For day names, the datetime objects are processed through a set comprehension
        and for loop which selects each day within the total listing. Set is used so that only one
        entry is ever selected.

        The ride.pickup datetime object is input to the start date field while the last datetime
        object within the ride_schedule list is input to the end date field. Finally, the time is
        parsed from the first datetime object and passed to the time field since the time of each
        ride will always be the same.

        :param recurring_ride: The recurring ride yielded from a recurring ride fixture.
        """
        rides: List[dict] = recurring_ride['rides']
        ride_start_date: datetime = datetime.strptime(
            recurring_ride['ride']['pickup']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ',
        )
        ride_schedule: List[datetime] = [
            datetime.strptime(date_string['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            for date_string in rides
        ]
        ride_days: Set[str] = {day.strftime('%A') for day in ride_schedule}
        ride_time: datetime = datetime.strptime(rides[0]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

        for day in ride_days:
            self.select_day(day)

        self.start_date_field.fill_picker_input(ride_start_date.strftime('%m-%d-%Y'))
        self.end_date_field.fill_picker_input(ride_schedule[-1].strftime('%m-%d-%Y'))
        self.time_field.fill_picker_input(ride_time.strftime('%I:%M %p'))

    def select_day(self, day: str) -> None:
        """Select a specific day for a recurring ride schedule.

        :param day: The specified day.
        """
        _groomed_day: str = day.lower()

        if day not in self._days:
            raise SelectionException(f'The day: {day} is invalid. Please enter a valid day.')
        self.container.find_element(
            *Selectors.data_test_id(f'day-of-week-input-{_groomed_day}'),
        ).click()
