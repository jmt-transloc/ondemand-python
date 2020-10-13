from typing import Tuple

from pages.ondemand.web.agency.service_list.service_row import ServiceRow
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors, WebElements


class ServiceList(Component):
    """Objects and methods for the Service List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('service-list')

    @property
    def service_rows(self) -> Tuple[ServiceRow, ...]:
        rows: WebElements = self.container.find_elements(*ServiceRow.ROOT_LOCATOR)

        return tuple(ServiceRow(self, element) for element in rows)

    def filter_rows(self, service_id: str) -> ServiceRow:
        """Filter all service rows for a match with a service ID.

        :param service_id: The unique service ID.
        """
        service_list: Tuple[ServiceRow, ...] = tuple(
            row for row in self.service_rows if row.service_id == service_id
        )

        if not service_list:
            raise NoSuchElementException
        return service_list[0]

    def surface_service_row(self, service_id: str) -> ServiceRow:
        """Raise a service row that matches a service ID.

        :param service_id: The unique service ID.
        """
        return self.filter_rows(service_id)
