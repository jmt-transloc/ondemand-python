import json

from environs import Env


sut_env = Env()


def authorization() -> str:
    """Build an authorization token for API consumption."""
    auth_cookie: dict = json.loads(sut_env.str('AUTH_TOKEN'))
    token: str = f'Token {auth_cookie["value"]}'

    return token
