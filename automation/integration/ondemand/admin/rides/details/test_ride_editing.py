from typing import Tuple

import factory
import pytest
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestEditRides:
    """Battery of tests for ride edit functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used for testing Details page ride editing."""
        self.rides = Rides(selenium)
        self.details = Details(selenium)

    @pytest.mark.high
    @pytest.mark.smoke
    @pytest.mark.xfail(
        reason='This is an escape and will be fixed in Sprint 119.',
    )  # TODO(J. Thompson) Remove once fixed
    def test_swap_ride_pu_do(self, ride_factory: factory, service_with_in_advance: fixture) -> None:
        """Swap an existing ride PU/DO, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        ride: dict = ride_factory.create(service=service_with_in_advance, future_ride=True)

        self.rides.navigate_to_details_by_ride_id(ride)

        before: Tuple[str, str] = (
            self.details.events_list.ride_requested_card.pick_up_address,
            self.details.events_list.ride_requested_card.drop_off_address,
        )

        self.details.info_card.open_ride_edit_form()
        self.details.edit_form.swap_addresses()

        after: Tuple[str, str] = (
            self.details.events_list.ride_requested_card.pick_up_address,
            self.details.events_list.ride_requested_card.drop_off_address,
        )

        assert before != after
