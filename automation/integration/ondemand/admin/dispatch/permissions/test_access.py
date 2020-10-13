import os

import pytest
from pages.ondemand.admin.dispatch.dispatch import Dispatch
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.ui
class TestPermissions:
    """Battery of tests for OnDemand Admin Dispatch page permissions."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in permissions testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.dispatch: Dispatch = Dispatch(selenium)

    @pytest.mark.role_admin
    def test_admin__dispatch_access(self) -> None:
        """Check that Admin users may access the Dispatch page."""
        self.dispatch.visit()

        assert self.dispatch.loaded is True

    @pytest.mark.role_agent
    def test_agent__dispatch_no_access(self) -> None:
        """Check that Agent users may not access the Dispatch page."""
        self.dispatch.visit()

        assert self.dispatch.loaded is False

    @pytest.mark.role_dispatcher
    def test_dispatcher__dispatch_access(self) -> None:
        """Check that Dispatcher users may access the Dispatch page."""
        self.dispatch.visit()

        assert self.dispatch.loaded is True

    @pytest.mark.role_driver
    @pytest.mark.skipif(os.environ['ENV'] == 'localhost', reason='Proxy is skipped on localhost.')
    def test_driver__no_dispatch_access(self) -> None:
        """Check that Driver users may not access the Dispatch page."""
        self.dispatch.visit()

        assert self.dispatch.loaded is False

    @pytest.mark.role_rider
    def test_rider__no_dispatch_access(self) -> None:
        """Check that Rider users may not access the Dispatch page."""
        self.dispatch.visit()

        assert self.dispatch.loaded is False
