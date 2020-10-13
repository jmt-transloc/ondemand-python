from utilities import Component, Selector, Selectors, WebElement


class KebabMenu(Component):
    """Objects and methods for the Ride Subscription Table Kebab Menu component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-kebab-menu-container')

    _details_button: Selector = Selectors.data_id('subscription-kebab-details-button')
    _cancel_all_button: Selector = Selectors.data_id('subscription-kebab-cancel-all')

    @property
    def details_button(self) -> WebElement:
        return self.container.find_element(*self._details_button)

    @property
    def cancel_all_button(self) -> WebElement:
        return self.container.find_element(*self._cancel_all_button)
