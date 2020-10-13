import os

import pytest
from pages.ondemand.admin.reports.reports import Reports
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.ui
class TestPermissions:
    """Battery of tests for OnDemand Admin Reports page permissions."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in permissions testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.reports: Reports = Reports(selenium)

    @pytest.mark.role_admin
    def test_admin__reports_access(self) -> None:
        """Check that Admin users may access the Reports page."""
        self.reports.visit()

        assert self.reports.sidebar.loaded is True

    @pytest.mark.role_agent
    def test_agent__reports_no_access(self) -> None:
        """Check that Agent users may not access the Reports page."""
        self.reports.visit()

        assert self.reports.sidebar.loaded is False

    @pytest.mark.role_dispatcher
    def test_dispatcher__reports_access(self) -> None:
        """Check that Dispatcher users may access the Reports page."""
        self.reports.visit()

        assert self.reports.sidebar.loaded is True

    @pytest.mark.role_driver
    @pytest.mark.skipif(os.environ['ENV'] == 'localhost', reason='Proxy is skipped on localhost.')
    def test_driver__no_reports_access(self) -> None:
        """Check that Driver users may not access the Reports page."""
        self.reports.visit()

        assert self.reports.sidebar.loaded is False

    @pytest.mark.role_rider
    def test_rider__no_reports_access(self) -> None:
        """Check that Rider users may not access the Reports page."""
        self.reports.visit()

        assert self.reports.sidebar.loaded is False
