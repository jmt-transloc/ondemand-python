from conftest import build_site_url
from environs import Env
from pages.ondemand.admin.base.header import Header
from pages.ondemand.common.navigation_tabs.tabs import Tabs
from utilities import Page
from utilities.constants.ondemand import Admin


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


class Base(Page):
    """Base Page objects and methods for the OnDemand Admin application."""

    URL_PATH = build_site_url(app='ondemand', path=f'/admin/{AGENCY}')

    @property
    def header(self: Page) -> Header:
        return Header(self)

    @property
    def navigation(self: Page) -> Tabs:
        return Tabs(
            self,
            tabs=[tab for tab in Admin.NAVIGATION_TABS],
            selector='header-navigation-container',
        )
