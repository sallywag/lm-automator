"""Contains an abstract base class for HTML elements to subclass."""

from abc import ABCMeta, abstractmethod


class Widget(metaclass=ABCMeta):
    """Abstract base class for HTML elements.

    Attributes:
        _locator -- CSS selector for locating the element
    """

    def __init__(self, locator: str):
        """
        Arguments:
            locator -- CSS selector for locating the element
        """
        self._locator = locator

    @property
    @abstractmethod
    def locator(self) -> str:
        """Abstract property to ensure child classes have locators."""
        return self._locator
