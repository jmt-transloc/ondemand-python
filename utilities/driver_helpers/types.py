from typing import List, Union

from selenium.webdriver.remote.webelement import WebElement

from .element import Element
from .element_tuple import ElementTuple


WebElement = Union[Element, WebElement]
WebElements = Union[List[WebElement], ElementTuple]
