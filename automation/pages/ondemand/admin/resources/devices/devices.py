from pages.ondemand.admin.resources.resources import Resources
from utilities import Selector, Selectors


class Devices(Resources):
    """Objects and methods for the Devices page.

    The devices page may be accessed by selecting the 'Devices' tab from the side navigation
    panel on the 'Resources' page.
    """

    URL_PATH: str = f'{Resources.URL_PATH}/devices'
    ROOT_LOCATOR: Selector = Selectors.data_id('content-container')
