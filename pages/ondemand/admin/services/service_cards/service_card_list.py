from typing import Tuple

from pages.ondemand.admin.services.service_cards.service_card import ServiceCard
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from utilities import Component, Selector, Selectors


class ServiceCardList(Component):
    """Objects and methods for the Service Card list."""

    ROOT_LOCATOR: Selector = Selectors.data_id('service-card-container')

    @property
    def service_cards(self) -> Tuple[ServiceCard, ...]:
        return tuple(
            ServiceCard(self.page, item)
            for item in self.container.find_elements(*ServiceCard.ROOT_LOCATOR)
        )

    def card_archived(self, service: dict) -> bool:
        """Confirm a card has been archived.

        Returns False if the card is still displayed and True if it is no longer within the DOM.
        This method should be used with an assert statement to verify its boolean return.

        :param service: The service intended to be archived.
        """
        try:
            self.surface_service_card(service)
            return False
        except NoSuchElementException:
            return True
        except StaleElementReferenceException:
            return True

    def filter_cards(self, service: dict) -> ServiceCard:
        """Filter all service cards for a match with a service id.

        :param service: The service intended to be raised.
        """
        card_list: Tuple[ServiceCard, ...] = tuple(
            card for card in self.service_cards if card.service_id == service['service_id']
        )

        if not card_list:
            raise NoSuchElementException
        return card_list[0]

    def surface_service_card(self, service: dict) -> ServiceCard:
        """Raise a service card for later use.

        :param service: The service intended to be raised.
        """
        return self.filter_cards(service)
