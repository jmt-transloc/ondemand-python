from typing import List

from utilities import Component, Selector, Selectors, WebElement


class SubscriptionErrors(Component):
    """Objects and methods for subscription errors."""

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-errors-container')
    _subscription_error: Selector = Selectors.data_id('subscription-error')

    @property
    def subscription_errors(self) -> List[WebElement]:
        return self.container.find_elements(*self._subscription_error)
