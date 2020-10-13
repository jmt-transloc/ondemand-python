from typing import List, Union

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def _element_if_visible(element: WebElement, visibility: bool = True) -> Union[bool, WebElement]:
    """Check whether an element is visible, then return the element if True.

    :param element: An instance of a Web Element.
    :param visibility: Boolean for whether the element is visible or not.
    """
    try:
        return element if element.is_displayed() == visibility else False
    except AttributeError:
        return False


def _find_element(
    driver: Union[WebDriver, WebElement], by: tuple, wait_time: int = None,
) -> WebElement:
    """Find an element using a specific strategy and locator.

    :param driver: An instance of a Web Driver or Web Element.
    :param by: A tuple containing by and value for the element to be found.
    :param wait_time: The amount of time before a TimeoutException occurs.
    """
    try:
        return driver.find_element(*by, wait_time)
    except NoSuchElementException as element_error:
        raise element_error
    except WebDriverException as driver_error:
        raise driver_error


def _find_elements(
    driver: Union[WebDriver, WebElement], by: tuple, wait_time: int = None,
) -> List[WebElement]:
    """Find all elements using a specific strategy and locator.

    :param driver: An instance of a Web Driver or Web Element.
    :param by: A tuple containing by and value for the element to be found.
    :param wait_time: The amount of time before a TimeoutException occurs.
    """
    try:
        return driver.find_elements(*by, wait_time)
    except WebDriverException as driver_error:
        raise driver_error


class Conditions:
    """Modified expected conditions which are useful within Web Driver tests."""

    class ElementToBeClickable(object):
        """Check that an element is visible and in a clickable state.

        :param locator: A tuple containing by and value for the element.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> Union[bool, WebElement]:
            element: WebElement = _find_element(driver, self.locator, self.wait_time)

            if element and element.is_enabled():
                return element
            else:
                return False

    class ElementToBeSelected(object):
        """Check that an element is present and in a selected state.

        :param locator: A tuple containing by and value for the element.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> bool:
            return _find_element(driver, self.locator, self.wait_time).is_selected()

    class PresenceOfAllElementsLocated(object):
        """Check that all elements are present within the DOM.

        :param locator: A tuple containing by and value for the elements.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> List[WebElement]:
            return _find_elements(driver, self.locator, self.wait_time)

    class PresenceOfElementLocated(object):
        """Check that an element is present within the DOM.

        :param locator: A tuple containing by and value for the element.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> WebElement:
            return _find_element(driver, self.locator, self.wait_time)

    class TextPresentInElement(object):
        """Check whether a text string is present within an element.

        :param locator: A tuple containing by and value for the element.
        :param text_: An expected text string within the element.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, text_: str, wait_time: int = None) -> None:
            self.locator = locator
            self.text = text_
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> Union[bool, str]:
            try:
                element_text: str = _find_element(driver, self.locator, self.wait_time).text
                element_value: str = _find_element(
                    driver, self.locator, self.wait_time,
                ).get_attribute('value')

                return self.text in element_text or element_value
            except StaleElementReferenceException:
                return False

    class TitleContains(object):
        """Check whether the title of the page contains a fragment of an expected title.

        :param title: The fragment of an expected page title.
        """

        def __init__(self, title: str) -> None:
            self.title = title

        def __call__(self, driver: Union[WebDriver, WebElement]) -> bool:
            return self.title in driver.title

    class TitleIs(object):
        """Check whether the title of the page matches an expected title.

        :param title: The expected title of the page.
        """

        def __init__(self, title: str) -> None:
            self.title = title

        def __call__(self, driver: Union[WebDriver, WebElement]) -> bool:
            return self.title == driver.title

    class VisibilityOfAllElementsLocated(object):
        """Check that all elements are both present within the DOM and displayed.

        :param locator: A tuple containing by and value for the elements.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> Union[bool, List[WebElement]]:
            try:
                elements: List[WebElement] = _find_elements(driver, self.locator, self.wait_time)

                if not elements:
                    return False

                for element in elements:
                    if _element_if_visible(element, visibility=False):
                        return False
                return elements
            except StaleElementReferenceException:
                return False

    class VisibilityOfElementLocated(object):
        """Check that an element is both present within the DOM and displayed.

        :param locator: A tuple containing by and value for the element.
        :param wait_time: The amount of time before a TimeoutException occurs.
        """

        def __init__(self, locator: tuple, wait_time: int = None) -> None:
            self.locator = locator
            self.wait_time = wait_time

        def __call__(self, driver: Union[WebDriver, WebElement]) -> Union[bool, WebElement]:
            try:
                return _element_if_visible(_find_element(driver, self.locator, self.wait_time))
            except StaleElementReferenceException:
                return False

    class UrlContains(object):
        """Check whether the current URL contains a string fragment of an expected URL.

        :param url: A string fragment of the expected URL.
        """

        def __init__(self, url: str) -> None:
            self.url = url

        def __call__(self, driver: Union[WebDriver, WebElement]) -> bool:
            return self.url in driver.current_url
