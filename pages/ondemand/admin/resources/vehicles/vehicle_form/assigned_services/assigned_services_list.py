from typing import List

from pages.ondemand.admin.resources.vehicles.vehicle_form.assigned_services import AssignedService
from selenium.common.exceptions import NoSuchElementException
from utilities import Component, Selector, Selectors


class AssignedServicesList(Component):
    """Objects and methods for the Assigned Services List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('assigned-services-container')

    @property
    def assigned_services(self) -> List[AssignedService]:
        return [
            AssignedService(self.page, item)
            for item in self.container.find_elements(*AssignedService.ROOT_LOCATOR)
        ]

    def filter_services(self, service_id: int) -> AssignedService:
        """Filter all assigned services for a match with a service ID.

        :param service_id: The unique service ID for an assigned service.
        """
        service_list: List[AssignedService] = [
            service for service in self.assigned_services if service.service_id == service_id
        ]

        if not service_list:
            raise NoSuchElementException(
                f'An assigned service matching service ID: {service_id} could not be found.',
            )
        return service_list[0]

    def surface_assigned_service(self, service_id: int) -> AssignedService:
        """Raise an assigned service for later use.

        :param service_id: The unique service ID for a service.
        """
        return self.filter_services(service_id)
