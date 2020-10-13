from utilities import Component, Selector, Selectors, WebElement


class GroupUserForm(Component):
    """Objects and methods for the Group Form component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('rider-editor-form-container')
    _clear_button: Selector = Selectors.data_id('filter-clear')
    _email_field: Selector = Selectors.name('rider-email')

    @property
    def clear_button(self) -> WebElement:
        return self.container.find_element(*self._clear_button)

    @property
    def email_field(self) -> WebElement:
        return self.container.find_element(*self._email_field)

    def fill_form(self, email: str) -> None:
        """Fill out email field, then submit the form.

        :param name: The email of the user.
        """
        self.email_field.fill(email)
