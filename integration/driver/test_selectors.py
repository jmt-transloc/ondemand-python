from typing import Generator

import pytest
from pytest import fixture
from utilities.driver_helpers.selectors import Selector, Selectors


@pytest.fixture
def test_var() -> Generator[str, None, None]:
    """Generate a string for testing Selectors."""
    var: str = 'testing'

    yield var


@pytest.mark.driver
@pytest.mark.unit
class TestSelector:
    """Battery of tests for Selector functionality."""

    @pytest.mark.low
    def test_type(self, test_var: fixture) -> None:
        """Check for whether the date type returned is a tuple.

        Type checking is removed on 'selector' to ensure that there is no confusion with what
        is being checked by this test.
        """
        selector = Selectors.data_id(test_var)

        assert type(selector) is tuple


@pytest.mark.driver
@pytest.mark.unit
class TestSelectors:
    """Battery of tests for Selectors functionality."""

    @pytest.mark.low
    def test_selectors_require_input(self) -> None:
        """Check that selectors require an input."""
        with pytest.raises(TypeError):
            assert Selectors.name()  # type: ignore

    @pytest.mark.low
    def test__class_name(self, test_var: fixture) -> None:
        """Check the output of a class name Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.class_name(test_var)

        assert selector == ('css selector', f'.{test_var}')

    @pytest.mark.low
    def test__css_selector(self, test_var: fixture) -> None:
        """Check the output of a css selector Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.css_selector(test_var)

        assert selector == ('css selector', test_var)

    @pytest.mark.low
    def test__data_id(self, test_var: fixture) -> None:
        """Check the output of a data id Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.data_id(test_var)

        assert selector == ('css selector', f'[data-id="{test_var}"]')

    @pytest.mark.low
    def test__data_test_id(self, test_var: fixture) -> None:
        """Check the output of a data test id Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.data_test_id(test_var)

        assert selector == ('css selector', f'[data-test-id="{test_var}"]')

    @pytest.mark.low
    def test__element_id(self, test_var: fixture) -> None:
        """Check the output of a element id Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.element_id(test_var)

        assert selector == ('css selector', f'[id="{test_var}"]')

    @pytest.mark.low
    def test__element_type(self, test_var: fixture) -> None:
        """Check the output of a element type Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.element_type(test_var)

        assert selector == ('css selector', f'[type="{test_var}"]')

    @pytest.mark.low
    def test__href(self, test_var: fixture) -> None:
        """Check the output of a href Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.href(test_var)

        assert selector == ('css selector', f'[href="{test_var}"]')

    @pytest.mark.low
    def test__link_text(self, test_var: fixture) -> None:
        """Check the output of a link text Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.link_text(test_var)

        assert selector == ('link text', f'{test_var}')

    @pytest.mark.low
    def test__name(self, test_var: fixture) -> None:
        """Check the output of a name Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.name(test_var)

        assert selector == ('css selector', f'[name="{test_var}"]')

    @pytest.mark.low
    def test__option_text(self, test_var: fixture) -> None:
        """Check the output of an option text Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.option_text(test_var)

        assert selector == ('xpath', f'//option[contains(text(), {test_var})]')

    @pytest.mark.low
    def test__option_value(self, test_var: fixture) -> None:
        """Check the output of an option value Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.option_value(test_var)

        assert selector == ('xpath', f'//option[value="{test_var}"]')

    @pytest.mark.low
    def test__partial_href(self, test_var: fixture) -> None:
        """Check the output of a partial href Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.partial_href(test_var)

        assert selector == ('xpath', f'//a[contains(@href, "{test_var}")]')

    @pytest.mark.low
    def test__partial_link_text(self, test_var: fixture) -> None:
        """Check the output of a partial link text Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.partial_link_text(test_var)

        assert selector == ('partial link text', f'{test_var}')

    @pytest.mark.low
    def test__placeholder(self, test_var: fixture) -> None:
        """Check the output of a placeholder Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.placeholder(test_var)

        assert selector == ('css selector', f'[placeholder="{test_var}"]')

    @pytest.mark.low
    def test__radio(self, test_var: fixture) -> None:
        """Check the output of a radio Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.radio(test_var)

        assert selector == ('css selector', f'[type="radio"][value="{test_var}"]')

    @pytest.mark.low
    def test__role(self, test_var: fixture) -> None:
        """Check the output of a role Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.role(test_var)

        assert selector == ('css selector', f'[role="{test_var}"]')

    @pytest.mark.low
    def test__tag(self, test_var: fixture) -> None:
        """Check the output of a tag Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.tag(test_var)

        assert selector == ('css selector', f'{test_var}')

    @pytest.mark.low
    def test__tag_and_text(self, test_var: fixture) -> None:
        """Check the output of a tag Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.tag_and_text(selector=test_var, text=test_var)

        assert selector == ('xpath', f'//{test_var}[contains(text(), "{test_var}")]')

    @pytest.mark.low
    def test__text(self, test_var: fixture) -> None:
        """Check the output of a text Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.text(test_var)

        assert selector == ('xpath', f'//*[contains(text(), "{test_var}")]')

    @pytest.mark.low
    def test__title(self, test_var: fixture) -> None:
        """Check the output of a title Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.title(test_var)

        assert selector == ('css selector', f'[title="{test_var}"]')

    @pytest.mark.low
    def test__value(self, test_var: fixture) -> None:
        """Check the output of a value Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.value(test_var)

        assert selector == ('css selector', f'[value="{test_var}"]')

    @pytest.mark.low
    def test__xpath(self, test_var: fixture) -> None:
        """Check the output of a xpath Selector.

        :param test_var: A string for testing.
        """
        selector: Selector = Selectors.xpath(test_var)

        assert selector == ('xpath', f'{test_var}')
