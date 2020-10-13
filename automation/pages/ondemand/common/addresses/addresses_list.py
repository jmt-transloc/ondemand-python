from typing import Tuple, Union

from pages.ondemand.admin.resources.addresses.address_row import AddressRow as AdminAddressRow
from pages.ondemand.web.addresses.address_row import AddressRow as WebAddressRow
from utilities import Component, Selector, Selectors, WebElements


AddressRow = Union[AdminAddressRow, WebAddressRow]


class AddressesList(Component):
    """Objects and methods for the Addresses List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('address-list-container')

    @property
    def address_rows(self) -> Tuple[AddressRow, ...]:
        """Return a tuple of address rows within the list container.

        A conditional check for whether the URL contains 'admin' allows this method to be used in
        both OnDemand Web and OnDemand Admin.
        """
        rows: WebElements

        if 'admin' not in self.driver.current_url:
            rows = self.container.find_elements(*WebAddressRow.ROOT_LOCATOR)

            return tuple(WebAddressRow(self, element) for element in rows)
        rows = self.container.find_elements(*AdminAddressRow.ROOT_LOCATOR)

        return tuple(AdminAddressRow(self, element) for element in rows)

    def filter_rows(self, address: dict, address_label: str = None) -> Union[AddressRow, None]:
        """Filter all address rows for a match with an address label.

        :param address_label: An optional label for an address.
        :param address: An address object yielded from an address fixture.
        """
        name: str = address['name'] if address_label is None else address_label
        address_list: Tuple[AddressRow, ...] = tuple(
            row for row in self.address_rows if name in row.data
        )

        if not address_list:
            return None
        return address_list[0]

    def surface_address_row(self, address: dict, address_label: str = None) -> AddressRow:
        """Raise a address row that matches an address label.

        :param address_label: An optional label for an address.
        :param address: An address object yielded from an address fixture.
        """
        return self.filter_rows(address, address_label=address_label)
