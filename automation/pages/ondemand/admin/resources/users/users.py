from pages.ondemand.admin.resources.resources import Resources
from utilities import Selector, Selectors, WebElement


class Users(Resources):
    """Objects and methods for the Users page.

    The users page may be accessed by selecting the 'Users' tab from the side navigation
    panel on the 'Resources' page.
    """

    URL_PATH: str = f'{Resources.URL_PATH}/users'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
    _fab_button: Selector = Selectors.data_id('new-button')

    @property
    def fab_button(self) -> WebElement:
        return self.driver.find_element(*self._fab_button)
