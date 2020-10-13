from typing import Tuple

from pages.ondemand.admin.services.locations.location_card import LocationCard
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors


class RegionsList(Component):
    """Objects and methods for the Addresses List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('regions-list-container')

    @property
    def location_cards(self) -> Tuple[LocationCard, ...]:
        """Return a list of location cards within the list container."""
        cards = self.container.find_elements(*LocationCard.ROOT_LOCATOR)

        return tuple(LocationCard(self, element) for element in cards)

    def filter_cards(self, address_label: str) -> LocationCard:
        """Filter all location cards for a match with an address label.

        :param address_label: The label for a specific address.
        """
        card_list: Tuple[LocationCard, ...] = tuple(
            card for card in self.location_cards if address_label in card.label
        )

        if not card_list:
            raise NoSuchElementException
        return card_list[0]

    def surface_location_card(self, address_label: str) -> LocationCard:
        """Raise a location card that matches an address label.

        :param address_label: The label for a specific address.
        """
        return self.filter_cards(address_label)
