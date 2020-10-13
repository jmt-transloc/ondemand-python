from typing import Tuple

from selenium.webdriver.common.by import By


Selector = Tuple[str, str]


class Selectors(object):
    """Library of commonly used selector objects for Selenium Web Driver."""

    @staticmethod
    def class_name(selector: str) -> Selector:
        """Return a Selector for an element based on a class name attribute.

        :param selector: The class name attribute of the element.
        """
        return By.CSS_SELECTOR, f'.{selector}'

    @staticmethod
    def css_selector(selector: str) -> Selector:
        """Return a Selector for an element based on a CSS attribute.

        :param selector: The CSS attribute of the element.
        """
        return By.CSS_SELECTOR, f'{selector}'

    @staticmethod
    def data_id(selector: str) -> Selector:
        """Return a Selector for an element based on a data-id attribute.

        :param selector: The data-id attribute of the element.
        """
        return By.CSS_SELECTOR, f'[data-id="{selector}"]'

    @staticmethod
    def data_test_id(selector: str) -> Selector:
        """Return a Selector for an element based on a data-test-id attribute.

        :param selector: The data-test-id attribute of the element.
        """
        return By.CSS_SELECTOR, f'[data-test-id="{selector}"]'

    @staticmethod
    def element_id(selector: str) -> Selector:
        """Return a Selector for an element based on an id attribute.

        :param selector: The id attribute of the element.
        """
        return By.CSS_SELECTOR, f'[id="{selector}"]'

    @staticmethod
    def element_type(selector: str) -> Selector:
        """Return a Selector for an element based on a type attribute.

        :param selector: The type attribute of the element.
        """
        return By.CSS_SELECTOR, f'[type="{selector}"]'

    @staticmethod
    def href(selector: str) -> Selector:
        """Return a Selector for an element based on an href attribute.

        :param selector: The href attribute of the element.
        """
        return By.CSS_SELECTOR, f'[href="{selector}"]'

    @staticmethod
    def link_text(selector: str) -> Selector:
        """Return a Selector for an element based on the element's link text.

        :param selector: The link text for the element.
        """
        return By.LINK_TEXT, f'{selector}'

    @staticmethod
    def name(selector: str) -> Selector:
        """Return a Selector for an element based on a name attribute.

        :param selector: The name attribute of the element.
        """
        return By.CSS_SELECTOR, f'[name="{selector}"]'

    @staticmethod
    def option_text(selector: str) -> Selector:
        """Return a Selector for an option element based on a text string.

        :param selector: The innerText of an option element.
        """
        return By.XPATH, f'//option[contains(text(), {selector})]'

    @staticmethod
    def option_value(selector: str) -> Selector:
        """Return a Selector for an option element based on a value attribute.

        :param selector: The value attribute of an option element.
        """
        return By.XPATH, f'//option[value="{selector}"]'

    @staticmethod
    def partial_href(selector: str) -> Selector:
        """Return a Selector for an element based on a portion of the element's href attribute.

        :param selector: A portion of the href attribute for the element.
        """
        return By.XPATH, f'//a[contains(@href, "{selector}")]'

    @staticmethod
    def partial_link_text(selector: str) -> Selector:
        """Return a Selector for an element based on a portion of the element's link text.

        :param selector: A portion of the link text for the element.
        """
        return By.PARTIAL_LINK_TEXT, f'{selector}'

    @staticmethod
    def placeholder(selector: str) -> Selector:
        """Return a Selector for an element based on a placeholder attribute.

        :param selector: The placeholder attribute of the element.
        """
        return By.CSS_SELECTOR, f'[placeholder="{selector}"]'

    @staticmethod
    def radio(selector: str) -> Selector:
        """Return a Selector for a radio element based on a value attribute.

        :param selector: The value attribute of the element.
        """
        return By.CSS_SELECTOR, f'[type="radio"][value="{selector}"]'

    @staticmethod
    def role(selector: str) -> Selector:
        """Return a Selector for an element based on a role attribute.

        :param selector: The role attribute of the element.
        """
        return By.CSS_SELECTOR, f'[role="{selector}"]'

    @staticmethod
    def tag(selector: str) -> Selector:
        """Return a Selector for an element based on a tag type.

        :param selector: The tag attribute of the element.
        """
        return By.CSS_SELECTOR, f'{selector}'

    @staticmethod
    def tag_and_text(selector: str, text: str) -> Selector:
        """Return a Selector for an element based on a tag type and inner text.

        :param selector: The tag attribute of the element.
        :param text: The inner text of the element.
        """
        return By.XPATH, f'//{selector}[contains(text(), "{text}")]'

    @staticmethod
    def text(text: str) -> Selector:
        """Return a Selector for an element based on inner text.

        :param text: The inner text of the element.
        """
        return By.XPATH, f'//*[contains(text(), "{text}")]'

    @staticmethod
    def title(selector: str) -> Selector:
        """Return a Selector for an element based on a title attribute.

        :param selector: The title attribute of the element.
        """
        return By.CSS_SELECTOR, f'[title="{selector}"]'

    @staticmethod
    def value(selector: str) -> Selector:
        """Return a Selector for an element based on a value attribute.

        :param selector: The value attribute of the element.
        """
        return By.CSS_SELECTOR, f'[value="{selector}"]'

    @staticmethod
    def xpath(selector: str) -> Selector:
        """Return a Selector for an element based on an xpath locator.

        :param selector: The xpath locator of the element.
        """
        return By.XPATH, f'{selector}'
