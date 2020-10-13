from environs import Env
from utilities.constants.common import URLS


sut_env = Env()
ENV: str = sut_env.str('ENV')


def build_login_url(path: str = '') -> str:
    """Construct a login URL based on environment data.

    :param path: Additional path for a site URL.
    """
    if ENV == 'stage':
        return f'{URLS.LOGIN_STAGE_URL}{path}'
    else:
        return f'{URLS.LOGIN_DEV_URL}{path}'
