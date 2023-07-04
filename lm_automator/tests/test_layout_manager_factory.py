from lm_automator.layout_manager_factory import LayoutManagerFactory

from lm_automator.region import Region
from lm_automator.inputs import Text, Button, Checkbox, Select
from lm_automator.component import Component

MODEL_DATA = {
    "menus": {"page-1": {"region-1": ["component-1", "component-2", "component-3"]}},
    "regions": {"region-1": {"locator": "region-1-locator"}},
    "components": {
        "locator": "component-locator",
        "component-1": {
            "input-1": {"type": "text", "locator": "input-1-locator"},
            "input-2": {"type": "button", "locator": "input-3-locator"},
            "input-3": {"type": "checkbox", "locator": "input-3-locator"},
            "input-4": {"type": "select", "locator": "input-4-locator"}
        },
    },
}

FACTORY = LayoutManagerFactory(MODEL_DATA)
REGION = FACTORY.get_region(region_name="region-1", page_name="page-1")
COMPONENT = FACTORY.get_component(region_name="region-1", position=1)


def test_get_region_returns_region_object():
    assert isinstance(REGION, Region)


def test_get_region_returns_region_with_expected_locator():
    assert REGION.locator == "region-1-locator"


def test_get_region_returns_region_with_expected_menu_items():
    assert ["component-1", "component-2", "component-3"] == REGION.menu_items


def test_get_input_return_text_object():
    assert isinstance(
        FACTORY.get_input(
            region_name="region-1", component_name="component-1", input_name="input-1"
        ),
        Text,
    )


def test_get_input_return_button_object():
    assert isinstance(
        FACTORY.get_input(
            region_name="region-1", component_name="component-1", input_name="input-2"
        ),
        Button,
    )


def test_get_input_return_checkbox_object():
    assert isinstance(
        FACTORY.get_input(
            region_name="region-1", component_name="component-1", input_name="input-3"
        ),
        Checkbox,
    )


def test_get_input_return_select_object():
    assert isinstance(
        FACTORY.get_input(
            region_name="region-1", component_name="component-1", input_name="input-4"
        ),
        Select,
    )


def test_get_input_returns_input_with_expected_locator():
    assert (
        FACTORY.get_input(
            region_name="region-1", component_name="component-1", input_name="input-1"
        ).locator
        == "region-1-locator component-locator input-1-locator"
    )


def test_get_component_returns_component_object():
    assert isinstance(COMPONENT, Component)


def test_get_component_returns_component_object_with_expected_position():
    assert COMPONENT.position == 1


def test_get_component_returns_component_object_with_expected_locator():
    assert COMPONENT.locator == "region-1-locator component-locator:nth-child(1)"
