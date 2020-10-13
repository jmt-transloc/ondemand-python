from typing import Union

from selenium.common.exceptions import WebDriverException
from utilities.driver_helpers.element import Element
from utilities.driver_helpers.selectors import Selector


class Component(object):
    """A page component.

    Page components are used to abstract specific regions found within a page object.

    :usage example:
        from utilities import Page, Component

        class Login(Page):
            ROOT_LOCATOR: Selector = Selectors.class_name('login-container')
            URL_PATH: str = '/login'

            @property
            def login_form(self) -> LoginForm:
                return LoginForm(self)

            class LoginForm(Component):
                ROOT_LOCATOR: Selector = Selectors.role('form')

                @property
                def username_field(self):
                    return self.driver.find_element(*Selectors.name('username'))

        login_page = Login(selenium)
        login_form = login_page.login_form
        login_page.visit()
        assert login_page.loaded is True

        login_form.username_field.fill('demodavid')
        assert login_form.username_field.contains('demodavid')
    """

    ROOT_LOCATOR: Selector = None

    def __init__(self, page, container=None):
        """Initialize the component.

        :param page: The parent page of the component.
        """
        self._container = container
        self.driver = page.driver
        self.page = page
        self.wait_for_component_to_be_present()

    @property
    def container(self) -> Union[Element, None]:
        """Return the unique locator of the component.

        The container property should be used for finding elements within the Component.

        :usage example:
            def username_field(self):
                return self.container.find_element(*Selectors.name('username'))
        """
        if self._container is None and self.ROOT_LOCATOR is not None:
            try:
                return self.driver.find_element(*self.ROOT_LOCATOR)
            except WebDriverException:
                return None
        return self._container

    @property
    def loaded(self) -> bool:
        """Boolean check for whether the component has loaded successfully.

        wait_until_all_present is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.

        wait_until_present methods are inherently faster than visible as they wait until the
        component is found in the DOM, not in the UI.
        """
        try:
            return bool(self.driver.wait_until_all_present(*self.ROOT_LOCATOR))
        except WebDriverException:
            return False

    @property
    def visible(self) -> bool:
        """Boolean check for whether the component is visible.

        wait_until_all_visible is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.
        """
        try:
            return bool(self.driver.wait_until_all_visible(*self.ROOT_LOCATOR))
        except WebDriverException:
            return False

    def wait_for_component_to_be_present(self, wait_time=None) -> Union[object, None]:
        """Wait for the component to be present, then return the component.

        wait_until_all_present is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.

        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        try:
            self.driver.wait_until_all_present(*self.ROOT_LOCATOR, wait_time=wait_time)
            return self
        except WebDriverException:
            return None

    def wait_for_component_to_not_be_present(self, wait_time=None) -> bool:
        """Wait for the component to not be present, then return a boolean value.

        wait_until_all_not_present is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.

        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        try:
            self.driver.wait_until_all_not_present(*self.ROOT_LOCATOR, wait_time=wait_time)
            return True
        except WebDriverException:
            return False

    def wait_for_component_to_be_visible(self, wait_time=None) -> Union[object, None]:
        """Wait for the component to be visible, then return the component.

        wait_until_all_visible is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.

        An additional sleep is added to combat race conditions. Use this method sparingly due to
        this sleep.

        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        try:
            self.driver.wait_until_all_visible(*self.ROOT_LOCATOR, wait_time=wait_time)
            return self
        except WebDriverException:
            return None

    def wait_for_component_to_not_be_visible(self, wait_time=None) -> bool:
        """Wait for the component to not be visible, then return a boolean value.

        wait_until_all_not_visible is used to compensate for situations in which multiple components
        of the same class are rendered. An example of this may be found on the OnDemand Admin
        Dispatch page where multiple RideCard components can be found within the RideCardPanel
        component.

        An additional sleep is added to combat race conditions. Use this method sparingly due to
        this sleep.

        :param wait_time: The amount of time until a TimeoutException occurs.
        """
        try:
            self.driver.wait_until_all_not_visible(*self.ROOT_LOCATOR, wait_time=wait_time)
            return True
        except WebDriverException:
            return False
