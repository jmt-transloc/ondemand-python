import base64
import os
from typing import Generator, List

import pytest
from environs import Env
from faker import Faker
from marshmallow.validate import OneOf
from pages import Login
from pytest import fixture
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from utilities.api_helpers.api import API
from utilities.constants.common import USERS
from utilities.exceptions import ConfigurationException


sut_env = Env()
fake = Faker('en_US')

AGENCY: str = sut_env.str('AGENCY', default='imperialdemo')
ENV: str = sut_env.str(
    'ENV',
    default='dev',
    validate=OneOf(
        ['dev', 'localhost', 'stage'],
        error='ENV must be one of the following: {choices}. Please enter a valid choice.',
    ),
)
HEADLESS: bool = sut_env.bool('HEADLESS', default=True)
PORT: int = sut_env.int('PORT', default=8080)
TEAM: str = sut_env.str(
    'TEAM',
    default='mamlambo',
    validate=OneOf(
        ['bloop', 'kraken', 'mamlambo', 'thunderbird'],
        error='TEAM must be one of the following: {choices}. Please enter a valid choice.',
    ),
)


def pytest_selenium_capture_debug(item, extra):
    """Override default screenshot behavior to always take screenshots on failure."""
    for log_type in extra:
        if log_type['name'] == 'Screenshot':
            content = base64.b64decode(log_type['content'].encode('utf-8'))
            with open(f'{os.getcwd()}/output/screenshots/{item.name + ".png"}', 'wb') as f:
                f.write(content)


def build_site_url(app: str, path: str = '') -> str:
    """Construct an application specific URL based on environment data.

    :param app: The application under test.
    :param path: Additional path for a site URL.
    """
    validate_application(app)

    if ENV == 'localhost':
        return f'http://{ENV}.transloc.com:{PORT}{path}'
    elif ENV == 'stage':
        return f'https://{app}.{ENV}.transloc.com{path}'
    else:
        return f'https://{app}.{TEAM}.{ENV}.transloc.com{path}'


@pytest.fixture
def chrome_options(chrome_options: Options) -> Options:
    """Construct and return chrome options to an instance of Google Chrome.

    By default, headed testing is disabled. For headed testing, add 'HEADLESS=False' as an
    environment variable.

    :param chrome_options: Options being distributed to Chrome.
    """
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--window-size=1920,1080')

    chrome_options.headless = False if sut_env.bool('HEADLESS') is False else True
    return chrome_options


@pytest.fixture(autouse=True)
def login(request: fixture, selenium: fixture) -> None:
    """Login via submitting a login form or auth token.

    Runs a check to determine if an auth token exists. If one exists, the framework will add the
    auth token as a cookie. If not, the framework will input valid login credentials, then capture
    the auth token for later tests.

    :param request: Fixture for requesting Pytest configuration data.
    :param selenium: An instance of Selenium Web Driver.
    """
    login_api = API()
    login_page = Login(selenium)

    if 'no_auth' not in request.keywords:

        #
        # Check for specific pytest marks for permissions, then login accordingly
        #
        if 'role_agent' in request.keywords:
            login_api.capture_token(username=USERS.Agent.USERNAME, superuser=False)
        elif 'role_driver' in request.keywords:
            login_api.capture_token(username=USERS.Driver.USERNAME, superuser=False)
        elif 'role_dispatcher' in request.keywords:
            login_api.capture_token(username=USERS.Dispatcher.USERNAME, superuser=False)
        elif 'role_rider' in request.keywords:
            login_api.capture_token(username=USERS.Rider.USERNAME, superuser=False)
        else:
            login_api.capture_token(username=USERS.Admin.USERNAME, superuser=False)

        login_page.visit()
        login_page.add_auth_token()


@pytest.fixture
def selenium(selenium: fixture) -> WebDriver:
    """Override the base Selenium settings.

    :param selenium: Fixture for running an instantiation of Selenium webdriver.
    """
    selenium.delete_all_cookies()
    selenium.maximize_window()
    return selenium


@pytest.fixture(scope='session', autouse=True)
def system_under_test() -> Generator:
    """Create system under test prior to test instantiation."""
    sut_env.read_env()

    yield


def validate_application(app: str) -> None:
    """Check whether an application is supported or not.

    :param app: The specified application.
    """
    supported_applications: List[str] = ['architect', 'ondemand', 'realtime', 'traveler']

    if app not in supported_applications:
        raise ConfigurationException(
            f'The application: "{app}" is not supported.\nPlease specify a valid application.',
        )
    elif app is None:
        raise ConfigurationException('Please specify an application.')
