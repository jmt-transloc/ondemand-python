import os
from typing import Optional

import pytest
from pages.authentication.login import Login
from pages.ondemand.admin.base.base import Base
from pytest import fixture
from selenium.common.exceptions import StaleElementReferenceException
from utilities.constants.ondemand import Admin


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestAppNavigation:
    """Battery of tests for OnDemand Admin navigation functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.base = Base(selenium)
        self.login = Login(selenium)

    @pytest.fixture(autouse=True)
    def set_state(self) -> None:
        self.base.visit()

    @pytest.mark.high
    @pytest.mark.smoke
    def test_application_logout(self) -> None:
        """Log out of the application, then check for a success state.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.
        """
        result: bool = False
        while not result:
            try:
                self.base.header.logout_link.is_displayed()
                result = True
            except StaleElementReferenceException:
                self.base.driver.refresh()

        self.base.header.logout_link.click()

        assert self.login.loaded

    @pytest.mark.low
    def test_help_link(self) -> None:
        """Copy the help link href, then ensure it matches a test constant.

        The help link href is checked instead of selecting the link due to the value of the target
        attribute causing a new browser tab to open.
        """
        result: bool = False
        while not result:
            try:
                self.base.header.help_link.is_displayed()
                result = True
            except StaleElementReferenceException:
                self.base.driver.refresh()

        link_text = self.base.header.help_link.get_attribute('href')

        assert link_text == self.base.header.HELP_LINK

    @pytest.mark.low
    def test_profile_link(self) -> None:
        """Copy the profile link href, then ensure it contains the user.

        The profile link href is checked instead of selecting the link due to the value of the
        target attribute causing a new browser tab to open.
        """
        result: bool = False
        while not result:
            try:
                self.base.header.profile_link.is_displayed()
                result = True
            except StaleElementReferenceException:
                self.base.driver.refresh()

        link_text = self.base.header.profile_link.get_attribute('href')
        username: Optional[str] = os.getenv('DEFAULT_USERNAME')

        assert username in link_text

    @pytest.mark.low
    @pytest.mark.parametrize('tab', [tab for tab in Admin.NAVIGATION_TABS])
    def test_tab_navigation(self, tab: fixture) -> None:
        """Navigate to a tab using the navigation container, then check for a success state.

        Parametrization is used in order to test all navigation scenarios.

        :param tab: The page name for navigation.
        """
        result: bool = False
        while not result:
            try:
                self.base.navigation.select_tab(tab=tab)
                result = True
            except StaleElementReferenceException:
                self.base.driver.refresh()

        assert tab.lower() in self.base.driver.current_url
