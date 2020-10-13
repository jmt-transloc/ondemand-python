from typing import Tuple, Union

from pages.ondemand.admin.resources.groups.group_users.group_user_row import GroupUserRow
from utilities import Component, Selector, Selectors, WebElements


class GroupUserList(Component):
    """Objects and methods for the Groups List component."""

    ROOT_LOCATOR: Selector = Selectors.data_id('rider-list-container')

    @property
    def user_rows(self) -> Tuple:
        """Return a tuple of rider rows within the list container."""
        rows: WebElements = self.container.find_elements(*GroupUserRow.ROOT_LOCATOR)
        return tuple(GroupUserRow(self, element) for element in rows)

    def filter_rows(
        self, user: dict, user_email: str = None, wait_for_row: bool = False,
    ) -> Union[GroupUserRow, None]:
        """Filter all user rows for a match with a user name.

        :param user_email: An optional email for a user.
        :param user: A user object yielded from a user fixture.
        :param wait_for_row: Optionally wait for a row.
        """
        email: str = user['email'] if user_email is None else user_email

        if wait_for_row:
            self.wait_for_user_row(user=user, user_email=user_email)

        group_list: list = [row for row in self.user_rows if email == row.email]

        if not group_list:
            return None
        return group_list[0]

    def wait_for_user_row(self, user: dict, user_email: str = None) -> None:
        """Wait until a user row is located which contains a specific email.

        An increased wait time is used within this function as rows can take upward of five seconds
        to appear within the DOM. This amount is nearly doubled when running in parallel.

        :param user_email: An optional email for a user.
        :param user: A user object yielded from a user fixture.
        """
        email: str = user['email'] if user_email is None else user_email
        self.driver.wait_until_visible(*Selectors.text(email), wait_time=10)

    def surface_user_row(
        self, user: dict, user_email: str = None, wait_for_row: bool = False,
    ) -> Union[GroupUserRow, None]:
        """Raise a user row that matches a user name.

        :param user_email: An optional email for a user.
        :param user: A user object yielded from a user fixture.
        :param wait_for_row: Optionally wait for a row.
        """
        return self.filter_rows(user=user, user_email=user_email, wait_for_row=wait_for_row)
