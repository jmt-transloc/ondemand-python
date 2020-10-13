from conftest import build_site_url
from pages.ondemand.common.navigation_tabs.tabs import Tabs
from utilities import Page
from utilities.constants.ondemand import Web


class Base(Page):
    """Base page objects and methods for the OnDemand Web application."""

    URL_PATH = build_site_url(app='ondemand')

    @property
    def navigation(self) -> Tabs:
        return Tabs(
            self,
            tabs=[tab for tab in Web.NAVIGATION_TABS],
            selector='sidebar-navigation-container',
        )
