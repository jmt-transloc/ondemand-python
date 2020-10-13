from utilities import Component, Selector, Selectors
from utilities.exceptions import NavigationException


class Tabs(Component):
    """Objects and methods for the OnDemand applications Tabs container.

    The Tabs component may be used for navigating or selecting a tab within both OnDemand
    applications. An example would be the sidebar tab container on the OnDemand Admin Rides page,
    the sidebar navigation tabs container on the OnDemand Web application, or the header navigation
    tabs container on the OnDemand Admin application.

    :example usage:
        def navigation(self) -> Tabs:
            return Tabs(self,
                        tabs=['Rides', 'Services', 'Reports'],
                        selector='header-navigation-container'
                        )
    """

    def __init__(self, page: object, selector: str, tabs: list):
        self.tabs = tabs
        self.ROOT_LOCATOR: Selector = Selectors.data_id(selector)
        super().__init__(page)

    def select_tab(self, tab: str) -> None:
        """Navigate to a specific tab within an OnDemand application.

        :param tab: The specified tab.
        """
        _groomed_tab: str = tab.lower().replace(' ', '-')

        if tab not in self.tabs:
            raise NavigationException
        self.container.find_element(*Selectors.data_id(f'tab-{_groomed_tab}')).click()
