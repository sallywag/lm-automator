import pytest
from selenium.common.exceptions import TimeoutException

from lm_automator.region import Region
from lm_automator.element_handler import ElementHandler
from lm_automator.common import DRIVER


@pytest.mark.usefixtures("login")
class TestRegion:

    @classmethod
    def setup_class(cls):
        cls.region = Region(
            locator=".pre-content-region",
            menu_items=["ad", "doomsday", "school-closing"],
        )

    @classmethod
    def get_all_components_in_pre_content_region(cls):
        try:
            return ElementHandler.get_all_elements(".pre-content-region [component]")
        except TimeoutException:
            return []

    def setup_method(self):
        DRIVER.refresh()
        ElementHandler.wait_for_timeout(reason="Overlay needs to disappear.")

    def test_add_components(self):
        assert not ElementHandler.element_is_visible(
            ".pre-content-region .panel [id^=collapse_] .panel-body"
        )
        self.region.add_components(["ad", "doomsday", "school-closing"])
        components = self.get_all_components_in_pre_content_region()
        assert len(components) == 4
        assert components[0].get_attribute("component") == "ads"
        assert components[1].get_attribute("component") == "ads"
        assert components[2].get_attribute("component") == "doomsday"
        assert components[3].get_attribute("component") == "alert-closings"
        assert not ElementHandler.element_is_visible(
            ".pre-content-region .panel [id^=collapse_] .panel-body"
        )
