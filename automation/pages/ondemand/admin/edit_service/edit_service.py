from pages.ondemand.admin.base.base import Base
from pages.ondemand.admin.edit_service.restricted_groups.group_restrictions_modal import (
    GroupRestrictionsModal,
)
from pages.ondemand.admin.edit_service.restricted_groups.group_restrictions_table import (
    GroupRestrictionsTable,
)
from utilities import Selector, Selectors


class EditService(Base):
    """Objects and methods for the Edit Service page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('service-edit-page-container')

    @property
    def group_restrictions_modal(self) -> GroupRestrictionsModal:
        return GroupRestrictionsModal(self)

    @property
    def group_restrictions_table(self) -> GroupRestrictionsTable:
        return GroupRestrictionsTable(self)
