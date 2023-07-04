from typing import List

from lm_automator.element_handler import ElementHandler, wait_after_for_timeout
from lm_automator.widget import Widget
from lm_automator.inputs import Button


class Region(Widget):

    def __init__(self, locator: str, menu_items):
        super().__init__(locator)
        self.menu = Button(self._locator + " .panel-title .caret")
        self.menu_items = menu_items

    def add_components(self, components: List[str]) -> None:
        """Add components to the region.

        User Flow:
        1. Click the menu to open it.
        2. Click the name of each component you wish to add to the region.
        3. Click the menu to close it.
        """
        self.expand_menu()
        for component_name in components:
            ElementHandler.click_element(
                f"{self.locator} .small-box:nth-child({self.menu_items.index(component_name)+1})"
            )
        self.expand_menu()

    @wait_after_for_timeout(reason="Ensure menu is fully expanded.")
    def expand_menu(self):
        self.menu.click()

    @property
    def locator(self) -> str:
        return self._locator
