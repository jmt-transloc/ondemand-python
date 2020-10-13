"""Exceptions which may occur within this automation framework."""


class FrameworkException(Exception):
    """Base framework exception."""

    def __init__(self, message: str = None, stacktrace: str = None):
        self.message = message
        self.stacktrace = stacktrace

    def __str__(self):
        exception_message: str = f'Message: {self.message}\n'

        if self.stacktrace is not None:
            stacktrace: str = '\n'.join(self.stacktrace)
            exception_message += f'Stacktrace: {stacktrace}\n'

        return exception_message


class ConfigurationException(FrameworkException):
    """Thrown when a configuration error has occurred.

    If you encounter this exception, check the following:
        * Check for the existence of an .env file
        * Check for whether env variables are used in the command line
            * This would occur when using a different environment from the .env file
    """

    pass


class FilterException(FrameworkException):
    """Thrown when filtering fails due to invalid filter input.

    If you encounter this exception, check the following:
        * Check for whether the filter is valid
        * Check for whether the filter constants are up to date
    """

    pass


class InvalidDayException(FrameworkException):
    """Thrown when an invalid day is passed to a calendar component.

    If you encounter this exception, check the following:
        * Check to see whether the day is valid within the calendar month
        * Check to see whether the day is enabled within the calendar component
    """

    pass


class MultipleElementsException(FrameworkException):
    """Thrown when multiple elements are found by the driver.

    If you encounter this exception, check the following:
        * Check for the existence of multiple elements with the same selector
            * If raised during run time, insert a pdb.set_trace() call to debug in real time
    """

    pass


class NavigationException(FrameworkException):
    """Thrown when navigation fails due to invalid page input.

    If you encounter this exception, check the following:
        * Check for whether the page is valid
        * Check for whether the navigation elements contains the page
        * Check for whether the page is spelled correctly
    """

    pass


class PageObjectUrlException(FrameworkException):
    """Thrown when a Page is missing a URL.

    If you encounter this exception, check the following:
        * Check if a Base URL for the page has been set
        * Check if a URL_PATH attribute for the page has been set
    """

    pass


class PaymentMethodException(FrameworkException):
    """Thrown when an invalid payment method is passed.

    If you encounter this exception, check the following:
        * Check whether the service has fare enabled
        * Check for whether a valid payment method has been passed
    """

    pass


class PrioritizationException(FrameworkException):
    """Thrown when an invalid prioritization type is passed.

    If you encounter this exception, check the following:
        * Check for whether the prioritization type is valid
        * Check for whether the prioritization type matches drop off, entire ride, or pick up
    """

    pass


class RideTypeException(FrameworkException):
    """Thrown when an invalid ride type is passed.

    If you encounter this exception, check the following:
        * Check for whether the service supports Asap, Future, or Recurring rides
        * Check for whether the ride type passed is supported by the service used
    """

    pass


class SearchException(FrameworkException):
    """Thrown when search fails due to invalid search input.

    If you encounter this exception, check the following:
        * Check for whether the input is valid
        * Check for whether the input matches ride name, phone, or email
    """

    pass


class SelectionException(FrameworkException):
    """Thrown when selection fails due to invalid selection input.

    If you encounter this exception, check the following:
        * Check for whether the selection input is valid
        * Check for whether the selection input matches an entry in the selection list
    """

    pass
