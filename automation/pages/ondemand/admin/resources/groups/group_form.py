from utilities import Component, Selector, Selectors, WebElement


class GroupForm(Component):
    """Objects and methods for the Group Form component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('group-container')
    _cancel_button: Selector = Selectors.data_id('cancel-button')
    _delete_button: Selector = Selectors.data_id('delete-group-button')
    _name_field: Selector = Selectors.name('name')
    _save_button: Selector = Selectors.data_id('save-group-button')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def delete_group_button(self) -> WebElement:
        return self.container.find_element(*self._delete_button)

    @property
    def name_field(self) -> WebElement:
        return self.container.find_element(*self._name_field)

    @property
    def save_button(self) -> WebElement:
        return self.container.find_element(*self._save_button)

    def fill_form(self, name: str) -> None:
        """Fill out a group form, then submit the form.

        :param name: The name of the group.
        """
        self.name_field.fill(name)
