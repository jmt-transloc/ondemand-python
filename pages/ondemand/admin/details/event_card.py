from utilities import Component, Selector, Selectors, WebElements


class EventCard(Component):
    """Ride Event Card component objects and methods for the Details Page.

    Event Cards feature event data for a ride. Ride Events are 'Ride Requested', 'Ride Cancelled',
    and 'Ride Completed'.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('details-event-card')
    _event_individual_item: Selector = Selectors.data_id('details-event-list-item')
    _event_items: Selector = Selectors.data_id('details-event-items-list')
    _event_timestamp: Selector = Selectors.data_id('details-event-timestamp')
    _event_type: Selector = Selectors.data_id('details-event-type')

    @property
    def event_individual_item(self) -> str:
        """Return the text of an individual event item."""
        return self.container.find_element(*self._event_individual_item).get_attribute('innerText')

    @property
    def event_items(self) -> WebElements:
        """Return a list of all event items within the card."""
        return self.container.find_elements(*self._event_individual_item)

    @property
    def event_timestamp(self) -> str:
        return self.container.find_element(*self._event_timestamp).get_attribute('innerText')

    @property
    def event_type(self) -> str:
        return self.container.find_element(*self._event_type).get_attribute('innerText')

    @property
    def pick_up_address(self) -> str:
        """Return the pick up address for the ride."""
        return self.event_items[2].text

    @property
    def drop_off_address(self) -> str:
        """Return the drop off address for the ride."""
        return self.event_items[3].text
