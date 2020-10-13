import time
from typing import List, Union

from environs import Env
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from utilities.driver_helpers.conditions import Conditions
from utilities.driver_helpers.element import Element
from utilities.driver_helpers.element_tuple import ElementTuple
from utilities.driver_helpers.selectors import Selectors
from utilities.exceptions import MultipleElementsException


sut_env = Env()
sut_env.read_env()


def wait() -> int:
    """Set a wait time based on whether the browser is headed or not.

    Headless runs require a longer wait time in order to compensate for running in parallel.
    """
    _wait = 6
    if sut_env.bool('HEADLESS') is True:
        _wait *= 4
    return _wait


class Driver(WebDriver):
    """Extension of Selenium Web Driver methods for automation testing.

    Instances of 'self' refer to the the Web Driver.
    """

    wait_time: int = wait()

    WebDriver.wait_time = wait_time

    def __init__(self):
        super().__init__()
        self.WebDriver = Driver

    def choose(self, value, value_attr) -> None:
        """Select a radio button based on parent input name and the radio button value attribute.

        :usage example: driver.choose('days-of-the-week', 'sunday')

        :param value: The unique locator value for the element.
        :param value_attr: The contents of the value attribute for an input field.
        """
        input_fields: Union[List, ElementTuple] = self.find_elements(*Selectors.name(value))
        input_list: list = [field for field in input_fields if field.value == value_attr]

        if not input_list:
            raise NoSuchElementException
        input_list[0].click()

    WebDriver.choose = choose

    def fill(self, value: str, input_text: Union[str, int]) -> None:
        """Fill out an input element with a value.

        :usage example: driver.fill('username', 'demodavid')

        :param value: The unique locator value for the element.
        :param input_text: The input text for the element.
        """
        input_field: Union[WebElement, Element] = self.find_element(*Selectors.name(value))

        self.execute_script("arguments[0].value = ''", input_field)
        input_field.send_keys(input_text)

    WebDriver.fill = fill

    def fill_picker_input(self, value: str, input_text: Union[str, int]) -> None:
        """Fill the value for a Material UI Pickers Keyboard Date or Time Picker.

        A value of int 1 is passed prior to filling as we use a Moment parser alongside the Material
        UI Pickers library. Since Moment cannot parse strings, we pass an int and then clear out the
        input field. This allows for normal text entry with a string.

        :usage example: driver.fill_picker_input('date', '05-22-2020')

        :param value: The unique locator value for the element.
        :param input_text: The input text for the element.
        """
        input_field: Union[WebElement, Element] = self.find_element(*Selectors.name(value))

        self.execute_script("arguments[0].value = ' '", input_field)
        input_field.send_keys(1)
        self.execute_script("arguments[0].value = ' '", input_field)
        input_field.send_keys(input_text)

    WebDriver.fill_picker_input = fill_picker_input

    def find_dropdown(self, by, value) -> Select:
        """Find a select element using a specific strategy and locator.

        Select elements are most commonly used as dropdown menus. The find_dropdown method should
        be used for all dropdown elements within a page. In addition, Selenium natively supports
        Select elements with various method calls which can be chained on to the finder method. For
        more information on Selenium's support for Select elements, visit:

        https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/support/select.py

        :usage example: driver.find_dropdown(*Selectors.name('serviceId'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        return Select(self.find_element(by, value))

    WebDriver.find_dropdown = find_dropdown

    def finder(self, by: str, value: str, wait_time: int = None) -> List[Element]:
        """Finder method used in overriding Selenium find_element and find_elements methods.

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        element_list: List[Element] = []
        _wait: int = wait_time if wait_time is not None else self.wait_time
        end_time: float = time.time() + _wait

        if _wait == 0:
            element_list = (
                self.execute(Command.FIND_ELEMENTS, {'using': by, 'value': value})['value'] or []
            )
        else:
            while time.time() < end_time:
                element_list = (
                    self.execute(Command.FIND_ELEMENTS, {'using': by, 'value': value})['value']
                    or []
                )

                if element_list:
                    break
        return element_list

    WebDriver.finder = finder

    def find_by(self, by: str, value: str, wait_time: int = None) -> Union[Element, None]:
        """Find an element using a specific strategy and locator.

        This method overrides the builtin find_element method. Calling find_element will use the
        find_by method rather than the builtin. This method returns the element when properly found,
        and False when an element cannot be located. If multiple elements are found, this method
        will return an exception detailing this.

        :usage example: driver.find_element(*Selectors.name('username'))

        This method may also be used in assertions to determine visibility of an element. The
        following example displays this functionality:

        :usage example: assert driver.find_element(*Selectors.name('username')) is False

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else self.wait_time
        element_list: List = self.finder(by, value, _wait)

        if len(element_list) > 1:
            raise MultipleElementsException(
                f'Multiple elements found for: "{by}", "{value}". Use the find_elements method or '
                f'a more specific strategy and locator.',
            )
        elif element_list:
            return element_list[0]
        else:
            return None

    WebDriver.find_element = find_by

    def find_all_by(self, by: str, value: str, wait_time: int = None) -> Union[ElementTuple, None]:
        """Find all elements using a specific strategy and locator.

        This method overrides the builtin find_elements method. Calling find_elements will use the
        find_by_all method rather than the builtin. This method returns the elements when properly
        found, and False when elements cannot be located.

        :usage example: driver.find_elements(*Selectors.data_id('ride-card'))

        This method may also be used in assertions to determine visibility of the elements. The
        following example displays this functionality:

        :usage example: assert driver.find_elements(*Selectors.name('username')) is False

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else self.wait_time
        element_list: List = self.finder(by, value, _wait)

        if element_list:
            return ElementTuple(element_list)
        else:
            return None

    WebDriver.find_elements = find_all_by

    def is_checkbox_checked(self, by: str, value: str) -> bool:
        """Boolean check for if a checkbox is selected.

        :usage example: driver.is_checkbox_checked(*self._username_field)

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            (self.find_element(by, value) and self.find_element(by, value).is_selected())
            return True
        except NoSuchElementException:
            return False

    WebDriver.is_checkbox_checked = is_checkbox_checked

    def is_checkbox_not_checked(self, by: str, value: str) -> bool:
        """Boolean check for if a checkbox is not selected.

        :usage example: driver.is_checkbox_not_checked(*self._username_field)

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            (self.find_element(by, value) and self.find_element(by, value).is_selected())
            return False
        except NoSuchElementException:
            return False

    WebDriver.is_checkbox_not_checked = is_checkbox_not_checked

    def is_element_present(self, by: str, value: str) -> bool:
        """Boolean check for if an element exists.

        :usage example: driver.is_element_present(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            self.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    WebDriver.is_element_present = is_element_present

    def is_element_not_present(self, by: str, value: str) -> bool:
        """Boolean check for if an element does not exist.

        :usage example: driver.is_element_not_present(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            self.find_element(by, value)
            return False
        except NoSuchElementException:
            return True

    WebDriver.is_element_not_present = is_element_not_present

    def is_element_visible(self, by: str, value: str) -> bool:
        """Boolean check for if an element exists and is visible.

        :usage example: driver.is_element_visible(*Selectors.name('username))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            (self.find_element(by, value) and self.find_element(by, value).is_displayed())
            return True
        except NoSuchElementException:
            return False

    WebDriver.is_element_visible = is_element_visible

    def is_element_not_visible(self, by: str, value: str) -> bool:
        """Boolean check for if an element does not exist and is not visible.

        :usage example: driver.is_element_not_visible(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        try:
            (self.find_element(by, value) and self.find_element(by, value).is_displayed())
            return False
        except NoSuchElementException:
            return True

    WebDriver.is_element_not_visible = is_element_not_visible

    def is_text_present(self, text: str) -> bool:
        """Boolean check for if a node with specific text exists.

        :usage example: driver.is_text_present('Forgot password?')

        :param text: The specific text within a node.
        """
        try:
            self.find_element(*Selectors.text(text))
            return True
        except NoSuchElementException:
            return False
        except ValueError:
            return False

    WebDriver.is_text_present = is_text_present

    def is_text_not_present(self, text: str) -> bool:
        """Boolean check for if a node with specific text does not exist.

        :usage example: driver.is_text_not_present('Forgot password?')

        :param text: The specific text within a node.
        """
        try:
            self.find_element(*Selectors.text(text))
            return False
        except NoSuchElementException:
            return True
        except ValueError:
            return True

    WebDriver.is_text_not_present = is_text_not_present

    def is_text_visible(self, text: str) -> bool:
        """Boolean check for if a node with specific text exists and is visible.

        :usage example: driver.is_text_visible('Forgot password?')

        :param text: The specific text within a node.
        """
        try:
            (
                self.find_element(*Selectors.text(text))
                and self.find_element(*Selectors.text(text)).is_displayed()
            )
            return True
        except NoSuchElementException:
            return False
        except ValueError:
            return False

    WebDriver.is_text_visible = is_text_visible

    def is_text_not_visible(self, text: str) -> bool:
        """Boolean check for if a node with specific text does not exist and is not visible.

        :usage example: driver.is_text_not_visible('Forgot password?')

        :param text: The specific text within a node.
        """
        try:
            (
                self.find_element(*Selectors.text(text))
                and self.find_element(*Selectors.text(text)).is_displayed()
            )
            return False
        except NoSuchElementException:
            return True
        except ValueError:
            return True

    WebDriver.is_text_not_visible = is_text_not_visible

    def mouse_over_element(self, by: str, value: str) -> Element:
        """Move the mouse over a specific element, then raise the element for further actions.

        :usage example: driver.mouse_over(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        element: Element = self.find_element(by, value)

        self.scroll_to_element(by, value)
        ActionChains(self).move_to_element(element).perform()
        return element

    WebDriver.mouse_over_element = mouse_over_element

    def scroll_to_element(self, by: str, value: str) -> Element:
        """Scroll to a specific element, then raise the element for further actions.

        :usage example: driver.scroll_to_element(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        """
        element: Element = self.find_element(by, value)

        self.execute_script('arguments[0].scrollIntoView(true);', element)
        return element

    WebDriver.scroll_to_element = scroll_to_element

    def wait_until_all_not_present(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until all elements are not present, then return a boolean value.

        :usage example: driver.wait_until_all_not_present(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until_not(
                Conditions.PresenceOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return False

    WebDriver.wait_until_all_not_present = wait_until_all_not_present

    def wait_until_all_present(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[ElementTuple, None]:
        """Wait until all elements are present, then return the elements for further actions.

        :usage example: driver.wait_until_all_present(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until(
                Conditions.PresenceOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return None

    WebDriver.wait_until_all_present = wait_until_all_present

    def wait_until_not_present(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until an element is not present, then return a boolean value.

        :usage example: driver.wait_until_not_present(*Selectors.name('username'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until_not(
                Conditions.PresenceOfElementLocated((by, value), _wait),
            )
        except WebDriverException:
            return False

    WebDriver.wait_until_not_present = wait_until_not_present

    def wait_until_present(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[Element, None]:
        """Wait until an element is present, then return the element for further actions.

        :usage example: driver.wait_until_present(*Selectors.element_type('submit')).click()

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until(
                Conditions.PresenceOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return None

    WebDriver.wait_until_present = wait_until_present

    def wait_until_url_contains(self, url: str, wait_time: int = None) -> bool:
        """Wait until the Web Driver URL contains a specific portion of a URL.

        :usage example: driver.wait_until_url_contains('/admin/imperialdemo/dispatch')

        :param url: A portion of the intended URL.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        return bool(WebDriverWait(self, _wait).until(Conditions.UrlContains(url)))

    WebDriver.wait_until_url_contains = wait_until_url_contains

    def wait_until_all_not_visible(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until all elements are not visible, then return a boolean value.

        :usage example: driver.wait_until_all_not_visible(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until_not(
                Conditions.VisibilityOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return False

    WebDriver.wait_until_all_not_visible = wait_until_all_not_visible

    def wait_until_all_visible(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[ElementTuple, None]:
        """Wait until all elements are visible, then return the elements for further actions.

        :usage example: driver.wait_until_all_visible(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until(
                Conditions.VisibilityOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return None

    WebDriver.wait_until_all_visible = wait_until_all_visible

    def wait_until_not_visible(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until an element is not visible, then return a boolean value.

        :usage example: driver.wait_until_not_visible(*Selectors.element_type('submit'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until_not(
                Conditions.VisibilityOfAllElementsLocated((by, value), _wait),
            )
        except WebDriverException:
            return False

    WebDriver.wait_until_not_visible = wait_until_not_visible

    def wait_until_text_not_visible(self, text: str, wait_time: int = None) -> bool:
        """Wait until a text string is not visible, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.data_id(
                    'ride-card-container')).wait_until_text_not_visible('Joe Schmo')

        :param text: The specific text string.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until_not(
                Conditions.VisibilityOfElementLocated(
                    (Selectors.text(text)[0], Selectors.text(text)[1]), _wait,
                ),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_text_not_visible = wait_until_text_not_visible

    def wait_until_text_visible(self, text: str, wait_time: int = None) -> Union[Element, None]:
        """Wait until a text string is visible, then return the element for further actions.

        :usage example:
            driver.wait_until_text_visible('Joe Schmo')

        :param text: The specific text string.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until(
                Conditions.VisibilityOfElementLocated(
                    (Selectors.text(text)[0], Selectors.text(text)[1]), _wait,
                ),
            )
        except WebDriverException:
            return None

    WebDriver.wait_until_text_visible = wait_until_text_visible

    def wait_until_visible(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[Element, None]:
        """Wait until an element is visible, then return the element for further actions.

        :usage example: driver.wait_until_visible(*Selectors.element_type('submit')).click()

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        _wait: int = wait_time if wait_time is not None else (self.wait_time // 2)

        try:
            return WebDriverWait(self, _wait).until(
                Conditions.VisibilityOfElementLocated((by, value), _wait),
            )
        except WebDriverException:
            return None

    WebDriver.wait_until_visible = wait_until_visible
