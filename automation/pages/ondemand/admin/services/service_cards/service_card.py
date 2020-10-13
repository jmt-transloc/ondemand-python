from pages.ondemand.admin.services.service_cards.archive_modal import ArchiveModal
from utilities import Component, Selector, Selectors, WebElement


class ServiceCard(Component):
    """Objects and methods for an individual Service Card."""

    ROOT_LOCATOR: Selector = Selectors.data_id('service-card')
    card_locator: Selector = Selectors.data_id('service-card')
    _archive_button: Selector = Selectors.data_id('service-archive')
    _edit_button: Selector = Selectors.data_id('service-edit')
    _service_dates: Selector = Selectors.data_id('service-dates')
    _service_id: Selector = Selectors.data_id('service-id')
    _service_name: Selector = Selectors.data_id('service-name')
    _service_schedule: Selector = Selectors.data_id('service-schedule')

    @property
    def archive_button(self) -> WebElement:
        return self.container.find_element(*self._archive_button)

    @property
    def archive_modal(self) -> ArchiveModal:
        return ArchiveModal(self)

    @property
    def edit_button(self) -> WebElement:
        return self.container.find_element(*self._edit_button)

    @property
    def service_dates(self) -> WebElement:
        return self.container.find_element(*self._service_dates)

    @property
    def service_id(self) -> str:
        """Return the unique service ID for a service card.

        The get_attribute method is used instead of .text as the service_id is a hidden attribute.
        """
        return self.container.find_element(*self._service_id).get_attribute('innerText')

    @property
    def service_name(self) -> str:
        return self.container.find_element(*self._service_name).text

    @property
    def service_schedule(self) -> WebElement:
        return self.container.find_element(*self._service_schedule)

    def open_archive_modal(self) -> object:
        """Find and open a service card archive modal.

        :returns ArchiveModal: An instance of the service's Archive Modal.
        """
        self.archive_button.click()

        return ArchiveModal(self).wait_for_component_to_be_present()
