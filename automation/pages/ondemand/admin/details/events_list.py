from typing import Tuple

from pages.ondemand.admin.details.event_card import EventCard
from utilities import Component, Selector, Selectors


class EventsList(Component):
    """Ride Events List component objects and methods for the Details Page.

    The Ride Events List component contains ride event data within a container that can be found
    below the Ride Info Card on the Details page.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('details-events-container')
    _event_card: Selector = Selectors.data_id('details-event-card')

    @property
    def event_cards(self) -> Tuple[EventCard, ...]:
        """Return a list of all event cards within the event list container."""
        return tuple(
            EventCard(self.page, item)
            for item in self.container.find_elements(*EventCard.ROOT_LOCATOR)
        )

    @property
    def ride_requested_card(self) -> EventCard:
        """Return the first card within the event list.

        The first card in the event list container should always be the Ride Requested card. This
        card contains ride data such as pick up and drop off locations.
        """
        return self.event_cards[0]
