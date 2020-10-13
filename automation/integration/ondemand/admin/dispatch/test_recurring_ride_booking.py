from datetime import datetime

import pytest
from factory import Factory
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pytest import fixture


class TestDispatchRecurringRides:
    """Battery of tests for Dispatch page recurring ride booking functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in ASAP ride testing."""
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking__same_day__asap(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ) -> None:
        """Book a same day ASAP recurring ride, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build()
        rider: dict = ride['ride']['rider']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert self.dispatch.ride_subscription_modal.ride_placard.rider_name == rider_name

    @pytest.mark.medium
    def test_booking__same_day__future_time(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ):
        """Book a same day future time recurring ride, then check for a success state.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build(same_day_future_recurring_ride=True)
        ride_time: datetime = datetime.strptime(
            ride['rides'][0]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ',
        )
        actual_time: str = ride_time.strftime('%I:%M %p')

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert actual_time in self.dispatch.ride_subscription_modal.message

    @pytest.mark.medium
    def test_booking__future_day(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ):
        """Book a future day recurring ride, then check for a success state.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build(future_recurring_ride=True)
        ride_start: datetime = datetime.strptime(
            ride['ride']['pickup']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ',
        )
        ride_end: datetime = datetime.strptime(
            ride['rides'][-1]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ',
        )
        actual_start: str = ride_start.strftime('%b %d, %Y')
        actual_end: str = ride_end.strftime('%b %d, %Y')

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert actual_start and actual_end in self.dispatch.ride_subscription_modal.message

    @pytest.mark.high
    @pytest.mark.smoke
    def test_booking__limited_in_advance(
        self, recurring_ride_factory: Factory, service_with_limited_recurring_rides: fixture,
    ):
        """Book a recurring ride using a limited service, then check for an error state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_limited_recurring_rides: A limited recurring rides service.
        """
        ride: dict = recurring_ride_factory.build()

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_limited_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        errors = self.dispatch.ride_subscription_modal.subscription_errors

        assert errors.container.visible is True

    @pytest.mark.low
    def test_booking__with_note(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ):
        """Book a same day ASAP recurring ride with a note, then check for a success state.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build(ride_with_note=True)
        note: str = ride['ride']['note']

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert (
            self.dispatch.ride_subscription_modal.ride_placard.driver_note == f'Driver Note: {note}'
        )

    @pytest.mark.low
    def test_recurring_rides_require_enabled_service(
        self, recurring_ride_factory: Factory, service: fixture,
    ):
        """Attempt to book with an non-recurring rides service, then check for an error state.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service: A non-recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build()

        self.dispatch.visit()

        self.dispatch.fill_ride_form(service, ride=ride)
        assert self.dispatch.ride_booking_panel.schedule_form.loaded is False

    @pytest.mark.low
    def test_submission_modal_features_rides_link(
        self, recurring_ride_factory: Factory, service_with_recurring_rides: fixture,
    ):
        """Book a recurring ride, then check for a rides link in the submission modal.

        :param recurring_ride_factory: A factory for building recurring rides via the API or UI.
        :param service_with_recurring_rides: A recurring rides service yielded by the API.
        """
        ride: dict = recurring_ride_factory.build()

        self.dispatch.visit()

        self.dispatch.fill_ride_form(
            service=service_with_recurring_rides, ride=ride,
        )
        self.dispatch.ride_booking_panel.schedule_form.select_ride_type('recurring')
        self.dispatch.fill_recurring_ride_form(ride)
        self.dispatch.ride_booking_panel.submit_ride_form()

        assert self.dispatch.ride_subscription_modal.rides_page_link.visible is True
