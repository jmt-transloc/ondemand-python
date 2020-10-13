from typing import Tuple, Union

from pages.ondemand.admin.rides.recurring_ride_table.subscription_row import SubscriptionRow
from utilities import Component, Selector, Selectors


class RideSubscriptionTable(Component):
    """Objects and methods for the Ride Subscription Table component.

    The Ride Subscription Table component may be found by selecting 'Active', 'Upcoming' or
    'Complete' under 'Recurring Rides' in the Rides page side bar navigation panel. It is only
    located within these spaces and should not be found elsewhere at this time.
    """

    ROOT_LOCATOR: Selector = Selectors.data_id('subscription-table-container')

    @property
    def subscription_rows(self) -> Tuple[SubscriptionRow, ...]:
        return tuple(
            SubscriptionRow(self, element)
            for element in self.container.find_elements(*SubscriptionRow.ROOT_LOCATOR)
        )

    def filter_subscription_rows(self, subscription_id: str) -> Union[SubscriptionRow, None]:
        """Filter all subscription rows for a match with a subscription ID.

        :param subscription_id: A unique subscription ID.
        """
        row_list: Tuple[SubscriptionRow, ...] = tuple(
            row for row in self.subscription_rows if row.id == subscription_id
        )

        if not row_list:
            return None
        return row_list[0]

    def surface_subscription_row(self, subscription_id: str) -> Union[SubscriptionRow, None]:
        """Surface a subscription row.

        :param subscription_id: A unique subscription ID.
        """
        return self.filter_subscription_rows(str(subscription_id))
