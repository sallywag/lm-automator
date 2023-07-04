import timeit

import pytest
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, UnexpectedTagNameException
from selenium.webdriver.support.ui import Select

from lm_automator.common import DRIVER
from lm_automator.element_handler import ElementHandler


@pytest.mark.usefixtures("visit_test_site")
class TestElementHandler:
    def test_get_element_method_returns_a_web_element_instance(self):
        element = ElementHandler.get_element(".main-content")
        assert isinstance(element, WebElement)

    def test_get_element_method_returns_element_with_expected_class_name(self):
        element = ElementHandler.get_element(".main-content")
        assert element.get_attribute("class") == "main-content"

    def test_get_element_method_raises_a_timeout_exception_when_element_does_not_exist(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.get_element(".i-do-not-exist")

    def test_get_all_elements_method_returns_a_list(self):
        elements = ElementHandler.get_all_elements("p")
        assert isinstance(elements, list)

    def test_get_all_elements_method_returns_expected_number_of_elements(self):
        elements = ElementHandler.get_all_elements("p")
        assert len(elements) == 3

    def test_get_all_elements_method_returns_a_collection_of_web_elements(self):
        elements = ElementHandler.get_all_elements("p")
        assert all(isinstance(element, WebElement) for element in elements)

    def test_get_all_elements_method_returns_all_elements_with_the_expected_class_name(
        self,
    ):
        elements = ElementHandler.get_all_elements(".p-content")
        assert all(
            element.get_attribute("class") == "p-content" for element in elements
        )

    def test_get_all_elements_method_raises_timeout_exception_when_element_does_not_exist(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.get_all_elements(".i-do-not-exist")

    def test_click_element_method_can_click_enabled_element(self):
        ElementHandler.click_element("#button-1")

    def test_click_element_method_raises_timeout_exception_when_clicking_disabled_element(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.click_element("#button-2")

    def test_click_element_method_raises_timeout_exception_when_clicking_element_that_does_not_exist(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.click_element(".i-do-not-exist")

    def test_wait_for_at_least_number_of_elements_to_be_present_method_raises_vaule_error_when_number_of_elements_is_less_than_0(
        self,
    ):
        with pytest.raises(ValueError):
            ElementHandler.wait_for_at_least_number_of_elements_to_be_present("p", -1)

    def test_wait_for_at_least_number_of_elements_to_be_present_method_raises_vaule_error_when_number_of_elements_is_0(
        self,
    ):
        with pytest.raises(ValueError):
            ElementHandler.wait_for_at_least_number_of_elements_to_be_present("p", 0)

    def test_wait_for_at_least_number_of_elements_to_be_present_method_does_not_raise_timeout_exception_when_number_of_elements_is_less_than_the_amount_of_elements_present_on_page(
        self,
    ):
        ElementHandler.wait_for_at_least_number_of_elements_to_be_present("p", 2)

    def test_wait_for_at_least_number_of_elements_to_be_present_method_does_not_raise_timeout_exception_when_number_of_elements_is_equal_to_the_amount_of_elements_present_on_page(
        self,
    ):
        ElementHandler.wait_for_at_least_number_of_elements_to_be_present("p", 3)

    def test_wait_for_at_least_number_of_elements_to_be_present_method_raises_timeout_exception_when_number_of_elements_is_greater_than_the_amount_of_elements_present_on_page(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.wait_for_at_least_number_of_elements_to_be_present("p", 4)

    def test_wait_for_exact_number_of_elements_to_be_present_method_raises_vaule_error_when_number_of_elements_is_less_than_0(
        self,
    ):
        with pytest.raises(ValueError):
            ElementHandler.wait_for_exact_number_of_elements_to_be_present("p", -1)

    def test_wait_for_exact_number_of_elements_to_be_present_method_raises_vaule_error_when_number_of_elements_is_0(
        self,
    ):
        with pytest.raises(ValueError):
            ElementHandler.wait_for_exact_number_of_elements_to_be_present("p", 0)

    def test_wait_for_exact_number_of_elements_to_be_present_method_raises_timeout_exception_when_number_of_elements_is_less_than_the_amount_of_elements_present(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.wait_for_exact_number_of_elements_to_be_present("p", 2)

    def test_wait_for_exact_number_of_elements_to_be_present_method_does_not_raise_timeout_exception_when_number_of_elements_is_equal_to_the_amount_of_elements_present(
        self,
    ):
        ElementHandler.wait_for_exact_number_of_elements_to_be_present("p", 3)

    def test_wait_for_exact_number_of_elements_to_be_present_method_raises_timeout_exception_when_number_of_elements_is_greater_than_the_amount_of_elements_present(
        self,
    ):
        with pytest.raises(TimeoutException):
            ElementHandler.wait_for_exact_number_of_elements_to_be_present("p", 4)

    def test_send_keys_to_element_method_populates_input_with_expected_text(self):
        ElementHandler.send_keys_to_element("input", "test text")
        assert ElementHandler.get_element("input").get_attribute("value") == "test text"

    def test_get_element_as_select_method_returns_a_select(self):
        assert isinstance(ElementHandler.get_element_as_select("#select-1"), Select)

    def test_get_element_as_select_method_raises_unexpected_tag_name_exception_when_trying_to_get_an_element_that_is_not_a_select(
        self,
    ):
        with pytest.raises(UnexpectedTagNameException):
            ElementHandler.get_element_as_select(".p-content")

    def test_get_all_elements_as_selects_method_returns_a_list(self):
        elements = ElementHandler.get_all_elements_as_selects("select")
        assert isinstance(elements, list)

    def test_get_all_elements_as_selects_method_returns_expected_number_of_elements(
        self,
    ):
        elements = ElementHandler.get_all_elements_as_selects("select")
        assert len(elements) == 3

    def test_get_all_elements_as_selects_method_raises_unexpected_tag_name_exception_when_trying_to_get_elements_that_are_not_selects(
        self,
    ):
        with pytest.raises(UnexpectedTagNameException):
            ElementHandler.get_all_elements_as_selects(".p-content")

    def test_get_all_elements_as_selects_method_returns_a_collection_of_selects(self):
        elements = list(ElementHandler.get_all_elements_as_selects("select"))
        for element in elements:
            assert isinstance(element, Select)

    def test_element_is_present_method_returns_true_when_element_exists(self):
        assert ElementHandler.element_is_present("main.main-content") is True

    def test_element_is_present_method_returns_false_when_element_does_not_exists(self):
        assert ElementHandler.element_is_present("main.test-class") is False

    def test_is_visible_method_returns_true_when_element_is_displayed(self):
        assert ElementHandler.element_is_visible(".header-content") is True

    def test_is_visible_method_returns_false_when_element_is_not_displayed(self):
        assert ElementHandler.element_is_visible("#div-1") is False

    def test_enter_frame_method_brings_you_into_iframe_context_and_removes_you_from_it_after(
        self,
    ):
        assert ElementHandler.get_element("header").text == "Welcome to the site!"
        with ElementHandler.enter_frame("iframe"):
            assert ElementHandler.get_element("header").text == "Welcome to the iframe!"
        assert ElementHandler.get_element("header").text == "Welcome to the site!"

    def test_wait_for_timeout_method_waits_for_the_expected_amount_of_time(self):
        timeout = 5
        start_time = timeit.default_timer()
        ElementHandler.wait_for_timeout(reason="Testing.")
        assert int(timeit.default_timer() - start_time) == timeout

    def test_drag_element_to_element_method_drags_correct_element_to_target_element(
        self,
    ):
        DRIVER.refresh()
        ElementHandler.drag_element_to_element("#draggable", "#drop-zone")
        assert ElementHandler.get_element("#drop-zone").text == "Dropped!"

    def test_drag_element_by_offset_method_drags_correct_element_to_target_element(
        self,
    ):
        DRIVER.refresh()
        ElementHandler.drag_element_by_offset("#draggable", 100, 100)
        assert ElementHandler.get_element("#drop-zone").text == "Dropped!"
