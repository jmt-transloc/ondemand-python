import pytest
from factory import Factory
from pages.ondemand.admin.services.services import Services
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestServiceArchive:
    """Battery of tests for service archive functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in service archive testing.

        :param selenium: An instance of Selenium webdriver.
        """
        self.services = Services(selenium)

    @pytest.mark.medium
    @pytest.mark.smoke
    def test_archive_expired_service(self, service_factory: Factory) -> None:
        """Archive an expired service, then check for a success state.

        :param service_factory: A factory for building services via the API.
        """
        expired_service = service_factory.create(expired_service=True)

        self.services.visit()

        card = self.services.service_card_list.surface_service_card(expired_service)
        card.open_archive_modal()

        assert (
            card.archive_modal.confirm_service_archive() is True
            and self.services.service_card_list.card_archived(expired_service) is True
        )

    @pytest.mark.high
    def test_current_services_cannot_be_archived(self, service: fixture) -> None:
        """Attempt to archive a current service, then check for a failure state.

        :param service: A service built with the service API.
        """
        self.services.visit()
        card = self.services.service_card_list.surface_service_card(service)

        card.open_archive_modal()

        assert self.services.service_card_list.card_archived(service) is False

    @pytest.mark.medium
    def test_service_exceptions_prevent_archive(self, service_with_add_exception: fixture) -> None:
        """Attempt to archive a service with a service exception, then check for a failure state.

        :param service_with_add_exception: A service with exception built with the service API.
        """
        self.services.visit()
        card = self.services.service_card_list.surface_service_card(service_with_add_exception)

        card.open_archive_modal()

        assert self.services.service_card_list.card_archived(service_with_add_exception) is False

    @pytest.mark.medium
    def test_ride_data_prevents_archive(self, ride_factory: Factory, service: fixture) -> None:
        """Attempt to archive a service with ride data, then check for a failure state.

        :param ride_factory: RideFactory for creating ride objects.
        :param service: A service built with the service API.
        """
        _: dict = ride_factory.create(service=service)

        self.services.visit()
        card = self.services.service_card_list.surface_service_card(service)

        card.open_archive_modal()

        assert self.services.service_card_list.card_archived(service) is False
