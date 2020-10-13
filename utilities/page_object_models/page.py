from typing import Union

from selenium.common.exceptions import WebDriverException
from utilities.driver_helpers.selectors import Selector
from utilities.exceptions import PageObjectUrlException


class Page(object):
    """A page object.

    Page objects form the foundation for automation testing by programmatically simulating the
    page being tested.

    :usage example:
        from utilities import Page

        class Login(Page):
            ROOT_LOCATOR: Selector = Selectors.class_name('login-container')
            URL_PATH: str = '/login'

        login_page = Login(selenium)
        login_page.visit()
        assert login_page.loaded is True
    """

    ROOT_LOCATOR: Selector = None
    URL_PATH: str = None

    def __init__(self, driver, base_url=''):
        """Initialize the page.

        :param driver: An instance of Selenium Web Driver.
        :param base_url: The base url of the application.
        """
        self.base_url = base_url
        self.driver = driver

    @property
    def loaded(self) -> bool:
        """Boolean check for whether the page has loaded successfully."""
        if self.ROOT_LOCATOR is None:
            return self.driver.current_url == self.url

        try:
            return bool(self.driver.wait_until_visible(*self.ROOT_LOCATOR))
        except WebDriverException:
            return False

    @property
    def url(self) -> Union[str, None]:
        """Build a URL based on the base url and optional path."""
        url = self.base_url

        if self.URL_PATH is not None:
            url = f'{self.base_url}{self.URL_PATH}'

        if not url:
            return None

        return url

    def wait_for_page_to_load(self, wait_time=None) -> Union[object, None]:
        """Wait for the page to load, then return the page.

        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        if self.ROOT_LOCATOR is None:
            self.driver.wait_until_url_contains(self.url, wait_time=wait_time)
        else:
            try:
                self.driver.wait_until_visible(*self.ROOT_LOCATOR, wait_time=wait_time)
            except WebDriverException:
                return None
        return self

    def visit(self) -> object:
        """Open a page via url."""
        if self.url:
            self.driver.get(self.url)
            self.wait_for_page_to_load()
            return self
        raise PageObjectUrlException(
            'A base URL or URL_PATH must be set in order to visit this page.',
        )
