"""Contains various classes for interacting with HTML input elements on a page."""

from abc import ABCMeta, abstractmethod
from typing import Any

from lm_automator.widget import Widget
from lm_automator.element_handler import ElementHandler


class Input(Widget, metaclass=ABCMeta):
    """Abstract base class for various HTML input types."""

    @property
    def locator(self) -> str:
        return self._locator

    @property # type:ignore
    @abstractmethod
    def value(self) -> Any:
        """Abstract property for retrieving an HTML inputs value."""

    @value.setter # type:ignore
    @abstractmethod
    def value(self, value: Any) -> None:
        """Abstract property for setting an HTML inputs value."""


class Text(Input):
    """Class for interacting with HTML text fields."""

    @property
    def value(self) -> str:
        """Return text in text field."""
        return ElementHandler.get_element(self.locator).get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        """Add text to text field.

        Arguments:
            value -- the text to enter into the text field
        """
        ElementHandler.send_keys_to_element(self.locator, value)

    def clear(self) -> None:
        """Remove all text from text field."""
        ElementHandler.get_element(self.locator).clear()


class Checkbox(Input):
    """Class for interacting with HTML checkboxes."""

    @property
    def value(self) -> bool:
        """Return whether a checkbox is checked off."""
        return ElementHandler.get_element(self.locator).is_selected()

    @value.setter
    def value(self, value: bool) -> None:
        """"Check or uncheck a checkbox.

        Arguments:
            value -- value to determine whether to check or uncheck the checkbox
        """
        if (value is True and not self.value) or (value is False and self.value):
            ElementHandler.click_element(self.locator)


class Button(Input):
    """Class for interacting with HTML buttons."""

    @property
    def value(self) -> None:
        raise NotImplementedError

    @value.setter
    def value(self, value: Any) -> None:
        raise NotImplementedError

    def click(self) -> None:
        """Click an element."""
        ElementHandler.click_element(self.locator)


class Select(Input):
    """Class for interacting with HTML selects."""

    @property
    def value(self) -> str:
        """Return selected option of select."""
        return ElementHandler.get_element_as_select(
            self.locator
        ).first_selected_option.text

    @value.setter
    def value(self, value: str) -> None:
        """Select option of select.

        Arguments:
            value -- the option to select from the select menu
        """
        ElementHandler.select_value_from_element(self.locator, value)
