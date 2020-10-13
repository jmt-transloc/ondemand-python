from selenium.webdriver.remote.webelement import WebElement


class ElementTuple(tuple):
    """Tuple of elements returned by using the find_all_by driver method.

    Instances of 'self' refer to the tuple containing Web Elements.
    """

    def __init__(self, list: list) -> None:
        """Create the element tuple."""
        self._container = tuple(list)

    def __getitem__(self, index) -> WebElement:
        """Return an element within the tuple.

        :param index: The index of the Web Element.
        """
        return self._container[index]

    def __getattr__(self, attribute: str) -> str:
        """Return an attribute within the tuple.

        :param attribute: The attribute to be located.
        """
        try:
            return getattr(self.first, attribute)
        except AttributeError:
            try:
                return getattr(self._container, attribute)
            except AttributeError:
                raise AttributeError(f'Tuple has no attribute: {attribute}')

    def __len__(self) -> int:
        """Return the length of the container."""
        return len(self._container)

    @property
    def first(self) -> WebElement:
        """Return the first element within the tuple.

        :usage example:
            results = self.driver.find_all_by('css selector', '[data-id="ride-card"]')
            results.first
        """
        return self[0]

    @property
    def last(self) -> WebElement:
        """Return the last element within the tuple.

        :usage example:
            results = self.driver.find_all_by('css selector', '[data-id="ride-card"]')
            results.last
        """
        return self[-1]

    def is_empty(self) -> bool:
        """Check whether the tuple is empty or not.

        :usage example:
            results = self.driver.find_all_by('css selector', '[data-id="ride-card"]')
            results.is_empty
        """
        return len(self) == 0
