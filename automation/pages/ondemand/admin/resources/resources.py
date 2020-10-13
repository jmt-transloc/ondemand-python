from pages.ondemand.admin.base.base import Base
from pages.ondemand.common.navigation_tabs.tabs import Tabs
from utilities import Selector, Selectors
from utilities.constants.ondemand import Admin


class Resources(Base):
    """Resources Page objects and methods for the OnDemand Admin application."""

    URL_PATH: str = f'{Base.URL_PATH}/resources'
    ROOT_LOCATOR: Selector = Selectors.data_id('resources-page-container')

    @property
    def sidebar(self):
        return Tabs(
            self,
            tabs=[tab for tab in Admin.RESOURCES_TABS],
            selector='sidebar-navigation-container',
        )
