from pages.ondemand.admin.base.base import Base
from pages.ondemand.common.navigation_tabs.tabs import Tabs
from utilities import Selector, Selectors, WebElement
from utilities.constants.ondemand import Admin


class Reports(Base):
    """Reports Page objects and methods for the OnDemand Admin application."""

    URL_PATH = f'{Base.URL_PATH}/reports'
    ROOT_LOCATOR: Selector = Selectors.data_id('reports-page-container')
    CHARTS = [chart for chart in Admin.REPORTS_CHARTS]

    @property
    def sidebar(self) -> Tabs:
        return Tabs(self, tabs=self.CHARTS, selector='sidebar-navigation-container')

    def is_chart_displayed(self, chart: str) -> bool:
        """Boolean check for whether a specific chart is displayed on the Reports page.

        :param chart: The name of a chart on the Reports page.
        """
        groomed_chart: str
        if chart == 'Origins & Destinations':
            groomed_chart = f'chart-ride-{chart.lower().replace(" ", "-")}'
        else:
            groomed_chart = f'chart-{chart.lower().replace(" ", "-")}'
        element: WebElement = self.driver.wait_until_visible(*Selectors.data_id(groomed_chart))

        return element.is_displayed()
