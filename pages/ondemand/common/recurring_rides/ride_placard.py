from utilities import Component, Selector, Selectors, WebElement


class RidePlacard(Component):
    """Objects and methods for the ride placard."""

    ROOT_LOCATOR: Selector = Selectors.data_id('ride-placard-container')
    _ride_driver_note: Selector = Selectors.data_id('ride-placard-note')
    _ride_drop_off: Selector = Selectors.data_id('ride-placard-dropoff')
    _ride_fare_warning: Selector = Selectors.data_id('ride-placard-fare-warning')
    _ride_pick_up: Selector = Selectors.data_id('ride-placard-pickup')
    _rider_name: Selector = Selectors.data_id('ride-placard-name')
    _rider_phone: Selector = Selectors.data_id('ride-placard-phone')

    @property
    def driver_note(self) -> str:
        return self.container.find_element(*self._ride_driver_note).text

    @property
    def drop_off(self) -> str:
        return self.container.find_element(*self._ride_drop_off).text

    @property
    def fare_warning(self) -> WebElement:
        return self.container.find_element(*self._ride_fare_warning)

    @property
    def pick_up(self) -> str:
        return self.container.find_element(*self._ride_pick_up).text

    @property
    def rider_name(self) -> str:
        return self.container.find_element(*self._rider_name).text

    @property
    def rider_phone(self) -> str:
        return self.container.find_element(*self._rider_phone).text
