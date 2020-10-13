from utilities import Component, Selector, Selectors, WebElement


class AgencySelectModal(Component):
    """Objects and methods for the Agency Select Modal component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('agency-select-modal-container')
    _main_menu_link: Selector = Selectors.data_id('modal-main-menu-link')

    @property
    def main_menu_link(self) -> WebElement:
        return self.container.find_element(*self._main_menu_link)

    def select_agency(self, agency_short_name: str) -> None:
        """Select an agency based on its short name property.

        :param agency_short_name: The short name property of the specified agency.
        """
        agency = self.container.find_element(*Selectors.data_id(agency_short_name))
        agency.mouse_over()

        agency.click()
