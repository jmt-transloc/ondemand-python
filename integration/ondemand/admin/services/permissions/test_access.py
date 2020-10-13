import os

import pytest
from pages.ondemand.admin.services.services import Services
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.permissions
@pytest.mark.ui
class TestPermissions:
    """Battery of tests for OnDemand Admin Services page permissions."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in permissions testing.

        :param selenium: An instance of Selenium web driver.
        """
        self.services: Services = Services(selenium)

    @pytest.mark.role_admin
    def test_admin__services_access(self) -> None:
        """Check that Admin users may access the Services page."""
        self.services.visit()

        assert self.services.service_card_list.loaded is True

    @pytest.mark.role_agent
    def test_agent__no_services_access(self) -> None:
        """Check that Agent users may not access the Services page."""
        self.services.visit()

        assert self.services.service_card_list.loaded is False

    @pytest.mark.role_dispatcher
    def test_dispatcher__services_access(self) -> None:
        """Check that Dispatcher users may access the Services page."""
        self.services.visit()

        assert self.services.service_card_list.loaded is True

    @pytest.mark.role_driver
    @pytest.mark.skipif(os.environ['ENV'] == 'localhost', reason='Proxy is skipped on localhost.')
    def test_driver__no_services_access(self) -> None:
        """Check that Driver users may not access the Services page."""
        self.services.visit()

        assert self.services.service_card_list.loaded is False

    @pytest.mark.role_rider
    @pytest.mark.xfail
    def test_rider__no_services_access(self) -> None:
        """Check that Rider users may not access the Services page.

        Marked to fail as Rider users currently have access to the Services page.
        """
        self.services.visit()

        assert self.services.service_card_list.loaded is False
