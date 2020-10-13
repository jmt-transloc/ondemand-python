import os

import pytest
from environs import Env
from utilities.api_helpers.api import API


sut_env = Env()
AGENCY: str = sut_env.str('AGENCY')


@pytest.mark.api
@pytest.mark.unit
class TestApiHelper:
    """Battery of tests for API helper functionality."""

    @pytest.fixture(autouse=True)
    def set_api(self) -> None:
        """Instantiate all APIs for API helper testing."""
        self.api: API = API()

    @pytest.mark.low
    def test_build_api_url__localhost(self) -> None:
        """Check that the build_api_url handles localhost environments."""
        os.environ['ENV'] = 'localhost'
        url: str = self.api.build_api_url(path='/testing')

        assert 'localhost' in url

    @pytest.mark.low
    def test_build_api_url__stage(self) -> None:
        """Check that the build_api_url handles stage environments."""
        os.environ['ENV'] = 'stage'
        url: str = self.api.build_api_url(path='/testing')

        assert 'stage' in url

    @pytest.mark.low
    def test_build_api_url__dev(self) -> None:
        """Check that the build_api_url handles dev environments."""
        os.environ['ENV'] = 'dev'
        url: str = self.api.build_api_url(path='/testing')

        assert 'dev' in url

    @pytest.mark.low
    def test_build_auth_headers(self) -> None:
        """Check that the build_auth_headers method handles an auth token."""
        os.environ['AUTH_TOKEN'] = '{"value": "token"}'
        auth_token: dict = self.api.build_auth_headers()

        assert 'Token token' in auth_token['Authorization']
