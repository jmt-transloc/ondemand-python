from typing import List

from utilities import Component, Selector, Selectors, WebElement
from utilities.exceptions import PrioritizationException


class RidePrioritizationModal(Component):
    """Ride Prioritization Modal component objects and methods for the Dispatch page.

    The prioritization modal may be accessed by selecting 'Prioritize' from a Ride Card kebab menu.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-prioritization-modal-container')
    _cancel_button: Selector = Selectors.data_id('ride-prioritization-modal-cancel-button')
    _confirm_button: Selector = Selectors.data_id('ride-prioritization-modal-confirm-button')
    _entire_ride_button: Selector = Selectors.data_id(
        'ride-prioritization-modal-entire-ride-button',
    )
    _pick_up_button: Selector = Selectors.data_id('ride-prioritization-modal-pick-up-button')

    @property
    def cancel_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_button)

    @property
    def confirm_button(self) -> WebElement:
        return self.container.find_element(*self._confirm_button)

    @property
    def entire_ride_button(self) -> WebElement:
        return self.container.find_element(*self._entire_ride_button)

    @property
    def pick_up_button(self) -> WebElement:
        return self.container.find_element(*self._pick_up_button)

    def prioritize_ride(self, priority_type: str) -> None:
        """Prioritize a ride based on an input type.

        'Drop off' is skipped due to the fact that the drop off selection does not feature a radio
        button like 'Entire ride' and 'Pick up'. Instead, 'Drop off' is selected by selecting the
        confirm button on the prioritization modal. Logically, when 'Drop off' is passed to this
        method, the confirm button will be selected.

        :param priority_type: The type of prioritization.
        """
        _accepted_types: List[str] = ['drop off', 'entire ride', 'pick up']

        if priority_type not in _accepted_types:
            raise PrioritizationException(f'The prioritization type: {priority_type} is invalid.')

        if priority_type == 'pick up':
            self.pick_up_button.click()
        elif priority_type == 'entire ride':
            self.entire_ride_button.click()
        self.confirm_button.click()

        self.driver.wait_until_not_present(*self.ROOT_LOCATOR)
