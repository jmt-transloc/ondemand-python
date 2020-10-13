import pytest
from pages.ondemand.admin.edit_service.edit_service import EditService
from pages.ondemand.admin.edit_service.restricted_groups.group_restrictions_modal import (
    GroupRestrictionsModal,
)
from pages.ondemand.admin.edit_service.restricted_groups.group_restrictions_table import (
    GroupRestrictionsTable,
)
from pages.ondemand.admin.edit_service.restricted_groups.group_row import GroupRow
from pages.ondemand.admin.resources.groups.groups import Groups
from pages.ondemand.admin.services.services import Services
from pytest import fixture


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestGroupRestrictions:
    """Battery of group restrictions tests for the service edit page."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        self.edit_service: EditService = EditService(selenium)
        self.services: Services = Services(selenium)
        self.groups: Groups = Groups(selenium)

    @pytest.mark.low
    def test_groups__manage_groups_function(self, service: fixture) -> None:
        """Ensure that the manage groups link redirects properly.

        :param service: A service yielded from a service fixture.
        """
        self.services.navigate_to_edit_by_service_id(service)
        self.edit_service.group_restrictions_table.wait_for_component_to_be_visible()

        table: GroupRestrictionsTable = self.edit_service.group_restrictions_table
        modal: GroupRestrictionsModal = self.edit_service.group_restrictions_modal

        table.edit_groups_button.click()

        modal.manage_agency_button.click()

        assert self.groups.loaded

    @pytest.mark.high
    @pytest.mark.parametrize('check_type', ['allow', 'deny'])
    @pytest.mark.smoke
    def test_groups__modal_selection(
        self, check_type: fixture, group: fixture, service: fixture,
    ) -> None:
        """Ensure that allow or deny checks may be saved and update Group Restrictions table.

        This test is part of the smoke testing battery. Test failure should result in immediate
        remediation efforts as it is a main feature for the application.

        :param check_type: The type of check being made.
        :param group: A group yielded from a group fixture.
        :param service: A service yielded from a service fixture.
        """
        self.services.navigate_to_edit_by_service_id(service)
        self.edit_service.group_restrictions_table.wait_for_component_to_be_visible()

        table: GroupRestrictionsTable = self.edit_service.group_restrictions_table
        modal: GroupRestrictionsModal = self.edit_service.group_restrictions_modal

        table.edit_groups_button.click()
        modal_row: GroupRow = modal.surface_group_row(group)

        if check_type == 'allow':
            modal_row.allow_checkbox.click()
        elif check_type == 'deny':
            modal_row.deny_checkbox.click()

        modal.save_button.click()

        table_row: GroupRow = table.surface_group_row(group)

        if check_type == 'allow':
            assert table_row.status == 'Allow Only'
        elif check_type == 'deny':
            assert table_row.status == 'Denied Service'

    @pytest.mark.medium
    def test_groups__modal_selection__disable_checkbox(
        self, group: fixture, service: fixture,
    ) -> None:
        """Ensure that checking a selection disables the opposite selection checkbox.

        :param group: A group yielded from a group fixture.
        :param service: A service yielded from a service fixture.
        """
        self.services.navigate_to_edit_by_service_id(service)
        self.edit_service.group_restrictions_table.wait_for_component_to_be_visible()

        table: GroupRestrictionsTable = self.edit_service.group_restrictions_table
        modal: GroupRestrictionsModal = self.edit_service.group_restrictions_modal

        table.edit_groups_button.click()
        modal_row: GroupRow = modal.surface_group_row(group)

        modal_row.allow_checkbox.click()

        assert 'disabled' in modal_row.deny_checkbox.html

    @pytest.mark.low
    @pytest.mark.role_dispatcher
    def test_groups__dispatcher__no_access(self, service: fixture) -> None:
        """Ensure that role Dispatcher cannot edit group restrictions.

        :param service: A service yielded by a service fixture.
        """
        self.services.navigate_to_edit_by_service_id(service)

        self.edit_service.group_restrictions_table.wait_for_component_to_be_visible()

        assert (
            'disabled' in self.edit_service.group_restrictions_table.edit_groups_button.outer_html
        )
