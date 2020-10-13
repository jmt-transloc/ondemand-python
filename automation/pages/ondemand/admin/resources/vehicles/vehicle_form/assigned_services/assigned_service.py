from utilities import Component, Selector, Selectors


class AssignedService(Component):
    """Objects and methods for the Assigned Service component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('assigned-service')
    _service_id: Selector = Selectors.data_id('service-id')
    _service_name: Selector = Selectors.data_id('service-name')

    @property
    def service_id(self) -> str:
        """Return the unique service ID for a service row.

        The get_attribute method is used instead of .text as the service_id is a hidden attribute.
        """
        return self.container.find_element(*self._service_id).get_attribute('innerText')

    @property
    def service_name(self) -> str:
        return self.container.find_element(*self._service_name).text
