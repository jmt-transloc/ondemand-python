import os

import pytest
from pages.ondemand.admin.resources.resources import Resources
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.ui
class TestPermissions:
    """Battery of tests for OnDemand Admin Resources page permissions."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in permissions testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.resources: Resources = Resources(selenium)

    @pytest.mark.role_admin
    def test_admin__resources_access(self) -> None:
        """Check that Admin users may access the Resources page."""
        self.resources.visit()

        assert self.resources.sidebar.loaded is True

    @pytest.mark.role_agent
    def test_agent__resources_no_access(self) -> None:
        """Check that Agent users may not access the Resources page."""
        self.resources.visit()

        assert self.resources.sidebar.loaded is False

    @pytest.mark.role_dispatcher
    def test_dispatcher__resources_access(self) -> None:
        """Check that Dispatcher users may access the Resources page."""
        self.resources.visit()

        assert self.resources.sidebar.loaded is True

    @pytest.mark.role_driver
    @pytest.mark.skipif(os.environ['ENV'] == 'localhost', reason='Proxy is skipped on localhost.')
    def test_driver__no_resources_access(self) -> None:
        """Check that Driver users may not access the Resources page."""
        self.resources.visit()

        assert self.resources.sidebar.loaded is False

    @pytest.mark.role_rider
    def test_rider__no_resources_access(self) -> None:
        """Check that Rider users may not access the Resources page."""
        self.resources.visit()

        assert self.resources.sidebar.loaded is False
