from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.dispatch.book_a_ride.recurring_rides.ride_subscription_modal import (
    RideSubscriptionModal,
)
from pages.ondemand.admin.dispatch.book_a_ride.ride_booking_panel import RideBookingPanel
from pages.ondemand.admin.dispatch.ride_cards.ride_card import RideCard
from pages.ondemand.admin.dispatch.ride_cards.ride_card_panel import RideCardPanel
from pages.ondemand.admin.dispatch.ride_filters.ride_filters import RideFilters
from pages.ondemand.admin.dispatch.rider_search.rider_search import RiderSearch
from pages.ondemand.common.cancellation_modal.cancellation_modal import CancellationModal
from utilities import Selector, Selectors


class Dispatch(Base):
    """Dispatch Page objects and methods for the OnDemand Admin application."""

    URL_PATH: str = f'{Base.URL_PATH}/dispatch'
    ROOT_LOCATOR: Selector = Selectors.data_id('dispatch-page-container')

    @property
    def cancellation_modal(self) -> CancellationModal:
        return CancellationModal(self)

    @property
    def ride_booking_panel(self) -> RideBookingPanel:
        return RideBookingPanel(self)

    @property
    def ride_card_panel(self) -> RideCardPanel:
        return RideCardPanel(self)

    @property
    def ride_filters(self) -> RideFilters:
        return RideFilters(self)

    @property
    def rider_search(self) -> RiderSearch:
        return RiderSearch(self)

    @property
    def ride_subscription_modal(self) -> RideSubscriptionModal:
        return RideSubscriptionModal(self)

    def cancel_ride(self, cancel_reason: str, ride: dict) -> None:
        """Cancel a ride that matches a ride object.

        :param cancel_reason: The required cancellation reason.
        :param ride: The ride yielded from a ride fixture.
        """
        card: RideCard = self.ride_card_panel.surface_ride_card(ride)
        card.open_kebab_menu()
        card.kebab_menu.cancel_ride_button.click()

        self.cancellation_modal.cancel_ride(cancel_reason)

    def fill_future_ride_form(self, ride: dict) -> None:
        """Fill out the Future Ride form.

        :param ride: The ride yielded from a ride fixture.
        """
        self.ride_booking_panel.future_ride_form.fill_future_ride_form(ride)

    def fill_recurring_ride_form(self, ride: dict) -> None:
        """Fill out the Recurring Ride form.

        :param ride: The ride yielded from a recurring ride fixture.
        """
        self.ride_booking_panel.recurring_ride_form.fill_recurring_ride_form(ride)

    def fill_ride_form(self, service: dict, ride: dict) -> None:
        """Fill out the Dispatch page ride form.

        :param service: The service yielded from a service API fixture.
        :param ride: The ride yielded from a ride fixture.
        """
        self.ride_booking_panel.open_book_a_ride_form()
        self.ride_booking_panel.passenger_form.fill_passenger_info_form(ride)
        self.ride_booking_panel.ride_form.fill_ride_info_form(service, ride)
