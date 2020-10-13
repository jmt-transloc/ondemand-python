import factory
import pytest
from pages.ondemand.admin.resources.groups.group_row import GroupRow
from pages.ondemand.admin.resources.groups.group_users.bulk_import_users.bulk_import_users import (
    BulkImportUsers,
)
from pages.ondemand.admin.resources.groups.group_users.group_user_row import GroupUserRow
from pages.ondemand.admin.resources.groups.group_users.group_users import GroupUsers
from pages.ondemand.admin.resources.groups.groups import Groups
from pytest import fixture
from utilities.api_helpers.groups import GroupsAPI
from utilities.constants.ondemand import Admin
from utilities.factories.fake import fake


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestGroups:
    """Battery of tests for Groups page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.groups: Groups = Groups(selenium)
        self.group_users: GroupUsers = GroupUsers(selenium)
        self.bulk_import_users: BulkImportUsers = BulkImportUsers(selenium)
        self.API: GroupsAPI = GroupsAPI()

    @pytest.mark.medium
    def test_add_group(self, group_factory: factory) -> None:
        """Input a valid group, then check for a success state."""
        group: dict = group_factory.build()

        self.groups.visit()

        self.groups.add_new_group(group=group)
        row: GroupRow = self.groups.groups_list.surface_group_row(group)

        assert group['name'] == row.name

        group['group_id'] = row.group_id
        self.API.delete_group(group)

    @pytest.mark.medium
    def test_edit_group(self, group: fixture) -> None:
        """Yield a group from the API, edit a field, then check for a success state."""
        self.groups.visit()

        before_name: str = self.groups.groups_list.surface_group_row(group).name
        self.groups.open_edit_group(group=group)

        new_name = fake.sentence(nb_words=2)
        self.groups.edit_group(new_name=new_name)

        after_name: str = self.groups.groups_list.surface_group_row(
            group, group_name=new_name,
        ).name

        assert before_name != after_name

    @pytest.mark.medium
    def test_delete_group__kebab(self, group_factory: factory) -> None:
        """Yield a group from the API, delete the group, then check for a success state."""
        group: dict = group_factory.create()

        self.groups.visit()

        self.groups.delete_group__kebab(group=group)
        row: GroupRow = self.groups.groups_list.surface_group_row(group)

        assert row is None

    @pytest.mark.medium
    def test_delete_group__form(self, group_factory: factory) -> None:
        """Yield a group from the API, delete the group, then check for a success state."""
        group: dict = group_factory.create()

        self.groups.visit()

        before_row: GroupRow = self.groups.groups_list.surface_group_row(group)
        before_row.container.click()

        self.groups.groups_form.wait_for_component_to_be_visible()
        self.groups.delete_group__form()
        self.groups.deletion_modal.confirm_button.click()

        after_row: GroupRow = self.groups.groups_list.surface_group_row(group)

        assert after_row is None

    @pytest.mark.medium
    def test_add_user_to_group(self, group: fixture, user_factory: factory) -> None:
        """Input a valid group, then check for a success state."""
        user: dict = user_factory.create(account_user=True).__dict__

        self.groups.navigate_to_manage_users(group)

        self.group_users.add_user(user=user)
        row: GroupUserRow = self.group_users.group_user_list.surface_user_row(
            user, wait_for_row=True,
        )

        assert user['email'] == row.email

    @pytest.mark.medium
    def test_remove_user_from_group(self, group: fixture, user_factory: factory) -> None:
        """Input a valid group, then check for a success state."""
        user: dict = user_factory.create(account_user=True).__dict__

        # Manually associate the new user with a group
        self.API.add_user_to_group(group, user)

        self.groups.navigate_to_manage_users(group)
        self.group_users.remove_user(user=user)

        not_visible: bool = self.group_users.group_user_list.wait_for_component_to_not_be_visible()

        assert not_visible is True

    @pytest.mark.medium
    def test_search_user__not_in_group(self, group: fixture, user_factory: factory) -> None:
        """Search for a user by email.

        When searching by email, the API responds with the user that matches, regardless of group
        affiliation. This test ensures that functionality is present when a user does not belong to
        the current group.
        """
        user: dict = user_factory.create(account_user=True).__dict__

        self.groups.navigate_to_manage_users(group)
        row: GroupUserRow = self.group_users.find_user(user=user)

        assert row is not None
        assert row.add_button is not None
        assert row.remove_button is None

    @pytest.mark.medium
    def test_find_user__in_group(self, group: fixture, user_factory: factory) -> None:
        """Search for a user in a group by email.

        When searching by email, the API responds with the user that matches, regardless of group
        affiliation. This test ensures that functionality is present when a user does belong to the
        current group.
        """
        user: dict = user_factory.create(account_user=True).__dict__

        self.groups.navigate_to_manage_users(group)

        # Add a user to the group
        self.group_users.add_user(user=user)

        # Search for the user in the group.
        row: GroupUserRow = self.group_users.find_user(user=user)
        assert row is not None
        assert row.add_button is None
        assert row.remove_button is not None

    @pytest.mark.medium
    def test_bulk_user_import__success(self, group: fixture) -> None:
        """Bulk import users to a group, then check for a success state.

        The assertion message may be refactored once test users are added to the DB.

        :param group: A group yielded by the Groups API.
        """
        self.groups.navigate_to_manage_users(group)

        self.group_users.navigate_to_bulk_import()
        self.bulk_import_users.upload_file('users.csv')
        self.bulk_import_users.upload_user_list_modal.wait_for_component_to_be_visible()

        self.bulk_import_users.upload_user_list_modal.container.wait_until_text_not_visible(
            'Upload in Progress', wait_time=4,
        )

        message: str = self.bulk_import_users.upload_user_list_modal.message

        assert 'Added 1 new user to the group' in message

    @pytest.mark.medium
    def test_bulk_user_import__failure__invalid_file(self, group: fixture) -> None:
        """Attempt to upload a .txt file, then check for a failure state.

        :param group: A group yielded by the Groups API.
        """
        self.groups.navigate_to_manage_users(group)

        self.group_users.navigate_to_bulk_import()
        self.bulk_import_users.upload_file('testing.txt')

        assert self.bulk_import_users.upload_user_list_modal.visible is False

    @pytest.mark.medium
    def test_bulk_user_import__failure__invalid_users(self, group: fixture) -> None:
        """Attempt to upload a list of invalid users, then check for a failure state.

        :param group: A group yielded by the Groups API.
        """
        self.groups.navigate_to_manage_users(group)

        self.group_users.navigate_to_bulk_import()
        self.bulk_import_users.upload_file('non_users.csv')
        self.bulk_import_users.upload_user_list_modal.wait_for_component_to_be_visible()

        self.bulk_import_users.upload_user_list_modal.container.wait_until_text_not_visible(
            'Upload in Progress', wait_time=4,
        )

        message: str = self.bulk_import_users.upload_user_list_modal.message

        assert Admin.UPLOAD_NON_USER_MESSAGE in message
