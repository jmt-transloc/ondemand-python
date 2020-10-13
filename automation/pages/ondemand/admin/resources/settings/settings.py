from pages.ondemand.admin.resources.resources import Resources
from utilities import Selector, Selectors


class Settings(Resources):
    """Objects and methods for the Settings page.

    The settings page may be accessed by selecting the 'Settings' tab from the side navigation
    panel on the 'Resources' page.
    """

    URL_PATH: str = f'{Resources.URL_PATH}/settings'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
