from utilities import Component, Selector, Selectors


class ServiceRow(Component):
    """Objects and methods for the Service Row component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('service-list-row')
    _data: Selector = Selectors.data_id('service-data')
    _service_id: Selector = Selectors.data_id('service-id')

    @property
    def data(self) -> str:
        return self.container.find_element(*self._data).text

    @property
    def service_id(self) -> str:
        """Return the unique service ID for a service row.

        The get_attribute method is used instead of .text as the service_id is a hidden attribute.
        """
        return self.container.find_element(*self._service_id).get_attribute('innerText')
