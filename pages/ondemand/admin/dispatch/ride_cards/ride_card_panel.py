from typing import Tuple

from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors


class RideCardPanel(Component):
    """Objects and methods for the ride cards panel."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-card-container')

    @property
    def ride_cards(self) -> Tuple[RideCard, ...]:
        return tuple(
            RideCard(self, element)
            for element in self.container.find_elements(*RideCard.ROOT_LOCATOR)
        )

    def filter_cards(self, ride: dict) -> RideCard:
        """Filter all ride cards for a match with a passenger name.

        :param ride: The ride yielded from a ride fixture.
        """
        rider = ride['rider']
        rider_name = f'{rider["first_name"]} {rider["last_name"]}'

        self.verify_card_created(rider_name)

        card_list: Tuple[RideCard, ...] = tuple(
            card for card in self.ride_cards if card.rider_name == rider_name
        )

        if not card_list:
            raise NoSuchElementException
        return card_list[0]

    def verify_card_created(self, rider_name: str) -> None:
        """Wait until a card is located which contains a specific name.

        An increased wait time is used within this function as cards can take upward of seven
        seconds to appear within the DOM. This amount is nearly doubled when running in parallel.

        :param rider_name: The name of the rider for a Ride object.
        """
        self.container.wait_until_visible(*Selectors.text(rider_name), wait_time=10)

    def surface_ride_card(self, ride: dict) -> RideCard:
        """Validate a ride card, then raise it for later use.

        :param ride: The ride yielded from a ride fixture.
        """
        return self.filter_cards(ride)
