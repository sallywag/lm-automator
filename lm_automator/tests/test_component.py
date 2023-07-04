import pytest

from lm_automator.component import Component
from lm_automator.element_handler import ElementHandler
from lm_automator.common import DRIVER


@pytest.mark.usefixtures("login")
class TestComponent:
    @classmethod
    def setup_class(cls):
        cls.region_locator = ".pre-content-region"
        cls.component = Component(
            locator=f"{cls.region_locator} [component]", position=2,
        )

    @classmethod
    def add_component_to_page(cls):
        ElementHandler.click_element(f"{cls.region_locator} #heading_preContent")
        ElementHandler.click_element(
            f"{cls.region_locator} .small-box.cursor-grab.bg-green"
        )

    @classmethod
    def component_is_open(cls):
        return ElementHandler.element_is_present(
            f"{cls.component.locator}.box:not(.collapsed-box)"
        )

    @classmethod
    def component_is_closed(cls):
        return ElementHandler.element_is_present(
            f"{cls.component.locator}.box.collapsed-box"
        )

    @classmethod
    def component_was_deleted(cls):
        return (
            len(ElementHandler.get_all_elements(f"{cls.region_locator} [component]"))
            == 1
        )

    @classmethod
    def setup_method(cls):
        DRIVER.refresh()
        ElementHandler.wait_for_element_to_disappear(
            f"{cls.region_locator} .overlay",
            reason="Loading overlay over region must be gone to add a component.",
        )
        cls.add_component_to_page()

    def test_edit_method_opens_component_modal(self):
        self.component.edit()
        assert self.component_is_open()

    def test_edit_method_closes_component_modal_when_modal_is_open(self):
        self.component.edit()
        self.component.edit()
        assert self.component_is_closed()

    def test_delete_method_deletes_component(self):
        self.component.delete()
        assert self.component_was_deleted()
