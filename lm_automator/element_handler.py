"""Contains the ElementHandler class."""

from typing import List, Generator, Any
from contextlib import contextmanager
from functools import wraps

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from lm_automator.common import DRIVER


class ElementHandler:
    """Contains various methods for retrieving and interacting with HTML elements on a page.

    Attributes:
        _wait -- a class level WebDriverWait object for use with expected conditions
    """

    _wait = WebDriverWait(DRIVER, 5)

    @classmethod
    def get_element(cls, locator: str) -> WebElement:
        """Pause until element is present then return it.

        Arguments:
            locator -- CSS selector for locating the element
        """
        return cls._wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, locator))
        )

    @classmethod
    def get_all_elements(cls, locator: str) -> List[WebElement]:
        """Pause until all elements are present then return them.

        Arguments:
            locator -- CSS selector for locating the elements
        """
        return cls._wait.until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, locator)
            )
        )

    @classmethod
    def click_element(cls, locator: str) -> None:
        """Pause until element is clickable then click it.

        Arguments:
            locator -- CSS selector for locating the element
        """
        cls._wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, locator))
        ).click()

    @classmethod
    def wait_for_at_least_number_of_elements_to_be_present(
        cls, locator: str, number_of_elements: int
    ) -> None:
        """Pause until x or more number of elements are present on page.

        Arguments:
            locator -- CSS selector for locating the element
            number_of_elements -- a whole number greater than 0
        """
        if number_of_elements <= 0:
            raise ValueError("Please provide a whole number greater than 0.")

        cls._wait.until(
            lambda driver: len(DRIVER.find_elements(By.CSS_SELECTOR, locator))
            >= number_of_elements
        )

    @classmethod
    def wait_for_exact_number_of_elements_to_be_present(
        cls, locator: str, number_of_elements: int
    ) -> None:
        """Pause until exactly x number of elements are present on page.

        Arguments:
            locator -- CSS selector for locating the element
            number_of_elements -- a whole number greater than 0
        """
        if number_of_elements <= 0:
            raise ValueError("Please provide a whole number greater than 0.")

        cls._wait.until(
            lambda driver: len(DRIVER.find_elements(By.CSS_SELECTOR, locator))
            == number_of_elements
        )

    @classmethod
    def wait_for_timeout(cls, *, reason: str) -> None:
        """Pause for the predefined timeout duration.

        Arguments:
            reason -- explanation as to why the wait is being used (generic waits are bad practice)
        """
        try:
            cls.get_element("#i-do-not-exist")
        except TimeoutException:
            pass

    @classmethod
    def wait_for_element_to_disappear(cls, locator: str, *, reason: str) -> None:
        """Pause for the predefined timeout duration.

        Arguments:
            reason -- explanation as to why the wait is being used (generic waits are bad practice)
        """
        cls._wait.until(
            expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, locator)
            )
        )

    @classmethod
    def send_keys_to_element(cls, locator: str, keys: str) -> None:
        """Pause until element is present and send key input to it.

        Arguments:
            locator -- CSS selector for locating the element
            keys -- the key input to send to the element
        """
        element = cls.get_element(locator)
        element.clear()
        element.send_keys(keys)

    @classmethod
    def get_element_as_select(cls, locator: str) -> Select:
        """Pause until element is present then return it as a select object.

        Arguments:
            locator -- CSS selector for locating the element
        """
        return Select(cls.get_element(locator))

    @classmethod
    def get_all_elements_as_selects(cls, locator: str) -> List[Select]:
        """Pause until all elements are present then return them as selects in a list.

        Arguments:
            locator -- CSS selector for locating the element
        """
        return [Select(element) for element in cls.get_all_elements(locator)]

    @classmethod
    def select_value_from_element(cls, locator: str, value: str) -> None:
        """Pause until select element is present then select a value in it.

        Arguments:
            locator -- CSS selector for locating the element
            value -- the option you wish to select
        """
        Select(cls.get_element(locator)).select_by_value(value)

    @classmethod
    def element_is_present(cls, locator: str) -> bool:
        """Return whether an element is present or not.

        Arguments:
            locator -- CSS selector for locating the element
        """
        try:
            cls.get_element(locator)
        except TimeoutException:
            return False
        else:
            return True

    @classmethod
    def element_is_visible(cls, locator: str) -> bool:
        """Return whether an element is visible or not.

        Arguments:
            locator -- CSS selector for locating the element
        """
        try:
            cls._wait.until(expected_conditions.visibility_of(cls.get_element(locator)))
        except TimeoutException:
            return False
        else:
            return True

    @classmethod
    def drag_element_to_element(
        cls, source_element_locator: str, target_element_locator: str
    ) -> None:
        """Drag one element to the location of another.

        Arguments:
            source_element_locator -- CSS selector for locating the first element
            target_element_locator -- CSS selector for locating the second element
        """
        source_element = cls.get_element(source_element_locator)
        target_element = cls.get_element(target_element_locator)
        ActionChains(DRIVER).drag_and_drop(source_element, target_element).perform()

    @classmethod
    def drag_element_by_offset(
        cls, element_locator: str, x_offset: int, y_offset: int
    ) -> None:
        """Drag element by a given x and/or y offset.

        Arguments:
            x_offset -- distance to drag element in x direction
            y_offset -- distance to drag element in y direction
        """
        element = cls.get_element(element_locator)
        ActionChains(DRIVER).drag_and_drop_by_offset(
            element, x_offset, y_offset
        ).perform()

    @classmethod
    @contextmanager
    def enter_frame(cls, locator: str) -> Generator:
        """Switch to iframe, yield context, and return to default content after context.

        Arguments:
            locator -- CSS selector for locating the element
        """
        cls._wait.until(
            expected_conditions.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, locator)
            )
        )
        yield
        DRIVER.switch_to.default_content()


def wait_after_for_timeout(*, reason: str):
    def concrete_decorator(function):
        @wraps(function)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            function(self, *args, **kwargs)
            ElementHandler.wait_for_timeout(reason=reason)

        return wrapper

    return concrete_decorator


def wait_before_for_timeout(*, reason: str):
    def concrete_decorator(function):
        @wraps(function)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            ElementHandler.wait_for_timeout(reason=reason)
            function(self, *args, **kwargs)

        return wrapper

    return concrete_decorator
