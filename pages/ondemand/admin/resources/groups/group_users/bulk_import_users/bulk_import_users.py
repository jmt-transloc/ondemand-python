import os

from pages.ondemand.admin.base.base import Base
from utilities import Selector, Selectors, WebElement

from .upload_user_list_modal import UploadUserListModal


class BulkImportUsers(Base):
    """Objects and methods for the Bulk Import Users page."""

    ROOT_LOCATOR: Selector = Selectors.data_id('bulk-import-users-page-container')
    _back_button: Selector = Selectors.data_id('back-button')
    _input_field: Selector = Selectors.element_type('file')
    _upload_list_button: Selector = Selectors.data_id('upload-user-list-button')

    @property
    def back_button(self) -> WebElement:
        return self.driver.find_element(*self._back_button)

    @property
    def input_field(self) -> WebElement:
        return self.driver.find_element(*self._input_field)

    @property
    def upload_list_button(self) -> WebElement:
        return self.driver.find_element(*self._upload_list_button)

    @property
    def upload_user_list_modal(self) -> UploadUserListModal:
        return UploadUserListModal(self)

    def upload_file(self, file_name: str) -> None:
        """Upload a CSV list of test users for bulk import testing.

        :param file_name: The file name for upload.
        """
        _file_path: str = f'{os.getcwd()}/utilities/test_files/{file_name}'

        self.input_field.send_keys(_file_path)
