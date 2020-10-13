import pytest
from requests import HTTPError
from utilities.api_helpers.services import ServicesAPI
from utilities.factories.services import ServiceFactory


@pytest.mark.api
class TestServicesAPI:
    """Battery of tests for ServicesAPI helper functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs used in ServicesAPI testing."""
        self.api: ServicesAPI = ServicesAPI()

    @pytest.mark.high
    @pytest.mark.integration
    def test_archive__success(self) -> None:
        """Check that a service may be archived."""
        service_data: dict = ServiceFactory.build(expired_service=True).__dict__
        service = self.api.create_service(service_data)

        try:
            self.api.archive_service(service)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_archive__failure__invalid_input(self) -> None:
        """Check that the archive endpoint fails with invalid input."""
        with pytest.raises(TypeError):
            assert self.api.archive_service(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_archive__failure__service_id_required(self) -> None:
        """Check that the archive endpoint fails with no service id input."""
        with pytest.raises(TypeError):
            assert self.api.archive_service()  # type: ignore

    @pytest.mark.high
    @pytest.mark.integration
    def test_create__success(self):
        """Check that a service may be created."""
        service_data: dict = ServiceFactory.build().__dict__

        try:
            service: dict = self.api.create_service(service_data)
            self.api.delete_service(service)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_create__failure__invalid_input(self) -> None:
        """Check that the create endpoint fails with invalid input."""
        with pytest.raises(HTTPError):
            assert self.api.create_service(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_create__failure__service_data_required(self) -> None:
        """Check that the create endpoint fails with no service data input."""
        with pytest.raises(TypeError):
            assert self.api.create_service()  # type: ignore

    @pytest.mark.high
    @pytest.mark.integration
    def test_delete__success(self) -> None:
        """Check that a service may be deleted."""
        service_data: dict = ServiceFactory.build().__dict__
        service = self.api.create_service(service_data)

        try:
            self.api.delete_service(service)
        except HTTPError:
            pytest.fail('Test failed due to HTTPError.')

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete__failure__invalid_input(self) -> None:
        """Check that the delete endpoint fails with invalid input."""
        with pytest.raises(TypeError):
            assert self.api.delete_service(111111)  # type: ignore

    @pytest.mark.low
    @pytest.mark.unit
    def test_delete__failure__service_id_required(self) -> None:
        """Check that the delete endpoint fails with no service id input."""
        with pytest.raises(TypeError):
            assert self.api.delete_service()  # type: ignore
