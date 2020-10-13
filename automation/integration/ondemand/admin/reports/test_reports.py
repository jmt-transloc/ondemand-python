import pytest
from pages.ondemand.admin.reports.reports import Reports
from pytest import fixture
from utilities.constants.ondemand import Admin


@pytest.mark.ondemand_admin
@pytest.mark.ui
class TestReports:
    """Battery of tests for Reports page functionality."""

    @pytest.fixture(autouse=True)
    def set_pages(self, selenium: fixture) -> None:
        """Instantiate all pages used in Reports page testing."""
        self.reports: Reports = Reports(selenium)

    @pytest.mark.parametrize('chart', [chart for chart in Admin.REPORTS_CHARTS])
    def test_charts_render(self, chart: fixture):
        """Navigate to a chart using the sidebar tab container, then check for a success state.

        Parametrization is used in order to test all chart selection scenarios.

        :param chart: The chart name for selection and validation.
        """
        self.reports.visit()
        self.reports.sidebar.select_tab(tab=chart)

        assert self.reports.is_chart_displayed(chart=chart) is True
