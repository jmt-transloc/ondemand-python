from utilities import Component, Selector, Selectors, WebElement


class Header(Component):
    """Objects and methods for the Header container."""

    HELP_LINK: str = 'https://faq.transloc.com/'
    ROOT_LOCATOR: Selector = Selectors.data_id('header-container')
    _agency_drop_down: Selector = Selectors.data_id('agency-dropdown')
    _help_tab: Selector = Selectors.data_id('user-nav-help')
    _logout_tab: Selector = Selectors.data_id('user-nav-logout')
    _profile_tab: Selector = Selectors.data_id('user-nav-profile')

    @property
    def agency_drop_down(self) -> WebElement:
        return self.container.find_element(*self._agency_drop_down)

    @property
    def help_link(self) -> WebElement:
        return self.container.find_element(*self._help_tab)

    @property
    def logout_link(self) -> WebElement:
        return self.container.find_element(*self._logout_tab)

    @property
    def profile_link(self) -> WebElement:
        return self.container.find_element(*self._profile_tab)
