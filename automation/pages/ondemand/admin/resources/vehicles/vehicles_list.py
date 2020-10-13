from typing import Tuple, Union

from pages.ondemand.admin.resources.vehicles.vehicle_row import VehicleRow
from utilities import Component, Selector, Selectors


class VehiclesList(Component):
    """Objects and methods for the Vehicles List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('vehicle-list-container')

    @property
    def vehicle_rows(self) -> Tuple[VehicleRow, ...]:
        return tuple(
            VehicleRow(self.page, element)
            for element in self.container.find_elements(*VehicleRow.ROOT_LOCATOR)
        )

    def filter_rows(self, vehicle: dict) -> Union[VehicleRow, None]:
        """Filter all vehicle rows for a match with a vehicle call name.

        :param vehicle: A vehicle object yielded from a vehicle fixture.
        """
        call_name: str = vehicle['call_name']
        row_list: Tuple[VehicleRow, ...] = tuple(
            row for row in self.vehicle_rows if row.vehicle_call_name == call_name
        )

        if not row_list:
            return None
        return row_list[0]

    def surface_vehicle_row(self, vehicle: dict) -> VehicleRow:
        """Raise a vehicle row for later use.

        :param vehicle: A vehicle object yielded from a vehicle fixture.
        """
        return self.filter_rows(vehicle)
