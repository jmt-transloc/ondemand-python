import os

import pytest
from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.rides.rides import Rides
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.ui
class TestPermissions:
    """Battery of tests for OnDemand Admin permissions.

    These tests check access to the OnDemand Admin application by navigating to the base page. This
    will redirect the user to the Rides page which will be used for a content check. Should the
    Rides page sidebar be visible, then the user has access. Should it not, then the user does not
    have access.

    This is an MVP check as our current roles are not fine tuned enough to block out Rider users
    from accessing Admin at all. Instead, blank pages with a header show which is misleading.
    """

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in permissions testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.base: Base = Base(selenium)
        self.rides: Rides = Rides(selenium)

    @pytest.mark.role_admin
    def test_admin__ondemand_admin_access(self) -> None:
        """Check that Admin users may access OnDemand Admin."""
        self.base.visit()

        assert self.rides.sidebar.loaded is True

    @pytest.mark.role_agent
    def test_agent__ondemand_admin_access(self) -> None:
        """Check that Agent users may access OnDemand Admin."""
        self.base.visit()

        assert self.rides.sidebar.loaded is True

    @pytest.mark.role_dispatcher
    def test_dispatcher__ondemand_admin_access(self) -> None:
        """Check that Dispatcher users may access OnDemand Admin."""
        self.base.visit()

        assert self.rides.sidebar.loaded is True

    @pytest.mark.role_driver
    @pytest.mark.skipif(os.environ['ENV'] == 'localhost', reason='Proxy is skipped on localhost.')
    def test_driver__no_ondemand_admin_access(self) -> None:
        """Check that Driver users may not access OnDemand Admin."""
        self.base.visit()

        assert self.rides.sidebar.loaded is False

    @pytest.mark.role_rider
    def test_rider__no_ondemand_admin_access(self) -> None:
        """Check that Rider users may not access OnDemand Admin."""
        self.base.visit()

        assert self.rides.sidebar.loaded is False
