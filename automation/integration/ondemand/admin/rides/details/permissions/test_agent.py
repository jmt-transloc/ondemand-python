import pytest
from factory import Factory
from pages.ondemand.admin.details.details import Details
from pages.ondemand.admin.legacy_rides.legacy_ride_booking import LegacyRideBooking
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.role_agent
@pytest.mark.ui
class TestAgentPermissions:
    """Battery of tests for Agent role permissions on the Rides page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Agent role Rides page testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.details: Details = Details(selenium)
        self.legacy_rides: LegacyRideBooking = LegacyRideBooking(selenium)
        self.rides: Rides = Rides(selenium)

    @pytest.mark.medium
    def test_booked_rides__access(self, ride_factory: Factory, service: fixture) -> None:
        """As an Agent, ensure that I may view the Details page for a ride that I have booked.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        agent_ride: dict = ride_factory.build()

        self.rides.visit()

        self.rides.navigate_to_legacy_ride_booking()
        self.legacy_rides.fill_ride_form(service, ride=agent_ride)
        self.legacy_rides.submit_ride_form()

        assert bool(self.details.loaded) is True

    @pytest.mark.medium
    @pytest.mark.xfail(
        reason='Agents may access Ride Details',
    )  # TODO(J. Thompson) Remove once fixed
    def test_booked_rides__no_access(self, ride_factory: Factory, service: fixture) -> None:
        """As an Agent, ensure that I may not view the Details page for a ride I have not booked.

        :param ride_factory: A factory for building rides via the API or UI.
        :param service: A service yielded by the API.
        """
        ride: dict = ride_factory.create(service=service)

        self.rides.navigate_to_details_by_ride_id(ride)

        assert bool(self.details.loaded) is False
