import time
from typing import Any, List, Union

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from ..exceptions import MultipleElementsException
from .conditions import Conditions
from .element_tuple import ElementTuple
from .selectors import Selectors


class Element(WebElement):
    """Extension of Selenium Web Element methods and properties for automation testing.

    Instances of 'self' refer to the Web Element while instances of 'parent' refer to the Web
    Driver.
    """

    def __init__(self, parent, id_):
        super().__init__(parent, id_)
        self.WebElement = Element

    def __getitem__(self, attribute: str) -> Any:
        """Return the value of an attribute for a Web Element.

        :param attribute: The specific attribute.
        """
        return self.get_attribute(attribute)

    WebElement.__getitem__ = __getitem__

    @property
    def checked(self) -> bool:
        """Boolean check for if a Web Element is in a selected state.

        Checked is a useful method for check box elements.

        :usage example: driver.find_element(*Selectors.name('wheelchair')).checked
        """
        return self.is_selected()

    WebElement.checked = checked

    @property
    def html(self) -> str:
        """Return the html of a Web Element.

        :usage example: driver.find_element(*Selectors.name('username')).html
        """
        return self.get_attribute('innerHTML')

    WebElement.html = html

    @property
    def outer_html(self) -> str:
        """Return the outer html of a Web Element.

        :usage example: driver.find_element(*Selectors.name('username')).outer_html
        """
        return self.get_attribute('outerHTML')

    WebElement.outer_html = outer_html

    @property
    def value(self) -> str:
        """Return the value attribute of a Web Element.

        :usage example: driver.find_element(*Selectors.name('username')).value
        """
        return self.get_attribute('value')

    WebElement.value = value

    @property
    def visible(self) -> bool:
        """Boolean check for if an element is visible.

        :usage example: driver.find_element(*Selectors.name('username')).visible
        """
        return self.is_displayed()

    WebElement.visible = visible

    def check(self) -> None:
        """If in a non-checked state, check the Web Element.

        Check is a useful method for check box elements.

        :usage example: driver.find_element(*Selectors.name('wheelchair')).check()
        """
        if not self.checked:
            self.click()

    WebElement.check = check

    def contains(self, text: str) -> bool:
        """Boolean check for whether an element contains a specific string of text.

        :usage example: driver.find_element(*Selectors.name('username')).contains('demodavid')

        :param text: The specific string of text.
        """
        if text in self.text or self.value:
            return True
        else:
            return False

    WebElement.contains = contains

    def double_click(self) -> None:
        """Double-click on the element.

        :usage example: driver.find_element(*Selectors.name('username').double_click()
        """
        self.scroll_to()
        ActionChains(self.parent).double_click(self).perform()

    WebElement.double_click = double_click

    def fill(self, input_text: Union[str, int]) -> None:
        """Fill the value for a Web Element.

        Fill is a useful method for form and input elements.

        :usage example: driver.find_element(*Selectors.name('username')).fill('demodavid')

        :param input_text: The input text for the element.
        """
        self.set_value(input_text)

    WebElement.fill = fill

    def fill_picker_input(self, input_text: Union[str, int]) -> None:
        """Fill the value for a Material UI Pickers Keyboard Date or Time Picker.

        A value of int 1 is passed prior to filling as we use a Moment parser alongside the Material
        UI Pickers library. Since Moment cannot parse strings, we pass an int and then clear out the
        input field. This allows for normal text entry with a string.

        :usage example: driver.find_element(*Selectors.name('date')).fill_picker_input('05-22-2020')

        :param input_text: The input text for the picker element.
        """
        self.fill(1)
        self.fill(input_text)

    WebElement.fill_picker_input = fill_picker_input

    def find_dropdown(self, by: str, value: str) -> Select:
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

    WebElement.find_dropdown = find_dropdown

    def finder(self, by: str, value: str, wait_time: int = None) -> List['Element']:
        """Finder method used in overriding Selenium find_element and find_elements methods.

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        element_list: List[Element] = []
        wait: int = wait_time if wait_time is not None else self.parent.wait_time
        end_time: float = time.time() + wait

        if wait == 0:
            element_list = (
                self._execute(Command.FIND_CHILD_ELEMENTS, {'using': by, 'value': value})['value']
                or []
            )
        else:
            while time.time() < end_time:
                element_list = (
                    self._execute(Command.FIND_CHILD_ELEMENTS, {'using': by, 'value': value})[
                        'value'
                    ]
                    or []
                )

                if element_list:
                    break
        return element_list

    WebElement.finder = finder

    def find_by(self, by: str, value: str, wait_time: int = None) -> Union['Element', None]:
        """Find a child element using a specific strategy and locator.

        This method overrides the builtin find_element method. Calling find_element will use the
        find_by method rather than the builtin. This method returns the element when properly found,
        and False when an element cannot be located. If multiple elements are found, this method
        will return an exception detailing this.

        :usage example: self.container.find_element(*Selectors.name('username'))

        This method may also be used in assertions to determine visibility of an element. The
        following example displays this functionality:

        :usage example: assert self.container.find_element(*Selectors.name('username')) is False

        :param by: The selector strategy (by) for the child element.
        :param value: The unique locator value for the child element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else self.parent.wait_time
        element_list: List[Element] = self.finder(by, value, wait_time=wait)

        if len(element_list) > 1:
            raise MultipleElementsException(
                f'Multiple elements found for: "{by}", "{value}". Use the find_elements method or '
                f'a more specific strategy and locator.',
            )
        elif element_list:
            return element_list[0]
        else:
            return None

    WebElement.find_element = find_by

    def find_all_by(self, by: str, value: str, wait_time: int = None) -> Union[ElementTuple, None]:
        """Find all child elements using a specific strategy and locator.

        This method overrides the builtin find_elements method. Calling find_elements will use the
        find_by_all method rather than the builtin. This method returns the elements when properly
        found, and False when elements cannot be located.

        :usage example:
            results = self.container.find_elements(*Selectors.data_id('ride-card'))
            results.find_elements(*Selectors.data_id('ride-card-kebab-menu')

        This method may also be used in assertions to determine visibility of the elements. The
        following example displays this functionality:

        :usage example:
            results = self.container.find_elements(*Selectors.data_id('ride-card'))
            assert results.find_elements(*Selectors.data_id('ride-card-kebab-menu') is False

        :param by: The selector strategy (by) for the child elements.
        :param value: The unique locator value for the child elements.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else self.parent.wait_time
        element_list: List[Element] = self.finder(by, value, wait_time=wait)

        if element_list:
            return ElementTuple(element_list)
        else:
            return None

    WebElement.find_elements = find_all_by

    def get_value(self) -> str:
        """Return either the value attribute or text attribute.

        :usage example: driver.find_element(*Selectors.name('username')).get_value()
        """
        return self.value or self.text

    WebElement.get_value = get_value

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

    WebElement.is_element_present = is_element_present

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

    WebElement.is_element_not_present = is_element_not_present

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

    WebElement.is_element_visible = is_element_visible

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

    WebElement.is_element_not_visible = is_element_not_visible

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

    WebElement.is_text_present = is_text_present

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

    WebElement.is_text_not_present = is_text_not_present

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

    WebElement.is_text_visible = is_text_visible

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

    WebElement.is_text_not_visible = is_text_not_visible

    def mouse_out(self) -> None:
        """Mouse out from the element.

        Mouse out is particularly useful for testing whether a tooltip disappears or not.

        :usage example: driver.find_element(*Selectors.name('username')).mouse_out()
        """
        self.scroll_to()
        ActionChains(self.parent).move_to_element_with_offset(self, -15, -15).click().perform()

    WebElement.mouse_out = mouse_out

    def mouse_over(self) -> 'Element':
        """Move the mouse over the element, then raise the element for further actions.

        :usage example: driver.find_element(*Selectors.name('username')).mouse_over()
        """
        self.scroll_to()
        ActionChains(self.parent).move_to_element(self).perform()
        return self

    WebElement.mouse_over = mouse_over

    def right_click(self) -> None:
        """Right-click on the element.

        :usage example: driver.find_element(*Selectors.name('username').right_click()
        """
        self.scroll_to()
        ActionChains(self.parent).context_click(self).perform()

    WebElement.right_click = right_click

    def set_value(self, value) -> None:
        """Clear the value attribute, then set the attribute to a new value.

        :usage example: driver.find_element(*Selectors.name('username')).set_value('demodavid')

        :param value: The value for the element.
        """
        self.parent.execute_script("arguments[0].value = ''", self)
        self.send_keys(value)

    WebElement.set_value = set_value

    def scroll_to(self) -> 'Element':
        """Scroll to the element, then raise the element for further actions.

        :usage example: driver.find_element(*Selectors.name('username')).scroll_to()
        """
        self.parent.execute_script('arguments[0].scrollIntoView(true);', self)
        return self

    WebElement.scroll_to = scroll_to

    def uncheck(self) -> None:
        """If in a checked state, uncheck the Web Element.

        Uncheck is a useful method for check box elements.

        :usage example: driver.find_element(*Selectors.name('wheelchair')).uncheck()
        """
        if self.checked:
            self.click()

    WebElement.uncheck = uncheck

    def wait_until_all_not_present(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until all elements are not present, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.data_id(
                'ride-card-container')).wait_until_all_not_present(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until_not(
                Conditions.PresenceOfAllElementsLocated((by, value), wait),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_all_not_present = wait_until_all_not_present

    def wait_until_all_present(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[ElementTuple, None]:
        """Wait until all elements are present, then return the elements for further actions.

        :usage example:
            driver.find_element(*Selectors.data_id(
                'ride-card-container')).wait_until_all_present(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until(
                Conditions.PresenceOfAllElementsLocated((by, value), wait),
            )
        except WebDriverException:
            return None

    WebElement.wait_until_all_present = wait_until_all_present

    def wait_until_not_present(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until an element is not present, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.name('username')).wait_until_not_present(
                *Selectors.element_type('submit'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until_not(
                Conditions.PresenceOfElementLocated((by, value), wait),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_not_present = wait_until_not_present

    def wait_until_present(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union['Element', None]:
        """Wait until an element is present, then return the element for further actions.

        :usage example:
            driver.find_element(*Selectors.name('username')).wait_until_present(
                *Selectors.element_type('submit'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until(
                Conditions.PresenceOfElementLocated((by, value), wait),
            )
        except WebDriverException:
            return None

    WebElement.wait_until_present = wait_until_present

    def wait_until_all_not_visible(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until all elements are not visible, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.data_id(
                'ride-card-container')).wait_until_all_not_visible(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until_not(
                Conditions.VisibilityOfAllElementsLocated((by, value), wait),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_all_not_visible = wait_until_all_not_visible

    def wait_until_all_visible(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union[ElementTuple, None]:
        """Wait until all elements are visible, then return the elements for further actions.

        :usage example:
            driver.find_element(*Selectors.data_id(
                'ride-card-container')).wait_until_all_visible(*Selectors.data_id('ride-card'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until(
                Conditions.VisibilityOfAllElementsLocated((by, value), wait),
            )
        except WebDriverException:
            return None

    WebElement.wait_until_all_visible = wait_until_all_visible

    def wait_until_not_visible(self, by: str, value: str, wait_time: int = None) -> bool:
        """Wait until an element is not visible, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.name('username')).wait_until_not_visible(
                *Selectors.element_type('submit'))

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until_not(
                Conditions.VisibilityOfElementLocated((by, value), wait),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_not_visible = wait_until_not_visible

    def wait_until_text_not_visible(self, text: str, wait_time: int = None) -> bool:
        """Wait until a text string is not visible, then return a boolean value.

        :usage example:
            driver.find_element(*Selectors.data_id(
                    'ride-card-container')).wait_until_text_not_visible('Joe Schmo')

        :param text: The specific text string.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until_not(
                Conditions.VisibilityOfElementLocated(
                    (Selectors.text(text)[0], Selectors.text(text)[1]), wait,
                ),
            )
        except WebDriverException:
            return False

    WebElement.wait_until_text_not_visible = wait_until_text_not_visible

    def wait_until_text_visible(self, text: str, wait_time: int = None) -> Union['Element', None]:
        """Wait until a text string is visible, then return the element for further actions.

        :usage example:
            driver.find_element(*Selectors.data_id(
                    'ride-card-container')).wait_until_text_visible('Joe Schmo')

        :param text: The specific text string.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until(
                Conditions.VisibilityOfElementLocated(
                    (Selectors.text(text)[0], Selectors.text(text)[1]), wait,
                ),
            )
        except WebDriverException:
            return None

    WebElement.wait_until_text_visible = wait_until_text_visible

    def wait_until_visible(
        self, by: str, value: str, wait_time: int = None,
    ) -> Union['Element', None]:
        """Wait until an element is visible, then return the element for further actions.

        :usage example:
            driver.find_element(*Selectors.name('username')).wait_until_visible(
                *Selectors.element_type('submit')).click()

        :param by: The selector strategy (by) for the element.
        :param value: The unique locator value for the element.
        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        wait: int = wait_time if wait_time is not None else (self.parent.wait_time // 2)

        try:
            return WebDriverWait(self, wait).until(
                Conditions.VisibilityOfElementLocated((by, value), wait),
            )
        except WebDriverException:
            return None

    WebElement.wait_until_visible = wait_until_visible
