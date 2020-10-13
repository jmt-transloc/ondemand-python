from utilities import Component, Selector, Selectors, WebElement


class GroupUserRow(Component):
    """Group Row component objects and methods for the Group Page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('rider-row')
    _rider_fname: Selector = Selectors.data_id('first-name')
    _rider_lname: Selector = Selectors.data_id('last-name')
    _rider_email: Selector = Selectors.data_id('email')
    _add_button: Selector = Selectors.data_id('Add-item')
    _remove_button: Selector = Selectors.data_id('Remove-item')

    @property
    def first_name(self) -> str:
        return self.container.find_element(*self._rider_fname).text

    @property
    def last_name(self) -> str:
        return self.container.find_element(*self._rider_lname).text

    @property
    def email(self) -> str:
        return self.container.find_element(*self._rider_email).text

    @property
    def add_button(self) -> WebElement:
        return self.container.find_element(*self._add_button)

    @property
    def remove_button(self) -> WebElement:
        return self.container.find_element(*self._remove_button)
