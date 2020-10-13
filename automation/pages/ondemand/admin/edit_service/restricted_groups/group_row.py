from utilities import Component, Selector, Selectors, WebElement


class GroupRow(Component):
    """Objects and methods for the Restricted Groups row."""

    ROOT_LOCATOR = Selectors.data_id('group-row')
    _groups_manage_row_name: Selector = Selectors.data_id('group-name')
    _groups_manage_row_allow_checkbox: Selector = Selectors.data_id('allow-group-checkbox')
    _groups_manage_row_deny_checkbox: Selector = Selectors.data_id('deny-group-checkbox')
    _groups_manage_status: Selector = Selectors.data_id('group-status')
    _group_id: Selector = Selectors.data_id('group-id')

    @property
    def group_id(self) -> str:
        """Return the unique service ID for a service row.

        The get_attribute method is used instead of .text as the service_id is a hidden
        attribute.
        """
        return self.container.find_element(*self._group_id).get_attribute('innerText')

    @property
    def name(self) -> str:
        return self.container.find_element(*self._groups_manage_row_name).text

    @property
    def allow_checkbox(self) -> WebElement:
        return self.container.find_element(*self._groups_manage_row_allow_checkbox)

    @property
    def deny_checkbox(self) -> WebElement:
        return self.container.find_element(*self._groups_manage_row_deny_checkbox)

    @property
    def status(self) -> str:
        return self.container.find_element(*self._groups_manage_status).text
