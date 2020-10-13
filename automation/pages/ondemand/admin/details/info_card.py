from pages.ondemand.admin.details.edit_form import EditForm
from utilities import Component, Selector, Selectors, WebElement


class InfoCard(Component):
    """Ride Info Card component objects and methods for the Details Page.

    The Ride Info Card component contains various ride items within a small container that can be
    found on the Details page. Ride editing may be accessed from the Ride Info component.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('details-ride-info-container')
    _ride_edit: Selector = Selectors.data_id('info-ride-edit')
    _ride_time: Selector = Selectors.data_id('info-ride-time')
    _ride_name: Selector = Selectors.data_id('info-ride-full-name')
    _ride_capacity: Selector = Selectors.data_id('info-ride-capacity')
    _ride_wheelchair: Selector = Selectors.data_id('info-ride-wheelchair')
    _ride_phone: Selector = Selectors.data_id('info-ride-phone')
    _ride_username: Selector = Selectors.data_id('info-ride-username')
    _ride_service: Selector = Selectors.data_id('info-ride-service-name')
    _ride_fare: Selector = Selectors.data_id('info-ride-fare')
    _ride_cost: Selector = Selectors.data_id('info-ride-cost')
    _ride_note: Selector = Selectors.data_id('info-ride-note')
    _ride_termination_reason: Selector = Selectors.data_id('info-ride-terminal-reason')

    @property
    def edit_form(self) -> EditForm:
        return EditForm(self)

    @property
    def ride_time(self) -> str:
        return self.container.find_element(*self._ride_time).text

    @property
    def ride_name(self) -> str:
        return self.container.find_element(*self._ride_name).text

    @property
    def ride_capacity(self) -> str:
        return self.container.find_element(*self._ride_capacity).text

    @property
    def ride_wheelchair(self) -> WebElement:
        return self.container.find_element(*self._ride_wheelchair)

    @property
    def ride_phone(self) -> str:
        return self.container.find_element(*self._ride_phone).text

    @property
    def ride_username(self) -> str:
        return self.container.find_element(*self._ride_username).text

    @property
    def ride_service(self) -> str:
        return self.container.find_element(*self._ride_service).text

    @property
    def ride_fare(self) -> str:
        return self.container.find_element(*self._ride_fare).text

    @property
    def ride_cost(self) -> str:
        return self.container.find_element(*self._ride_cost).text

    @property
    def ride_note(self) -> str:
        return self.container.find_element(*self._ride_note).text

    @property
    def ride_termination_reason(self) -> str:
        return self.container.find_element(*self._ride_termination_reason).text

    def open_ride_edit_form(self) -> object:
        """Open the Edit Form component for the ride.

        :returns EditForm: An instance of the ride's Edit Form.
        """
        self.container.find_element(*self._ride_edit).click()

        return EditForm(self).wait_for_component_to_be_present()
