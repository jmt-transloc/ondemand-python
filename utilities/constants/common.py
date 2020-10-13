from environs import Env


sut_env = Env()

API_PASSWORD: str = sut_env.str('DEFAULT_API_PASSWORD')


class MESSAGES:
    """Message constants for Atlas applications."""

    class AUTH:
        """Message constants for Atlas authentication."""

        INCOMPLETE_EMAIL: str = 'Invalid email address.'
        NO_EMAIL: str = 'Field must be between 1 and 254 characters long.'
        PASSWORD_MIN_LENGTH: str = 'Field must be between 8 and 128 characters long.'
        PASSWORD_MISMATCH: str = 'Passwords must match.'
        PHONE_MIN_LENGTH: str = 'Field must be between 10 and 32 characters long.'
        PHONE_VALIDATION: str = 'Please enter a valid phone number.'
        USER_NOT_FOUND: str = 'User with that email not found.'
        USERNAME_MIN_LENGTH: str = 'Field must be between 4 and 32 characters long.'


class URLS:
    """URL constants for Atlas applications."""

    LOGIN_DEV_URL: str = 'https://login.legacy.dev.transloc.com'
    LOGIN_STAGE_URL: str = 'https://login.stage.transloc.com'


class USERS:
    """User constants for Atlas applications."""

    class Admin:
        """User with Admin role and permissions."""

        EMAIL: str = 'automation+qa_admin_001@transloc.com'
        PASSWORD: str = sut_env.str('ADMIN_PASSWORD')
        USERNAME: str = sut_env.str('ADMIN_USERNAME')

    class Agent:
        """User with Agent role and permissions."""

        EMAIL: str = 'automation+qa_agent_001@transloc.com'
        PASSWORD: str = sut_env.str('AGENT_PASSWORD')
        USERNAME: str = sut_env.str('AGENT_USERNAME')

    class Dispatcher:
        """User with Dispatcher role and permissions."""

        EMAIL: str = 'automation+qa_dispatcher_001@transloc.com'
        PASSWORD: str = sut_env.str('DISPATCHER_PASSWORD')
        USERNAME: str = sut_env.str('DISPATCHER_USERNAME')

    class Driver:
        """User with Driver role and permissions."""

        EMAIL: str = 'automation+qa_driver_001@transloc.com'
        PASSWORD: str = sut_env.str('DRIVER_PASSWORD')
        USERNAME: str = sut_env.str('DRIVER_USERNAME')

    class Rider:
        """User with Rider role and permissions."""

        EMAIL: str = 'automation+qa_rider_001@transloc.com'
        PASSWORD: str = sut_env.str('RIDER_PASSWORD')
        USERNAME: str = sut_env.str('RIDER_USERNAME')

    class Superuser:
        """User with Superuser permissions."""

        EMAIL: str = 'automation+qa_user_001@transloc.com'
        PASSWORD: str = sut_env.str('SUPERUSER_PASSWORD')
        USERNAME: str = sut_env.str('SUPERUSER_USERNAME')
