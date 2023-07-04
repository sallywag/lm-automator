import pytest

from lm_automator import inputs
from lm_automator.element_handler import ElementHandler


@pytest.mark.usefixtures("visit_test_site")
class TestTextInput:
    @classmethod
    def setup_class(cls):
        cls.text_input = inputs.Text(locator="#region #component #input")

    @staticmethod
    def enter_text():
        ElementHandler.send_keys_to_element("#input", "text")

    @staticmethod
    def get_text():
        return ElementHandler.get_element("#input").get_property("value")

    def test_value_property_returns_text_input_value(self):
        self.enter_text()
        assert self.text_input.value == self.get_text()

    def test_setting_value_property_enters_the_correct_value_in_the_text_input(self):
        self.text_input.value = "hello"
        assert self.get_text() == "hello"

    def test_clear_method_clears_text_input(self):
        ElementHandler.get_element("#input").clear()
        self.enter_text()
        self.text_input.clear()
        assert self.get_text() == ""


@pytest.mark.usefixtures("visit_test_site")
class TestCheckboxInput:
    @classmethod
    def setup_class(cls):
        cls.checkbox_input = inputs.Checkbox(locator="#region #component #checkbox")

    @staticmethod
    def is_selected():
        return ElementHandler.get_element("#checkbox").is_selected()

    def test_checked_property_returns_checkbox_state(self):
        assert self.checkbox_input.value == self.is_selected()

    def test_checkbox_is_checked_when_checked_property_is_true(self):
        self.checkbox_input.value = True
        assert self.is_selected()

    def test_checkbox_is_checked_when_checked_property_is_false(self):
        self.checkbox_input.value = False
        assert not self.is_selected()


@pytest.mark.usefixtures("visit_test_site")
class TestButtonInput:
    @classmethod
    def setup_class(cls):
        cls.button_input = inputs.Button(locator="#region #component #button")

    def test_click_method_makes_text_appears_in_button(self):
        assert ElementHandler.get_element("#button").text == ""
        self.button_input.click()
        assert ElementHandler.get_element("#button").text == "Hello"


@pytest.mark.usefixtures("visit_test_site")
class TestSelectInput:
    @classmethod
    def setup_class(cls):
        cls.select_input = inputs.Select(locator="#region #component #select-3")

    @staticmethod
    def select_option(option):
        ElementHandler.select_value_from_element("#select-3", option)

    def test_option_property_returns_a_string(self):
        assert isinstance(self.select_input.value, str)

    def test_option_property_returns_currently_selected_option(self):
        self.select_option("yellow")
        assert self.select_input.value == "Yellow"

    def test_setting_option_property_selects_the_correct_option(self):
        self.select_input.value = "green"
        assert (
            ElementHandler.get_element_as_select("#select-3").first_selected_option.text
            == "Green"
        )
