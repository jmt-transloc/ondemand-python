import pytest
from pages.authentication.login import Login
from pages.ondemand.web.base.base import Base
from pages.ondemand.web.booking.booking import Booking
from pytest import fixture


@pytest.mark.ondemand_web
@pytest.mark.ui
class TestAppNavigation:
    """Battery of tests for OnDemand Web navigation functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.base = Base(selenium)
        self.booking = Booking(selenium)
        self.login = Login(selenium)

    @pytest.fixture(autouse=True)
    def set_state(self) -> None:
        self.base.visit()
        self.booking.agency_select_modal.main_menu_link.click()

    @pytest.mark.high
    @pytest.mark.smoke
    def test_application_logout(self) -> None:
        """Log out of the application, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        self.base.navigation.select_tab(tab='Logout')

        assert self.login.loaded

    @pytest.mark.low
    @pytest.mark.parametrize(
        'tab, expected',
        [
            ('Book a Ride', ''),
            ('Agency', 'agency'),
            ('My Addresses', 'addresses'),
            ('My Rides', 'rides'),
        ],
    )
    def test_tab_navigation(self, tab: fixture, expected: fixture) -> None:
        """Navigate to a tab using the navigation container, then check for a success state.

        Parametrization is used in order to test all navigation scenarios.

        :param tab: The page name for navigation.
        :param expected: The expected URL path.
        """
        self.base.navigation.select_tab(tab=tab)

        assert expected in self.base.driver.current_url
