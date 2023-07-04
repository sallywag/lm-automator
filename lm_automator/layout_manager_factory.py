from typing import Dict

from lm_automator.region import Region
from lm_automator.inputs import Input, Text, Button, Select, Checkbox
from lm_automator.component import Component


class LayoutManagerFactory:

    INPUTS = {"text": Text, "button": Button, "select": Select, "checkbox": Checkbox}

    def __init__(self, model_data: Dict):
        self.model_data = model_data

    def get_region(self, region_name: str, page_name: str) -> Region:
        return Region(
            self.model_data["regions"][region_name]["locator"], self.model_data["menus"][page_name][region_name]
        )

    def get_input(self, region_name: str, component_name: str, input_name: str) -> Input:
        class_ = self.INPUTS[
            self.model_data["components"][component_name][input_name]["type"]
        ]
        return class_(
            self.model_data["regions"][region_name]["locator"]
            + " "
            + self.model_data["components"]["locator"]
            + " "
            + self.model_data["components"][component_name][input_name]["locator"]
        )

    def get_component(self, region_name: str, position: str) -> Component:
        return Component(
            self.model_data["regions"][region_name]["locator"]
            + " "
            + self.model_data["components"]["locator"],
            position
        )
